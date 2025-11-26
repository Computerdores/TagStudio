from typing import TYPE_CHECKING, cast, override

import structlog
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QInputDialog, QWidget

from tagstudio.core.library.alchemy.enums import BrowsingState
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.utils.types import unwrap
from tagstudio.qt.mixed.add_field import AddFieldModal
from tagstudio.qt.mixed.tag_search import TagSearchModal
from tagstudio.qt.views.panel_modal import PanelModal
from tagstudio.qt.views.quick_tagging_panel_view import QuickTaggingPanelView
from tagstudio.qt.views.tag_form_view import TagForm

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver

logger = structlog.get_logger(__name__)


class QuickTaggingPanel(QuickTaggingPanelView):
    __lib: Library
    __results: list[int]
    __index: int

    def __init__(self, driver: "QtDriver", form: TagForm):
        super().__init__(driver, form)
        self.__lib = driver.lib
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    @override
    def _on_next(self):  # type: ignore[misc]
        self.__update_index(+1)

    @override
    def _on_previous(self):  # type: ignore[misc]
        self.__update_index(-1)

    @override
    def _add_field_button_callback(self):
        def action(field_list: list[str]):
            for field_id in field_list:
                self.__lib.add_field_to_entry(self.__results[self.__index], field_id=field_id)
            self.__update_index()

        afm = AddFieldModal(self.__lib)
        afm.done.connect(action)
        afm.show()

    @override
    def _add_tag_button_callback(self):
        tsm = TagSearchModal(self.__lib, is_tag_chooser=True)
        tsm.tsp.tag_chosen.connect(
            lambda tag_id: self.__lib.add_tags_to_entries(self.__results[self.__index], tag_id)
        )
        unwrap(tsm.tsp.panel_done_button).clicked.connect(lambda: self.__update_index())
        tsm.show()

    def set_search(self, query: BrowsingState) -> None:
        self.__index = 0

        self.__results = self.__lib.search_library(query, None).ids

        self.__update_index()

    def __update_index(self, diff: int = 0) -> None:
        self.__index = (self.__index + diff) % len(self.__results)
        self._set_entry(unwrap(self.__lib.get_entry(self.__results[self.__index])))

    @classmethod
    def build_modal(cls, driver: "QtDriver") -> PanelModal["QuickTaggingPanel"] | None:
        text, ok = QInputDialog.getMultiLineText(
            cast(QWidget, None),
            "TagForm Chooser",
            "Enter TagForm JSON:",
            '{"Type": ["Wallpaper","Music"],"Character":["Mario","Luigi"]}',
        )
        if not ok:
            return None

        form = TagForm.from_json(text, driver)
        w: PanelModal[QuickTaggingPanel] = PanelModal(
            cls(driver, form), "Quick Tagging", has_save=False
        )
        w.root_layout.setContentsMargins(6, 6, 6, 6)
        w.title_widget.setVisible(False)
        w.button_container.setVisible(False)
        return w

    @override
    def keyPressEvent(self, event: QKeyEvent):  # type: ignore[misc]
        if event.modifiers() != Qt.KeyboardModifier.NoModifier:
            return super().keyPressEvent(event)

        match event.key():
            case Qt.Key.Key_Left:
                self._on_previous()
            case Qt.Key.Key_Right:
                self._on_next()
            case _:
                return super().keyPressEvent(event)
