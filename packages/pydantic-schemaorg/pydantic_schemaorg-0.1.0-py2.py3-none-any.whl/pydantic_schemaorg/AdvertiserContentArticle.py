from pydantic import Field
from pydantic_schemaorg.Article import Article


class AdvertiserContentArticle(Article):
    """An [[Article]] that an external entity has paid to place or to produce to its specifications."
     "Includes [advertorials](https://en.wikipedia.org/wiki/Advertorial), sponsored"
     "content, native advertising and other paid content.

    See https://schema.org/AdvertiserContentArticle.

    """
    type_: str = Field("AdvertiserContentArticle", const=True, alias='@type')
    

AdvertiserContentArticle.update_forward_refs()
