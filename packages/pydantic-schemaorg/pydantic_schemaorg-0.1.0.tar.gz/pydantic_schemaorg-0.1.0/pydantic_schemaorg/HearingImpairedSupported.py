from pydantic import Field
from pydantic_schemaorg.ContactPointOption import ContactPointOption


class HearingImpairedSupported(ContactPointOption):
    """Uses devices to support users with hearing impairments.

    See https://schema.org/HearingImpairedSupported.

    """
    type_: str = Field("HearingImpairedSupported", const=True, alias='@type')
    

HearingImpairedSupported.update_forward_refs()
