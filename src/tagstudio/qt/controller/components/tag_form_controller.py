from typing import TYPE_CHECKING

from tagstudio.core.library.alchemy.library import Library
from tagstudio.qt.view.components.tag_form_view import TagForm, TagFormComponentView

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class TagFormComponent(TagFormComponentView):
    __lib: Library

    def __init__(self, driver: "QtDriver", form: TagForm, parent=None):
        super().__init__(driver, form, parent)
        self.__lib = driver.lib
