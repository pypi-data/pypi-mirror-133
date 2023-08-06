from pydantic import Field
from pydantic_schemaorg.BodyOfWater import BodyOfWater


class SeaBodyOfWater(BodyOfWater):
    """A sea (for example, the Caspian sea).

    See https://schema.org/SeaBodyOfWater.

    """
    type_: str = Field("SeaBodyOfWater", const=True, alias='@type')
    

SeaBodyOfWater.update_forward_refs()
