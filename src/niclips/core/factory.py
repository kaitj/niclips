"""The factory of rendering images and videos."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ClassVar, TypeVar

from niclips.core.specs import IMG_EXT, VID_EXT
from niclips.typing import StrPath


@dataclass
class RenderedView:
    """Dataclass for rendered view."""

    path: StrPath
    metadata: dict[str, Any]
    figure_type: str

    def __post_init__(self) -> None:
        if isinstance(self.path, str):
            self.path = Path(self.path)
        elif not isinstance(self.path, Path):
            raise TypeError(
                f"'path' must be of type str or Path, not {type(self.path).__name__}"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError(
                f"'metadata' must be of type dict, not {type(self.metadata).__name__}"
            )

        if not isinstance(self.figure_type, str):
            raise TypeError(
                "'figure_type' must be of type str, not "
                f"{type(self.figure_type).__name__}"
            )


class ViewValidator:
    """Validator for rendered views."""

    @staticmethod
    def validate_and_fix(view: RenderedView) -> RenderedView:
        """Adjust view to be compliant with image formats and video codecs."""
        # TODO: ADD FIGURE VALIDATION CODE HERE.
        return view


F = TypeVar("F", bound=Callable)


class ViewFactory:
    """Factory of views to render."""

    _registry: ClassVar[dict[str, Callable]] = {}

    @classmethod
    def list(cls) -> None:
        """List all available views in registry."""
        if not cls._registry:
            print("No views registered.")
        else:
            print("Available views:")
            print("\n".join(cls._registry))

    @classmethod
    def register(cls, name: str | None = None) -> Callable[[F], F]:
        """Register an image or video generation code."""

        def decorator(fn: F) -> F:
            key = name if name is not None else fn.__name__
            cls._registry[key] = fn
            return fn

        return decorator

    @classmethod
    def _infer_output_path(
        cls, args: tuple[Any], kwargs: dict[str, Any]
    ) -> Path | bool:
        """Infer output file path from arguments."""
        valid_exts = IMG_EXT | VID_EXT
        for v in (*args, *kwargs.values()):
            if isinstance(v, StrPath):
                path = Path(v)
                if not (suffix := path.suffix):
                    continue
                if suffix in valid_exts:
                    return path
        return False

    @classmethod
    def render(cls, name: str, *args, **kwargs) -> object:
        """Render from a registered view in the factory."""
        if name not in cls._registry:
            raise ValueError(f"Figure type '{name}' not registered")

        result = cls._registry[name](*args, **kwargs)
        if isinstance(result, RenderedView):
            ViewValidator.validate_and_fix(result)

        # Auto-wrap
        inferred_path = cls._infer_output_path(args, kwargs)
        if not inferred_path:
            raise TypeError(
                f"'{name}' did not return a RenderedView or no file path with a valid "
                "extension could be inferred from arguments for auto-wrapping."
            )

        auto_fig = RenderedView(
            path=inferred_path,
            metadata={"auto_wrapped": True},
            figure_type=name,
        )
        return ViewValidator.validate_and_fix(auto_fig)
