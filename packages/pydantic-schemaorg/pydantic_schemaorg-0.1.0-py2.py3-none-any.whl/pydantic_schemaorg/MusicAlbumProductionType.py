from pydantic import Field
from pydantic_schemaorg.Enumeration import Enumeration


class MusicAlbumProductionType(Enumeration):
    """Classification of the album by it's type of content: soundtrack, live album, studio"
     "album, etc.

    See https://schema.org/MusicAlbumProductionType.

    """
    type_: str = Field("MusicAlbumProductionType", const=True, alias='@type')
    

MusicAlbumProductionType.update_forward_refs()
