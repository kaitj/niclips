import logging
from pathlib import Path

import pytest

from niclips.core import factory, plugins


class TestPlugins:
    def test_load_single_plugin(self, tmp_path: Path, caplog: pytest.LogCaptureFixture):
        plugin_file = tmp_path / "plugin1.py"
        plugin_file.write_text("""
def test_view():
    return "ok"
""")

        with caplog.at_level(logging.INFO):
            plugins.load_plugins_from_directory(tmp_path)
        assert "Registering test_view"
        assert "test_view" in factory.ViewFactory._registry
        assert factory.ViewFactory._registry["test_view"]()

    def test_skip_duplicate_fn(self, tmp_path: Path, caplog: pytest.LogCaptureFixture):
        @factory.ViewFactory.register("existing_view")
        def existing_view() -> str:
            return "already here"

        plugin_file = tmp_path / "plugin2.py"
        plugin_file.write_text("""
def existing_view():
    return 'duplicate'
""")

        with caplog.at_level(logging.DEBUG):
            plugins.load_plugins_from_directory(tmp_path)
        assert "already used to register a view - skipping" in caplog.text
