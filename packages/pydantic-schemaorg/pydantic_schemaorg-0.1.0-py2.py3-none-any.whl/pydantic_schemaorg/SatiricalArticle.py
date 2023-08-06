from pydantic import Field
from pydantic_schemaorg.Article import Article


class SatiricalArticle(Article):
    """An [[Article]] whose content is primarily [[satirical]](https://en.wikipedia.org/wiki/Satire)"
     "in nature, i.e. unlikely to be literally true. A satirical article is sometimes but not"
     "necessarily also a [[NewsArticle]]. [[ScholarlyArticle]]s are also sometimes satirized.

    See https://schema.org/SatiricalArticle.

    """
    type_: str = Field("SatiricalArticle", const=True, alias='@type')
    

SatiricalArticle.update_forward_refs()
