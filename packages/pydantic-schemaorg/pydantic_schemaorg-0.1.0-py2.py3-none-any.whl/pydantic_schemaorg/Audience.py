from pydantic import Field
from typing import List, Optional, Union
from pydantic_schemaorg.AdministrativeArea import AdministrativeArea
from pydantic_schemaorg.Intangible import Intangible


class Audience(Intangible):
    """Intended audience for an item, i.e. the group for whom the item was created.

    See https://schema.org/Audience.

    """
    type_: str = Field("Audience", const=True, alias='@type')
    audienceType: Optional[Union[List[str], str]] = Field(
        None,
        description="The target group associated with a given audience (e.g. veterans, car owners, musicians,"
     "etc.).",
    )
    geographicArea: Optional[Union[List[Union[AdministrativeArea, str]], Union[AdministrativeArea, str]]] = Field(
        None,
        description="The geographic area associated with the audience.",
    )
    

Audience.update_forward_refs()
