from pydantic import Field
from pydantic_schemaorg.WebPage import WebPage


class QAPage(WebPage):
    """A QAPage is a WebPage focussed on a specific Question and its Answer(s), e.g. in a question"
     "answering site or documenting Frequently Asked Questions (FAQs).

    See https://schema.org/QAPage.

    """
    type_: str = Field("QAPage", const=True, alias='@type')
    

QAPage.update_forward_refs()
