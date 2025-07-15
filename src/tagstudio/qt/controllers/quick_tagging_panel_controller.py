from typing import TYPE_CHECKING

from tagstudio.core.library.alchemy.enums import BrowsingState
from tagstudio.core.utils.types import unwrap
from tagstudio.qt.views.panel_modal import PanelModal
from tagstudio.qt.views.quick_tagging_panel_view import QuickTaggingPanelView

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class QuickTaggingPanel(QuickTaggingPanelView):
    __results: list[int]
    __index: int

    def __init__(self, driver: "QtDriver"):
        super().__init__(driver)

    def set_search(self, query: BrowsingState) -> None:
        self.__index = 0

        self.__results = self._lib.search_library(query, None).ids

        self._set_entry(unwrap(self._lib.get_entry(self.__results[self.__index])).path)

    @classmethod
    def build_modal(cls, driver: "QtDriver") -> PanelModal["QuickTaggingPanel"]:
        return PanelModal(cls(driver), "Quick Tagging", has_save=False)
