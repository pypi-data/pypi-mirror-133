from pydantic import Field
from pydantic_schemaorg.Periodical import Periodical


class Newspaper(Periodical):
    """A publication containing information about varied topics that are pertinent to general"
     "information, a geographic area, or a specific subject matter (i.e. business, culture,"
     "education). Often published daily.

    See https://schema.org/Newspaper.

    """
    type_: str = Field("Newspaper", const=True, alias='@type')
    

Newspaper.update_forward_refs()
