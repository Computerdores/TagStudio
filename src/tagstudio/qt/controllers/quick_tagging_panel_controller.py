from typing import TYPE_CHECKING, override

from tagstudio.core.library.alchemy.enums import BrowsingState
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.utils.types import unwrap
from tagstudio.qt.views.panel_modal import PanelModal
from tagstudio.qt.views.quick_tagging_panel_view import QuickTaggingPanelView

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanel(QuickTaggingPanelView):
    __lib: Library
    __results: list[int]
    __index: int

    def __init__(self, driver: "QtDriver"):
        super().__init__(driver)
        self.__lib = driver.lib

    @override
    def _on_next(self):  # type: ignore[misc]
        self.__update_index(+1)

    @override
    def _on_previous(self):  # type: ignore[misc]
        self.__update_index(-1)

    def set_search(self, query: BrowsingState) -> None:
        self.__index = 0

        self.__results = self.__lib.search_library(query, None).ids

        self.__update_index()

    def __update_index(self, diff: int = 0) -> None:
        self.__index = (self.__index + diff) % len(self.__results)
        self._set_entry(unwrap(self.__lib.get_entry(self.__results[self.__index])))

    @classmethod
    def build_modal(cls, driver: "QtDriver") -> PanelModal["QuickTaggingPanel"]:
        w: PanelModal[QuickTaggingPanel] = PanelModal(cls(driver), "Quick Tagging", has_save=False)
        w.root_layout.setContentsMargins(6, 6, 6, 6)
        w.title_widget.setVisible(False)
        w.button_container.setVisible(False)
        return w
