from typing import TYPE_CHECKING

from tagstudio.core.library.alchemy.enums import BrowsingState
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.qt.view.widgets.quick_tagging_panel_view import QuickTaggingPanelView
from tagstudio.qt.widgets.panel import PanelModal

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanel(QuickTaggingPanelView):
    __lib: Library
    __results: list[Entry]
    __index: int

    def __init__(self, driver: "QtDriver"):
        super().__init__(driver)
        self.__lib = driver.lib

    def set_search(self, query: BrowsingState) -> None:
        self.__index = 0

        self.__results = self.__lib.search_library(query, None).items

        self._set_entry(self.__results[self.__index])

    @classmethod
    def build_modal(cls, driver: "QtDriver") -> PanelModal["QuickTaggingPanel"]:
        w: PanelModal[QuickTaggingPanel] = PanelModal(cls(driver), "Quick Tagging", has_save=False)
        w.root_layout.setContentsMargins(6, 6, 6, 6)
        w.title_widget.setVisible(False)
        w.button_container.setVisible(False)
        return w
