import warnings

from .base import ElementBase


class Mesh(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Mesh` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
