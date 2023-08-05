from typing import Set, Optional, List

from strictdoc.backend.sdoc.models.config_special_field import (
    ConfigSpecialField,
)


class DocumentConfig:  # pylint: disable=too-many-instance-attributes
    @staticmethod
    def default_config(document):
        return DocumentConfig(document, None, None, None, None, None)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        version,
        number,
        special_fields,
        markup: Optional[str],
        auto_levels: Optional[str],
    ):
        self.parent = parent
        self.version = version
        self.number = number
        self.special_fields: List[ConfigSpecialField] = special_fields
        self.markup = markup
        self.auto_levels: bool = auto_levels is None or auto_levels == "On"
        self.ng_auto_levels_specified = auto_levels is not None

        self.special_fields_set: Set[str] = set()
        self.special_fields_required: List[str] = []
        if special_fields:
            for user_field in self.special_fields:
                self.special_fields_set.add(user_field.field_name)
                if (
                    user_field.field_required
                    and user_field.field_required == "Yes"
                ):
                    self.special_fields_required.append(user_field.field_name)
