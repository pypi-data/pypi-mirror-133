from pydantic import Field
from pydantic_schemaorg.Store import Store


class MusicStore(Store):
    """A music store.

    See https://schema.org/MusicStore.

    """
    type_: str = Field("MusicStore", const=True, alias='@type')
    

MusicStore.update_forward_refs()
