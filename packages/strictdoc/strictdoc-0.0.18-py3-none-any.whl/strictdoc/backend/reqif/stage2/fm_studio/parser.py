from reqif.reqif_bundle import ReqIFBundle

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.requirement import Requirement
from strictdoc.backend.sdoc.models.section import FreeText, Section
from strictdoc.helpers.html import prettify_html_fragment
from strictdoc.backend.reqif.stage2.abstract_parser import (
    AbstractReqIFStage2Parser,
)
from strictdoc.backend.reqif.stage2.fm_studio.mapping import FMStudioMapping
from strictdoc.backend.reqif.stage2.fm_studio.uid_matcher import (
    match_letter_uid,
    match_bullet_uid,
    match_continuation_uid,
)


class FMStudioReqIFStage2Parser(AbstractReqIFStage2Parser):
    def parse_reqif(self, reqif_bundle: ReqIFBundle):
        mapping = FMStudioMapping()
        document = mapping.create_document()
        # TODO: Should we rather show an error that there are no specifications?
        if len(reqif_bundle.core_content.req_if_content.specifications) == 0:
            return document

        specification = reqif_bundle.core_content.req_if_content.specifications[
            0
        ]
        document.name = specification.long_name
        document.section_contents = []
        current_section = document

        for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(
            specification
        ):
            spec_object = reqif_bundle.get_spec_object_by_ref(
                current_hierarchy.spec_object
            )

            if mapping.is_spec_object_section(spec_object):
                section = mapping.create_section_from_spec_object(
                    spec_object,
                    current_hierarchy.level,
                )
                if current_hierarchy.level > current_section.ng_level:
                    current_section.section_contents.append(section)
                elif current_hierarchy.level < current_section.ng_level:
                    for _ in range(
                        0, current_section.ng_level - current_hierarchy.level
                    ):
                        assert not isinstance(current_section, Document)
                        if isinstance(current_section, Section):
                            current_section = current_section.parent

                    current_section.section_contents.append(section)
                else:
                    raise NotImplementedError
            elif mapping.is_spec_object_requirement(spec_object):
                requirement = mapping.create_requirement_from_spec_object(
                    spec_object,
                    document,
                    current_hierarchy.level,
                )
                # The ReqIF example contains cases when a requirement 1.2.3 is
                # followed by sub-requirements: 1.2.3.a, 1.2.3.b, etc.
                # The current solution is to simply to merge the sub-requirement
                # statements into the parent requirement statement, so that the
                # sub-requirements do not appear in the tree.
                # A possible alternative is to use composite requirements, e.g.
                # [COMPOSITE_REQUIREMENT].
                matched_letter_uid = match_letter_uid(requirement.uid)
                if matched_letter_uid:
                    # Assumption: The a) b) c) ... requirements always follow
                    # a requirement. Cannot be a section.
                    assert isinstance(
                        current_section.section_contents[-1], Requirement
                    ), f"{current_section.section_contents[-1]} {spec_object}"

                    parent_requirement = current_section.section_contents[-1]
                    parent_requirement.append_to_multiline_statement(
                        f"<br/>"
                        f"{matched_letter_uid}) "
                        f"{requirement.statement_multiline}"
                    )
                elif match_bullet_uid(requirement.uid):
                    # Assumption: The bullet-point requirements always follow
                    # a requirement. Cannot be a section.
                    assert isinstance(
                        current_section.section_contents[-1], Requirement
                    ), f"{current_section.section_contents[-1]} {spec_object}"

                    parent_requirement = current_section.section_contents[-1]
                    parent_requirement.append_to_multiline_statement(
                        f"<br/>- {requirement.statement_multiline}"
                    )
                elif match_continuation_uid(requirement.uid):
                    # Assumption: The continuation requirements always follow
                    # a requirement. Cannot be a section.
                    assert isinstance(
                        current_section.section_contents[-1], Requirement
                    ), f"{current_section.section_contents[-1]} {spec_object}"

                    parent_requirement = current_section.section_contents[-1]
                    parent_requirement.append_to_multiline_statement(
                        f"<br/>{requirement.statement_multiline}"
                    )
                else:
                    current_section.section_contents.append(requirement)
            elif mapping.is_spec_object_table(spec_object):
                # Assumption: All tables should be rich XHTML content anyway.
                rich_text = spec_object.attribute_map[
                    "_stype_requirement_RichText"
                ]
                rich_text = prettify_html_fragment(rich_text)

                if len(current_section.section_contents) > 0:
                    latest_requirement = current_section.section_contents[-1]
                    if isinstance(latest_requirement, Requirement):
                        latest_requirement.append_to_multiline_statement(
                            rich_text
                        )
                    elif isinstance(latest_requirement, Section):
                        free_text = FreeText(current_section, [rich_text])
                        latest_requirement.free_texts.append(free_text)
                    else:
                        raise NotImplementedError(latest_requirement)
                else:
                    # free_text = FreeText(current_section, [rich_text])
                    # current_section.free_texts.append(free_text)
                    raise NotImplementedError(spec_object)
            elif mapping.is_spec_object_figure(spec_object):
                # Assumption: A Figure always follow a requirement.
                # Cannot be a section.
                assert isinstance(
                    current_section.section_contents[-1], Requirement
                ), f"{current_section.section_contents[-1]} {spec_object}"
                spec_object_rich_text = spec_object.attribute_map[
                    "_stype_requirement_RichText"
                ].replace("media/", "_assets/")

                spec_object_rich_text = prettify_html_fragment(
                    spec_object_rich_text
                )
                spec_object.attribute_map[
                    "_stype_requirement_RichText"
                ] = spec_object_rich_text
                parent_requirement: Requirement = (
                    current_section.section_contents[-1]
                )
                parent_requirement.append_to_multiline_statement(
                    f"\n\n{spec_object_rich_text.strip()}"
                )

            else:
                continue

        return document
