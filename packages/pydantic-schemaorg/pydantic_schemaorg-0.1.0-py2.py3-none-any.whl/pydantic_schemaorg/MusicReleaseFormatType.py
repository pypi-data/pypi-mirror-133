from pydantic import Field
from pydantic_schemaorg.Enumeration import Enumeration


class MusicReleaseFormatType(Enumeration):
    """Format of this release (the type of recording media used, ie. compact disc, digital media,"
     "LP, etc.).

    See https://schema.org/MusicReleaseFormatType.

    """
    type_: str = Field("MusicReleaseFormatType", const=True, alias='@type')
    

MusicReleaseFormatType.update_forward_refs()
