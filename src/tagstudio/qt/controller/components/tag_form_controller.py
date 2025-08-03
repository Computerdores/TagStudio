from typing import TYPE_CHECKING, override

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Tag
from tagstudio.qt.view.components.tag_form_view import TagForm, TagFormComponentView

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class TagFormComponent(TagFormComponentView):
    __lib: Library
    __current_entry: int

    def __init__(self, driver: "QtDriver", form: TagForm, parent=None):
        super().__init__(driver, form, parent)
        self.__lib = driver.lib

    @override
    def set_entry(self, entry: int):  # type: ignore[misc]
        self.__current_entry = entry
        return super().set_entry(entry)

    def _on_tag_click(self, tag: Tag):
        self.__lib.add_tags_to_entries(self.__current_entry, tag.id)
        self.on_update.emit()
