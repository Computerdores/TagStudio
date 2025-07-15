from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.qt.controller.widgets.preview.preview_thumb_controller import PreviewThumb
from tagstudio.qt.widgets.panel import PanelWidget
from tagstudio.qt.widgets.preview.field_containers import FieldContainers
from tagstudio.qt.widgets.preview.file_attributes import FileAttributes

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanelView(PanelWidget):
    __lib: Library

    def __init__(self, driver: "QtDriver"):
        super().__init__()
        self.__lib = driver.lib

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        left_panel_layout = QVBoxLayout(self)

        self.__file_attrs = FileAttributes(self.__lib, driver)
        left_panel_layout.addWidget(self.__file_attrs)

        self.__fields = FieldContainers(self.__lib, driver)
        left_panel_layout.addWidget(self.__fields)

        root_layout.addLayout(left_panel_layout)

        self.__preview_thumb = PreviewThumb(self.__lib, driver)
        root_layout.addWidget(self.__preview_thumb)

    def _set_entry(self, entry: Entry) -> None:
        assert self.__lib.library_dir is not None
        filepath: Path = self.__lib.library_dir / entry.path

        stats = self.__preview_thumb.display_file(filepath)

        self.__file_attrs.update_stats(filepath, stats)
        self.__fields.update_from_entry(entry.id, update_badges=False)
