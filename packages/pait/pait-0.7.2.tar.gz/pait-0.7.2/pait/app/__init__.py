from importlib import import_module
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from pydantic import BaseConfig

from pait.model.status import PaitStatus

from ..model.core import PaitCoreModel  # type: ignore
from ..model.response import PaitBaseResponseModel  # type: ignore
from .auto_load_app import auto_load_app_class  # type: ignore


def _import_func_from_app(app: Any, fun_name: str) -> Callable:
    app_name: str = app.__class__.__name__.lower()
    if app_name == "flask":
        return getattr(import_module("pait.app.flask"), fun_name)
    elif app_name == "starlette":
        return getattr(import_module("pait.app.starlette"), fun_name)
    elif app_name == "sanic":
        return getattr(import_module("pait.app.sanic"), fun_name)
    elif app_name == "application" and app.__class__.__module__ == "tornado.web":
        return getattr(import_module("pait.app.tornado"), fun_name)
    else:
        raise NotImplementedError(f"Pait not support app name:{app_name}, please check app:{app}")


def _base_call_func(app: Any, fun_name: str, *args: Any, **kwargs: Any) -> Any:
    return _import_func_from_app(app, fun_name)(*args, **kwargs)


def load_app(app: Any, project_name: str = "") -> Dict[str, PaitCoreModel]:
    """Read data from the route that has been registered to `pait`
    Note:This is an implicit method
    """
    return _base_call_func(app, "load_app", app, project_name=project_name)


def add_doc_route(app: Any, prefix: str = "/") -> None:
    return _base_call_func(app, "add_doc_route", prefix=prefix)


def pait(
    enable_mock_response: bool = False,
    pydantic_model_config: Optional[Type[BaseConfig]] = None,
    make_mock_response_fn: Optional[Callable[[Type[PaitBaseResponseModel]], Any]] = None,
    # param check
    pre_depend_list: Optional[List[Callable]] = None,
    at_most_one_of_list: Optional[List[List[str]]] = None,
    required_by: Optional[Dict[str, List[str]]] = None,
    # doc
    author: Optional[Tuple[str]] = None,
    desc: Optional[str] = None,
    summary: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[PaitStatus] = None,
    group: Optional[str] = None,
    tag: Optional[Tuple[str, ...]] = None,
    response_model_list: Optional[List[Type[PaitBaseResponseModel]]] = None,
) -> Callable:
    """provide parameter checks and type conversions for each routing function/cbv class
    Note:This is an implicit method
    """
    load_class_app = auto_load_app_class()
    app_name: str = load_class_app.__name__.lower()
    _pait: Optional[Callable] = getattr(import_module("pait.app." + app_name), "pait")
    if not _pait:
        raise NotImplementedError(f"Pait not support:{load_class_app}")
    return _pait(
        enable_mock_response=enable_mock_response,
        pydantic_model_config=pydantic_model_config,
        make_mock_response_fn=make_mock_response_fn,
        pre_depend_list=pre_depend_list,
        at_most_one_of_list=at_most_one_of_list,
        required_by=required_by,
        author=author,
        desc=desc,
        summary=summary,
        name=name,
        status=status,
        group=group,
        tag=tag,
        response_model_list=response_model_list,
    )
