import asyncio
import copy
import inspect
import logging
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from types import TracebackType
from typing import Any, Callable, Coroutine, Dict, List, Mapping, Optional, Tuple, Type, Union

from pydantic import BaseConfig, BaseModel
from pydantic.fields import UndefinedType

from pait import field
from pait.app.base import BaseAppHelper
from pait.exceptions import CheckValueError, NotFoundFieldError, PaitBaseException
from pait.field import BaseField
from pait.util import (
    FuncSig,
    create_pydantic_model,
    gen_tip_exc,
    get_func_sig,
    get_parameter_list_from_class,
    get_parameter_list_from_pydantic_basemodel,
)


def raise_multiple_exc(exc_list: List[Exception]) -> None:
    """
    Multiple exceptions may be thrown during the parsing process, and these will be thrown one by one like a stack
    """
    if not exc_list:
        return
    try:
        raise exc_list.pop()
    finally:
        raise_multiple_exc(exc_list)


def parameter_2_basemodel(
    parameter_value_dict: Dict["inspect.Parameter", Any],
    pydantic_config: Type[BaseConfig],
    use_pydantic_base_model_alias: bool = False,
) -> BaseModel:
    """Convert all parameters into pydantic mods"""
    annotation_dict: Dict[str, Tuple[Type, Any]] = {}
    param_value_dict: Dict[str, Any] = {}
    for parameter, value in parameter_value_dict.items():
        if isinstance(parameter.default, BaseField) and parameter.default.alias:
            # Resolve the key mismatch between Field.alias and request value
            param_field: field.BaseField = copy.deepcopy(parameter.default)
            param_field.default = value
            base_model_key: str = parameter.default.alias if use_pydantic_base_model_alias else parameter.name
        else:
            param_field = parameter.default
            base_model_key = parameter.name
        annotation_dict[base_model_key] = (parameter.annotation, param_field)
        param_value_dict[base_model_key] = value

    return create_pydantic_model(annotation_dict, pydantic_config=pydantic_config)(**param_value_dict)


class BaseParamHandler(object):
    def __init__(
        self,
        app_helper_class: Type[BaseAppHelper],
        func: Callable,
        pydantic_model_config: Type[BaseConfig],
        pre_depend_list: Optional[List[Callable]] = None,
        at_most_one_of_list: Optional[List[List[str]]] = None,
        required_by: Optional[Dict[str, List[str]]] = None,
        args: Any = None,
        kwargs: Any = None,
    ) -> None:
        self._func: Callable = func
        self.args: list = args or []
        self.kwargs: dict = kwargs or {}

        # cbv handle
        self.cbv_instance: Optional[Any] = None
        self.cbv_type: Optional[Type] = None
        if self.args and self.args[0].__class__.__name__ in func.__qualname__:
            self.cbv_instance = self.args[0]
            self.cbv_type = self.cbv_instance.__class__
        # else:
        #     cbv_type = getattr(inspect.getmodule(func), func.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0])

        self._app_helper: BaseAppHelper = app_helper_class(self.cbv_instance, self.args, self.kwargs)  # type: ignore

        self.pre_depend_list: List[Callable] = pre_depend_list or []
        self.at_most_one_of_list: Optional[List[List[str]]] = at_most_one_of_list
        self.required_by: Optional[Dict[str, List[str]]] = required_by
        self.pydantic_model_config: Type[BaseConfig] = pydantic_model_config

        if self.cbv_type:
            self.cbv_param_list: List["inspect.Parameter"] = get_parameter_list_from_class(self.cbv_type)
        else:
            self.cbv_param_list = []

    def _check_param(self) -> None:
        if self.at_most_one_of_list:
            # Check whether each group of parameters appear at the same time
            for at_most_one_of in self.at_most_one_of_list:
                if len([i for i in at_most_one_of if self.kwargs.get(i, None) is not None]) > 1:
                    raise CheckValueError(f"requires at most one of param {' or '.join(at_most_one_of)}")
        if self.required_by:
            # Check dependencies between parameters
            for pre_param, param_list in self.required_by.items():
                if pre_param not in self.kwargs:
                    continue
                for param in param_list:
                    if self.kwargs.get(param, None) is not None and self.kwargs[pre_param] is None:
                        raise CheckValueError(
                            f"{pre_param} requires param {' and '.join(param_list)}, which if not none"
                        )

    def _set_parameter_value_to_args(self, parameter: inspect.Parameter, func_args: list) -> bool:
        """Extract the self parameter of the cbv handler,
        the request parameter of the route and the parameter of type PaitBaseModel,
        and check if there are any other parameters that do not meet the conditions
        """
        if self.cbv_instance and not func_args:
            # first parma must self param
            func_args.append(self._app_helper.cbv_instance)
        elif self._app_helper.check_request_type(parameter.annotation):
            # support request param(def handle(request: Request))
            func_args.append(self._app_helper.request)
        elif issubclass(parameter.annotation, BaseModel):
            return True
        else:
            logging.warning(f"Pait not support args: {parameter}")
        return False

    def request_value_handle(
        self,
        parameter: inspect.Parameter,
        request_value: Any,
        base_model_dict: Optional[Dict[str, Any]],
        parameter_value_dict: Dict["inspect.Parameter", Any],
    ) -> None:
        """parse request_value and set to base_model_dict or parameter_value_dict"""
        param_value: BaseField = parameter.default
        annotation: Type[BaseModel] = parameter.annotation
        param_name: str = parameter.name

        if not isinstance(param_value, BaseField):
            # not support
            # raise PaitBaseException(f"must use {BaseField.__class__.__name__}, no {param_value}")
            return
        elif (
            isinstance(request_value, Mapping)
            # some type like dict, but not isinstance Mapping, e.g: werkzeug.datastructures.EnvironHeaders
            or self._app_helper.check_header_type(type(request_value))
            or self._app_helper.check_form_type(type(request_value))
        ):
            if not param_value.raw_return:
                # The code execution effect should be consistent with the generated documentation, no diversity
                # so remove code:
                #   > if type(param_value.alias) is str and param_value.alias in request_value:
                if type(param_value.alias) is str and param_value.alias:
                    request_value_key: str = param_value.alias
                else:
                    request_value_key = param_name
                request_value = request_value.get(request_value_key, param_value.default)
                if isinstance(request_value, UndefinedType):
                    raise NotFoundFieldError(f"{parameter.name} value is {str(UndefinedType)}")

            if base_model_dict is not None and inspect.isclass(annotation) and issubclass(annotation, BaseModel):
                # parse annotation is pydantic.BaseModel and base_model_dict not None
                base_model_dict[parameter.name] = annotation(**request_value)
            else:
                # parse annotation is python type and pydantic.field
                parameter_value_dict[parameter] = request_value
        else:
            parameter_value_dict[parameter] = request_value

    def get_request_value_from_parameter(self, parameter: inspect.Parameter) -> Union[Any, Coroutine]:
        assert isinstance(parameter.default, BaseField), f"{parameter.name}'s value must pait field"
        field_name: str = parameter.default.get_field_name()
        # Note: not use hasattr with LazyProperty (
        #   because hasattr will calling getattr(obj, name) and catching AttributeError,
        # )
        app_field_func: Optional[Callable] = getattr(self._app_helper, field_name, None)
        if app_field_func is None:
            raise NotFoundFieldError(f"field: {field_name} not found in {self._app_helper}")
        return app_field_func()


class ParamHandler(BaseParamHandler):
    def __init__(
        self,
        app_helper_class: Type[BaseAppHelper],
        func: Callable,
        pydantic_model_config: Type[BaseConfig],
        pre_depend_list: Optional[List[Callable]] = None,
        at_most_one_of_list: Optional[List[List[str]]] = None,
        required_by: Optional[Dict[str, List[str]]] = None,
        args: Any = None,
        kwargs: Any = None,
    ) -> None:
        super().__init__(
            app_helper_class,
            func,
            pydantic_model_config,
            at_most_one_of_list=at_most_one_of_list,
            pre_depend_list=pre_depend_list,
            required_by=required_by,
            args=args,
            kwargs=kwargs,
        )
        self._contextmanager_list: List[AbstractContextManager] = []

    def param_handle(
        self,
        _object: Union[FuncSig, Type, None],
        param_list: List["inspect.Parameter"],
        use_pydantic_base_model_alias: bool = False,
    ) -> Tuple[List[Any], Dict[str, Any]]:
        args_param_list: List[Any] = []
        kwargs_param_dict: Dict[str, Any] = {}

        single_field_dict: Dict["inspect.Parameter", Any] = {}

        for parameter in param_list:
            try:
                if parameter.default != parameter.empty:
                    # kwargs param
                    # support model: def demo(pydantic.BaseModel: BaseModel = pait.field.BaseField())
                    if isinstance(parameter.default, field.Depends):
                        kwargs_param_dict[parameter.name] = self._depend_handle(parameter.default.func)
                    else:
                        request_value: Any = self.get_request_value_from_parameter(parameter)
                        self.request_value_handle(
                            parameter,
                            request_value,
                            kwargs_param_dict,
                            single_field_dict,
                        )
                else:
                    # args param
                    # support model: model: ModelType
                    self.set_parameter_value_to_args(parameter, args_param_list)
            except PaitBaseException as e:
                raise gen_tip_exc(_object, e, parameter)
        # support field: def demo(demo_param: int = pait.field.BaseField())
        if single_field_dict:
            try:
                kwargs_param_dict.update(
                    parameter_2_basemodel(
                        single_field_dict,
                        self.pydantic_model_config,
                        use_pydantic_base_model_alias=use_pydantic_base_model_alias,
                    ).dict(),
                )
            except Exception as e:
                raise e from gen_tip_exc(_object, e)
        return args_param_list, kwargs_param_dict

    def set_parameter_value_to_args(self, parameter: inspect.Parameter, func_args: list) -> None:
        """use func_args param faster return and extend func_args"""
        if not self._set_parameter_value_to_args(parameter, func_args):
            return
        # support pait_model param(def handle(model: PaitBaseModel))
        _pait_model: Type[BaseModel] = parameter.annotation
        _, kwargs = self.param_handle(
            None, get_parameter_list_from_pydantic_basemodel(_pait_model), use_pydantic_base_model_alias=True
        )
        func_args.append(_pait_model(**kwargs))

    def _depend_handle(self, func: Callable) -> Any:
        func_sig: FuncSig = get_func_sig(func)
        _func_args, _func_kwargs = self.param_handle(func_sig, func_sig.param_list)
        func_result: Any = func(*_func_args, **_func_kwargs)
        if isinstance(func_result, AbstractContextManager):
            self._contextmanager_list.append(func_result)
            return func_result.__enter__()
        else:
            return func_result

    def _gen_param(self) -> None:
        # check param from pre depend
        for pre_depend in self.pre_depend_list:
            self._depend_handle(pre_depend)

        # gen and check param from func
        func_sig: FuncSig = get_func_sig(self._func)
        self.args, self.kwargs = self.param_handle(func_sig, func_sig.param_list)

        # gen and check param from class
        if self.cbv_param_list and self.cbv_type:
            _, kwargs = self.param_handle(self.cbv_type, self.cbv_param_list)
            self.cbv_instance.__dict__.update(kwargs)
        return None

    def __enter__(self) -> "BaseParamHandler":
        try:
            self._gen_param()
            self._check_param()
            return self
        except Exception as e:
            raise e from gen_tip_exc(self._func, e)

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> Optional[bool]:
        exc_list: List[Exception] = []
        for contextmanager in self._contextmanager_list:
            try:
                contextmanager.__exit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                exc_list.append(e)
        if exc_list:
            raise_multiple_exc(exc_list)
            return True
        else:
            return False


class AsyncParamHandler(BaseParamHandler):
    def __init__(
        self,
        app_helper_class: Type[BaseAppHelper],
        func: Callable,
        pydantic_model_config: Type[BaseConfig],
        pre_depend_list: Optional[List[Callable]] = None,
        at_most_one_of_list: Optional[List[List[str]]] = None,
        required_by: Optional[Dict[str, List[str]]] = None,
        args: Any = None,
        kwargs: Any = None,
    ) -> None:
        super().__init__(
            app_helper_class,
            func,
            pydantic_model_config,
            at_most_one_of_list=at_most_one_of_list,
            pre_depend_list=pre_depend_list,
            required_by=required_by,
            args=args,
            kwargs=kwargs,
        )
        self._contextmanager_list: List[Union[AbstractAsyncContextManager, AbstractContextManager]] = []

    async def param_handle(
        self,
        _object: Union[FuncSig, Type],
        param_list: List["inspect.Parameter"],
        use_pydantic_base_model_alias: bool = False,
    ) -> Tuple[List[Any], Dict[str, Any]]:
        args_param_list: List[Any] = []
        kwargs_param_dict: Dict[str, Any] = {}
        single_field_dict: Dict["inspect.Parameter", Any] = {}

        for parameter in param_list:
            try:
                if parameter.default != parameter.empty:
                    # kwargs param
                    # support like: def demo(pydantic.BaseModel: BaseModel = pait.field.BaseField())
                    if isinstance(parameter.default, field.Depends):
                        kwargs_param_dict[parameter.name] = await self._depend_handle(parameter.default.func)
                    else:
                        request_value: Any = self.get_request_value_from_parameter(parameter)
                        if asyncio.iscoroutine(request_value) or asyncio.isfuture(request_value):
                            request_value = await request_value
                        self.request_value_handle(parameter, request_value, kwargs_param_dict, single_field_dict)
                else:
                    # args param
                    # support model: model: ModelType
                    await self.set_parameter_value_to_args(_object, parameter, args_param_list)
            except PaitBaseException as e:
                raise gen_tip_exc(_object, e, parameter)
        # support field: def demo(demo_param: int = pait.field.BaseField())
        if single_field_dict:
            try:
                kwargs_param_dict.update(
                    parameter_2_basemodel(
                        single_field_dict,
                        self.pydantic_model_config,
                        use_pydantic_base_model_alias=use_pydantic_base_model_alias,
                    ).dict()
                )
            except Exception as e:
                raise e from gen_tip_exc(_object, e)
        return args_param_list, kwargs_param_dict

    async def set_parameter_value_to_args(
        self, _object: Union[FuncSig, Type], parameter: inspect.Parameter, func_args: list
    ) -> None:
        """use func_args param faster return and extend func_args"""
        if not self._set_parameter_value_to_args(parameter, func_args):
            return
        _pait_model: Type[BaseModel] = parameter.annotation
        _, kwargs = await self.param_handle(
            _object, get_parameter_list_from_pydantic_basemodel(_pait_model), use_pydantic_base_model_alias=True
        )
        func_args.append(_pait_model(**kwargs))

    async def _depend_handle(self, func: Callable) -> Any:
        func_sig: FuncSig = get_func_sig(func)
        _func_args, _func_kwargs = await self.param_handle(func_sig, func_sig.param_list)
        func_result: Any = func(*_func_args, **_func_kwargs)
        if asyncio.iscoroutine(func_result):
            func_result = await func_result
        if isinstance(func_result, AbstractAsyncContextManager):
            self._contextmanager_list.append(func_result)
            return await func_result.__aenter__()
        elif isinstance(func_result, AbstractContextManager):
            self._contextmanager_list.append(func_result)
            return func_result.__enter__()
        else:
            return func_result

    async def _gen_param(self) -> None:
        # check param from pre depend
        for pre_depend in self.pre_depend_list:
            await self._depend_handle(pre_depend)

        # gen and check param from func
        func_sig: FuncSig = get_func_sig(self._func)
        self.args, self.kwargs = await self.param_handle(func_sig, func_sig.param_list)

        # gen and check param from class
        if self.cbv_param_list and self.cbv_type:
            _, kwargs = await self.param_handle(self.cbv_type, self.cbv_param_list)
            self.cbv_instance.__dict__.update(kwargs)
        return None

    async def __aenter__(self) -> "AsyncParamHandler":
        try:
            await self._gen_param()
            self._check_param()
            return self
        except Exception as e:
            raise e from gen_tip_exc(self._func, e)

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> Optional[bool]:
        exc_list: List[Exception] = []
        for contextmanager in self._contextmanager_list:
            try:
                if isinstance(contextmanager, AbstractContextManager):
                    contextmanager.__exit__(exc_type, exc_val, exc_tb)
                else:
                    await contextmanager.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                exc_list.append(e)
        if exc_list:
            raise_multiple_exc(exc_list)
            return True
        else:
            return False
