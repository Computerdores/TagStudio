from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Tag
from tagstudio.qt.controller.components.tag_box_controller import TagBoxWidget
from tagstudio.qt.widgets.fields import FieldContainer

if TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class TagForm:
    __lib: Library
    _fields: list[tuple[str, list[int]]] = []

    def __init__(self, driver: "QtDriver"):
        self.__lib = driver.lib

    def add_field(self, field_name: str, possible_values: list[Tag | str | int]) -> "TagForm":
        """Adds a field to the form with the given name and possible tag values.

        Values can be Tag objects, tag names, or tag IDs.
        The tag values will be stored as tag IDs and resolved on retrieval.
        Duplicate tag IDs will be removed.
        """
        tags = [
            tag_id
            for val in possible_values
            if (
                tag_id := val.id
                if isinstance(val, Tag)
                else (tag.id if (tag := self.__lib.get_tag_by_name(val)) is not None else None)
                if isinstance(val, str)
                else val
            )
            is not None
        ]
        self._fields.append((field_name, tags))
        return self

    def get_fields(self) -> list[tuple[str, list[Tag]]]:
        """Returns a list of all fields after resolving the tag ids to Tag objects."""
        return [
            (name, [tag for i in set(tag_ids) if (tag := self.__lib.get_tag(i)) is not None])
            for name, tag_ids in self._fields
        ]


class TagFormComponentView(QWidget):
    on_update = Signal()

    __tag_boxes: list[TagBoxWidget] = []

    def __init__(self, driver: "QtDriver", form: TagForm, parent=None):
        super().__init__(parent)
        self.__lib = driver.lib
        self.__form = form

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for field_name, tags in form.get_fields():
            container = FieldContainer(field_name, inline=False)

            w = TagBoxWidget(field_name, driver)
            w.set_tags(tags)
            w.override_tag_click_action(self._on_tag_click)
            w.on_update.connect(self.__on_update)
            self.__tag_boxes.append(w)
            container.set_inner_widget(w)

            root_layout.addWidget(container)

    def set_entry(self, entry: int) -> None:
        for tag_box in self.__tag_boxes:
            tag_box.set_entries([entry])

    def _on_tag_click(self, tag: Tag) -> None:
        raise NotImplementedError

    def __on_update(self) -> None:
        self.on_update.emit()
        # Update tag boxes
        for tag_box, field in zip(self.__tag_boxes, self.__form.get_fields(), strict=True):
            assert tag_box.title == field[0], "TagBoxWidget title does not match field name"
            tag_box.set_tags(field[1])
