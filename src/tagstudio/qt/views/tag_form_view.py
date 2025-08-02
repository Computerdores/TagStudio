from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Tag
from tagstudio.qt.controllers.tag_box_controller import TagBoxWidget
from tagstudio.qt.mixed.field_containers import FieldContainer

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class TagForm:
    __lib: Library
    _fields: list[tuple[str, list[Tag]]] = []

    def __init__(self, driver: "QtDriver"):
        self.__lib = driver.lib

    def add_field(self, field_name: str, possible_values: list[Tag | str | int]) -> "TagForm":
        tags = [
            tag
            for val in possible_values
            if (
                tag := val
                if isinstance(val, Tag)
                else self.__lib.get_tag_by_name(val)
                if isinstance(val, str)
                else self.__lib.get_tag(val)
            )
            is not None
        ]
        self._fields.append((field_name, tags))
        return self


class TagFormComponentView(QWidget):
    __lib: Library

    def __init__(self, driver: "QtDriver", form: TagForm, parent=None):
        super().__init__(parent)
        self.__lib = driver.lib

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for field_name, tags in form._fields:
            container = FieldContainer(field_name, inline=False)
            tbw = TagBoxWidget(field_name, driver)
            tbw.set_tags(set(tags))
            container.set_inner_widget(tbw)
            root_layout.addWidget(container)
