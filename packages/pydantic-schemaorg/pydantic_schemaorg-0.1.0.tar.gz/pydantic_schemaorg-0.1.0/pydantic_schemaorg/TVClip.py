from pydantic import Field
from pydantic_schemaorg.TVSeries import TVSeries
from typing import List, Optional, Union
from pydantic_schemaorg.Clip import Clip


class TVClip(Clip):
    """A short TV program or a segment/part of a TV program.

    See https://schema.org/TVClip.

    """
    type_: str = Field("TVClip", const=True, alias='@type')
    partOfTVSeries: Optional[Union[List[Union[TVSeries, str]], Union[TVSeries, str]]] = Field(
        None,
        description="The TV series to which this episode or season belongs.",
    )
    

TVClip.update_forward_refs()
