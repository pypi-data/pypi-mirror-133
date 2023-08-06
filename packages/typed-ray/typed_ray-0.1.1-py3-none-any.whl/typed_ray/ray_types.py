import typing
from typing_extensions import ParamSpec

_T = typing.TypeVar("_T")
_ArgsT = ParamSpec("_ArgsT")
_ReturnT = typing.TypeVar("_ReturnT")

ObjectRefFullName = "typed_ray.ray_types.ObjectRef"


class ObjectRef(typing.Generic[_T]):
    """Object returned by ray.put"""


class ActorHandle(typing.Generic[_T]):
    """Actor handle returned by decorating class with tray.remote_cls"""


class RemoteFunction(typing.Generic[_ArgsT, _ReturnT]):
    # remote: typing.Callable[_ArgsT, ObjectRef[_ReturnT]]
    @property
    def remote(self) -> typing.Callable[_ArgsT, ObjectRef[_ReturnT]]:
        """
        Call a remote function.
        """
