from pydantic import AnyUrl, Field
from pydantic_schemaorg.Duration import Duration
from typing import List, Optional, Union
from pydantic_schemaorg.DefinedTerm import DefinedTerm
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.AdministrativeArea import AdministrativeArea
from pydantic_schemaorg.CreativeWork import CreativeWork


class EducationalOccupationalCredential(CreativeWork):
    """An educational or occupational credential. A diploma, academic degree, certification,"
     "qualification, badge, etc., that may be awarded to a person or other entity that meets"
     "the requirements defined by the credentialer.

    See https://schema.org/EducationalOccupationalCredential.

    """
    type_: str = Field("EducationalOccupationalCredential", const=True, alias='@type')
    validFor: Optional[Union[List[Union[Duration, str]], Union[Duration, str]]] = Field(
        None,
        description="The duration of validity of a permit or similar thing.",
    )
    competencyRequired: Optional[Union[List[Union[AnyUrl, str, DefinedTerm]], Union[AnyUrl, str, DefinedTerm]]] = Field(
        None,
        description="Knowledge, skill, ability or personal attribute that must be demonstrated by a person"
     "or other entity in order to do something such as earn an Educational Occupational Credential"
     "or understand a LearningResource.",
    )
    educationalLevel: Optional[Union[List[Union[AnyUrl, str, DefinedTerm]], Union[AnyUrl, str, DefinedTerm]]] = Field(
        None,
        description="The level in terms of progression through an educational or training context. Examples"
     "of educational levels include 'beginner', 'intermediate' or 'advanced', and formal"
     "sets of level indicators.",
    )
    recognizedBy: Optional[Union[List[Union[Organization, str]], Union[Organization, str]]] = Field(
        None,
        description="An organization that acknowledges the validity, value or utility of a credential. Note:"
     "recognition may include a process of quality assurance or accreditation.",
    )
    validIn: Optional[Union[List[Union[AdministrativeArea, str]], Union[AdministrativeArea, str]]] = Field(
        None,
        description="The geographic area where a permit or similar thing is valid.",
    )
    credentialCategory: Optional[Union[List[Union[AnyUrl, str, DefinedTerm]], Union[AnyUrl, str, DefinedTerm]]] = Field(
        None,
        description="The category or type of credential being described, for example \"degree”, “certificate”,"
     "“badge”, or more specific term.",
    )
    

EducationalOccupationalCredential.update_forward_refs()
