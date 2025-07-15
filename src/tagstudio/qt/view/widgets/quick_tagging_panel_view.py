from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QHBoxLayout

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.qt.controller.widgets.preview.preview_thumb_controller import PreviewThumb
from tagstudio.qt.widgets.panel import PanelWidget

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanelView(PanelWidget):
    _lib: Library

    def __init__(self, driver: "QtDriver"):
        super().__init__()
        self._lib = driver.lib

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.__preview_thumb = PreviewThumb(self._lib, driver)
        root_layout.addWidget(self.__preview_thumb)

    def _set_entry(self, entry: Entry) -> None:
        assert self._lib.library_dir is not None
        filepath: Path = self._lib.library_dir / entry.path

        self.__preview_thumb.display_file(filepath)
