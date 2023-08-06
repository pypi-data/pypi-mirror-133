from pydantic import Field
from pydantic_schemaorg.BookFormatType import BookFormatType


class AudiobookFormat(BookFormatType):
    """Book format: Audiobook. This is an enumerated value for use with the bookFormat property."
     "There is also a type 'Audiobook' in the bib extension which includes Audiobook specific"
     "properties.

    See https://schema.org/AudiobookFormat.

    """
    type_: str = Field("AudiobookFormat", const=True, alias='@type')
    

AudiobookFormat.update_forward_refs()
