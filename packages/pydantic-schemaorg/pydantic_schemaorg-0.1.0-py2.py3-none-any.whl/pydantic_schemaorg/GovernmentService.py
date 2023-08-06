from pydantic import Field
from pydantic_schemaorg.AdministrativeArea import AdministrativeArea
from typing import List, Optional, Union
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Service import Service


class GovernmentService(Service):
    """A service provided by a government organization, e.g. food stamps, veterans benefits,"
     "etc.

    See https://schema.org/GovernmentService.

    """
    type_: str = Field("GovernmentService", const=True, alias='@type')
    jurisdiction: Optional[Union[List[Union[str, AdministrativeArea]], Union[str, AdministrativeArea]]] = Field(
        None,
        description="Indicates a legal jurisdiction, e.g. of some legislation, or where some government"
     "service is based.",
    )
    serviceOperator: Optional[Union[List[Union[Organization, str]], Union[Organization, str]]] = Field(
        None,
        description="The operating organization, if different from the provider. This enables the representation"
     "of services that are provided by an organization, but operated by another organization"
     "like a subcontractor.",
    )
    

GovernmentService.update_forward_refs()
