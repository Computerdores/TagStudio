from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QSplitter, QVBoxLayout, QWidget

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.qt.controller.components.tag_form_controller import TagForm, TagFormComponent
from tagstudio.qt.controller.widgets.preview.preview_thumb_controller import PreviewThumb
from tagstudio.qt.view.widgets.preview_panel_view import BUTTON_STYLE
from tagstudio.qt.widgets.panel import PanelWidget
from tagstudio.qt.widgets.preview.field_containers import FieldContainers
from tagstudio.qt.widgets.preview.file_attributes import FileAttributes

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanelView(PanelWidget):
    __lib: Library
    __current_entry: Entry | None = None

    def __init__(self, driver: "QtDriver"):
        super().__init__()
        self.__lib = driver.lib

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_splitter = QSplitter(self)
        root_splitter.setOrientation(Qt.Orientation.Horizontal)
        root_splitter.setHandleWidth(12)

        # Left Panel
        left_panel = QWidget(self)
        left_panel_layout = QVBoxLayout(left_panel)

        self.__file_attrs = FileAttributes(self.__lib, driver)
        left_panel_layout.addWidget(self.__file_attrs)

        self.__fields = FieldContainers(self.__lib, driver)
        left_panel_layout.addWidget(self.__fields)

        root_splitter.addWidget(left_panel)
        root_splitter.setStretchFactor(0, 2)

        # Center Panel
        self.__preview_thumb = PreviewThumb(self.__lib, driver)
        root_splitter.addWidget(self.__preview_thumb)
        root_splitter.setStretchFactor(1, 1)

        # Right Panel
        right_panel = QWidget(self)
        right_panel_layout = QVBoxLayout(right_panel)

        self.__tag_form = TagFormComponent(
            driver, TagForm(driver).add_field("In-/Outdoor", ["Wallpaper", "Music"])
        )
        self.__tag_form.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.__tag_form.on_update.connect(self.__on_update)
        right_panel_layout.addWidget(self.__tag_form)

        buttons_container = QWidget(right_panel)
        buttons_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(6)

        button_previous = QPushButton("Previous")
        button_previous.setCursor(Qt.CursorShape.PointingHandCursor)
        button_previous.setMinimumHeight(28)
        button_previous.setStyleSheet(BUTTON_STYLE)
        button_previous.clicked.connect(self._on_previous)
        buttons_layout.addWidget(button_previous)
        shortcut_previous = QShortcut(QKeySequence("Left"), self)
        shortcut_previous.activated.connect(button_previous.click)

        button_next = QPushButton("Next")
        button_next.setCursor(Qt.CursorShape.PointingHandCursor)
        button_next.setMinimumHeight(28)
        button_next.setStyleSheet(BUTTON_STYLE)
        button_next.clicked.connect(self._on_next)
        buttons_layout.addWidget(button_next)
        shortcut_next = QShortcut(QKeySequence("Right"), self)
        shortcut_next.activated.connect(button_next.click)

        right_panel_layout.addWidget(buttons_container)

        root_splitter.addWidget(right_panel)
        root_splitter.setStretchFactor(2, 2)

        root_layout.addWidget(root_splitter)

    def _on_previous(self) -> None:
        raise NotImplementedError

    def _on_next(self) -> None:
        raise NotImplementedError

    def _set_entry(self, entry: Entry) -> None:
        self.__current_entry = entry
        assert self.__lib.library_dir is not None
        filepath: Path = self.__lib.library_dir / entry.path

        stats = self.__preview_thumb.display_file(filepath)

        self.__file_attrs.update_stats(filepath, stats)
        self.__fields.update_from_entry(entry.id, update_badges=False)

        self.__tag_form.set_entry(entry.id)

    def __on_update(self) -> None:
        if self.__current_entry is not None:
            self._set_entry(self.__current_entry)
