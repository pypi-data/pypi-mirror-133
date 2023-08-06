from pydantic import Field
from pydantic_schemaorg.Periodical import Periodical


class ComicSeries(Periodical):
    """A sequential publication of comic stories under a unifying title, for example \"The"
     "Amazing Spider-Man\" or \"Groo the Wanderer\".

    See https://schema.org/ComicSeries.

    """
    type_: str = Field("ComicSeries", const=True, alias='@type')
    

ComicSeries.update_forward_refs()
