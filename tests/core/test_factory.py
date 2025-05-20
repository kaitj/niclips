from pathlib import Path

import pytest

from niclips.core import factory


class TestRenderedView:
    @pytest.mark.parametrize("path", [(False), (True)])
    def test_rendered_view_valid_path(self, path: bool):
        out_fpath = Path("test.png") if path else "test.png"
        view = factory.RenderedView(path=out_fpath, metadata={}, figure_type="test")
        assert isinstance(view.path, Path)
        assert view.path.name == "test.png"

    def test_rendered_new_invalid_path(self):
        with pytest.raises(TypeError, match="'path' must be of type str or Path"):
            factory.RenderedView(path=123, metadata={}, figure_type="test")

    @pytest.mark.parametrize("metadata", [([]), ("string-metadata")])
    def test_rendered_view_invalid_metadata(self, metadata: object):
        with pytest.raises(TypeError, match="'metadata' must be of type dict"):
            factory.RenderedView(path="test.png", metadata=metadata, figure_type="test")

    @pytest.mark.parametrize("ftype", [({}), ([]), (123)])
    def test_rendered_view_invalid_figure_type(self, ftype: object):
        with pytest.raises(TypeError, match="'figure_type' must be of type str"):
            factory.RenderedView(path="test.png", metadata={}, figure_type=ftype)


class TestViewFactory:
    def test_list_no_views(self, capfd: pytest.CaptureFixture):
        factory.ViewFactory._registry.clear()
        factory.ViewFactory.list()

        out, _ = capfd.readouterr()
        assert "No views registered." in out

    def test_list_views(self, capfd: pytest.CaptureFixture):
        factory.ViewFactory._registry.clear()

        @factory.ViewFactory.register("custom")
        def dummy_view() -> None:
            pass

        factory.ViewFactory.list()
        out, _ = capfd.readouterr()

        assert "Available views:" in out
        assert "custom" in out

    def test_register_and_render_ret_rendered_view(self):
        @factory.ViewFactory.register("custom")
        def render_custom_test(path: str) -> factory.RenderedView:
            return factory.RenderedView(
                path=path, metadata={"key": "val"}, figure_type="custom"
            )

        result = factory.ViewFactory.render("custom", "test.png")
        assert isinstance(result, factory.RenderedView)
        assert result.figure_type == "custom"
        assert result.path.name == "test.png"

    def test_register_and_render_autowrap(self):
        @factory.ViewFactory.register("auto")
        def render_auto(path: str) -> object:
            return {"not": "RenderedView"}

        result = factory.ViewFactory.render("auto", "test.png")
        assert isinstance(result, factory.RenderedView)
        assert result.path.name == "test.png"
        assert result.metadata["auto_wrapped"] is True
        assert result.figure_type == "auto"

    def test_render_unknown_name(self):
        with pytest.raises(ValueError, match="not registered"):
            factory.ViewFactory.render("unknown", "test.png")

    def test_render_unsupported_ext(self):
        @factory.ViewFactory.register("bad_ext")
        def render_bad_ext(path: str) -> object:
            return factory.RenderedView(path=path, metadata={}, figure_type="test")

        with pytest.raises(ValueError, match="currently unsupported"):
            factory.ViewFactory.render("bad_ext", "test.123")

    @pytest.mark.parametrize("path", [("test"), (123)])
    def test_render_invalid_path(self, path: object):
        @factory.ViewFactory.register("bad")
        def render_bad(path: str) -> object:
            return "not a RenderedView"

        with pytest.raises(TypeError, match="no file path with a valid extension"):
            factory.ViewFactory.render("bad", path=path)
