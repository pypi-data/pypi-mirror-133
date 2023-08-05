from enum import Enum
from typing import Optional, Union

from reqif.models.reqif_spec_object import ReqIFSpecObject

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.document_config import DocumentConfig
from strictdoc.backend.sdoc.models.document_grammar import DocumentGrammar
from strictdoc.backend.sdoc.models.reference import Reference
from strictdoc.backend.sdoc.models.requirement import (
    Requirement,
    RequirementField,
)
from strictdoc.backend.sdoc.models.section import Section, FreeText
from strictdoc.helpers.string import unescape


class ReqIFField(Enum):
    TYPE = "TYPE"
    UID = "UID"
    STATUS = "STATUS"
    TITLE = "TITLE"
    STATEMENT = "STATEMENT"
    COMMENT = "COMMENT"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ReqIFSectionField(Enum):
    TITLE = "TITLE"
    FREETEXT = "FREETEXT"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ReqIFNodeType(Enum):
    SECTION = "SECTION"
    REQUIREMENT = "REQUIREMENT"


class StrictDocReqIFMapping:
    @staticmethod
    def create_document(title: Optional[str]) -> Document:
        document_config = DocumentConfig(
            parent=None,
            version=None,
            number=None,
            special_fields=[],
            markup=None,
            auto_levels=None,
        )
        document_title = title if title else "<No title>"
        document = Document(None, document_title, document_config, None, [], [])
        document.grammar = DocumentGrammar.create_default(document)
        return document

    @staticmethod
    def is_spec_object_section(spec_object: ReqIFSpecObject):
        return spec_object.spec_object_type == ReqIFNodeType.SECTION.value

    @staticmethod
    def is_spec_object_requirement(spec_object):
        return spec_object.spec_object_type == ReqIFNodeType.REQUIREMENT.value

    @staticmethod
    def create_section_from_spec_object(
        spec_object: ReqIFSpecObject, level
    ) -> Section:
        title = spec_object.attribute_map[ReqIFSectionField.TITLE.value]
        free_texts = []
        if ReqIFSectionField.FREETEXT.value in spec_object.attribute_map:
            free_text = unescape(
                spec_object.attribute_map[ReqIFSectionField.FREETEXT.value]
            )
            free_texts.append(
                FreeText(
                    parent=None,
                    parts=[free_text],
                )
            )
        section = Section(
            parent=None,
            uid=None,
            level=None,
            title=title,
            free_texts=free_texts,
            section_contents=[],
        )
        section.ng_level = level
        return section

    @staticmethod
    def create_requirement_from_spec_object(
        spec_object: ReqIFSpecObject,
        parent_section: Union[Section, Document],
        level,
    ) -> Requirement:
        fields = []
        for attribute in spec_object.attributes:
            attribute_value = unescape(attribute.value)
            attribute_multiline_value = None
            if "\n" in attribute_value:
                attribute_multiline_value = attribute_value
                attribute_value = None
            fields.append(
                RequirementField(
                    parent=None,
                    field_name=attribute.name,
                    field_value=attribute_value,
                    field_value_multiline=attribute_multiline_value,
                    field_value_references=None,
                    field_value_special_fields=None,
                )
            )
        requirement = Requirement(
            parent=parent_section, requirement_type="REQUIREMENT", fields=fields
        )

        requirement.ng_level = level
        return requirement

    @staticmethod
    def create_reference(requirement: Requirement, spec_object_parent):
        return Reference(requirement, "Parent", spec_object_parent)
