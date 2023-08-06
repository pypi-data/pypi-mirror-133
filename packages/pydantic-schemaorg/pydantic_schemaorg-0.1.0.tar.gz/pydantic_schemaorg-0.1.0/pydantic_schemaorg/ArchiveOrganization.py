from pydantic import Field
from pydantic_schemaorg.ArchiveComponent import ArchiveComponent
from typing import List, Optional, Union
from pydantic_schemaorg.LocalBusiness import LocalBusiness


class ArchiveOrganization(LocalBusiness):
    """An organization with archival holdings. An organization which keeps and preserves"
     "archival material and typically makes it accessible to the public.

    See https://schema.org/ArchiveOrganization.

    """
    type_: str = Field("ArchiveOrganization", const=True, alias='@type')
    archiveHeld: Optional[Union[List[Union[ArchiveComponent, str]], Union[ArchiveComponent, str]]] = Field(
        None,
        description="Collection, [fonds](https://en.wikipedia.org/wiki/Fonds), or item held, kept"
     "or maintained by an [[ArchiveOrganization]].",
    )
    

ArchiveOrganization.update_forward_refs()
