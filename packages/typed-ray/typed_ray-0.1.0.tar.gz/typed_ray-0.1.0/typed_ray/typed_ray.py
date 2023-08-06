import typing

import ray
from typing_extensions import ParamSpec

from typed_ray.ray_types import ObjectRef, RemoteFunction


T = typing.TypeVar("T")


def put(value: T) -> ObjectRef[T]:
    """
    Put a value into the object store.

    Args:
        value: The value to put into the object store.

    Returns:
        An ObjectRef object that can be used to get the value back later.
    """
    return ray.put(value)


@typing.overload
def get(object_refs: ObjectRef[T]) -> T:
    pass


@typing.overload
def get(object_refs: typing.List[ObjectRef[T]]) -> typing.List[T]:
    pass


def get(object_refs: typing.Union[ObjectRef[T], typing.List[ObjectRef[T]]]) -> typing.Union[T, typing.List[T]]:
    """
    Get the value wrapped by ObjectRef.

    Args:
        object_refs: The ObjectRef object usually returned by ray.put.

    Returns:
        The value that was wrapped by ObjectRef.
    """
    return ray.get(object_refs)


_ArgsT = ParamSpec("_ArgsT")
_ReturnT = typing.TypeVar("_ReturnT")


def remote_func(func: typing.Callable[_ArgsT, _ReturnT]) -> RemoteFunction[_ArgsT, _ReturnT]:
    """
    Make a remote function.

    Args:
        func: The function to make remote.

    Returns:
        A remote function.
    """
    return ray.remote(func)


_ClassT = typing.TypeVar("_ClassT", bound=object)


def remote_cls(cls: _ClassT) -> typing.Any:
    """
    Make a remote class.

    Args:
        cls: The class to make remote.

    Returns:
        A remote class.
    """
    return ray.remote(cls)
