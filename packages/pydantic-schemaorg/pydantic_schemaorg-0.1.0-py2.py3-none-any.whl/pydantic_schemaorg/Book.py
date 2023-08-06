from pydantic import StrictBool, Field
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Any, Union
from pydantic_schemaorg.BookFormatType import BookFormatType
from pydantic_schemaorg.CreativeWork import CreativeWork


class Book(CreativeWork):
    """A book.

    See https://schema.org/Book.

    """
    type_: str = Field("Book", const=True, alias='@type')
    illustrator: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The illustrator of the book.",
    )
    abridged: Optional[Union[List[Union[StrictBool, str]], Union[StrictBool, str]]] = Field(
        None,
        description="Indicates whether the book is an abridged edition.",
    )
    isbn: Optional[Union[List[str], str]] = Field(
        None,
        description="The ISBN of the book.",
    )
    numberOfPages: Optional[Union[List[Union[int, str]], Union[int, str]]] = Field(
        None,
        description="The number of pages in the book.",
    )
    bookFormat: Optional[Union[List[Union[BookFormatType, str]], Union[BookFormatType, str]]] = Field(
        None,
        description="The format of the book.",
    )
    bookEdition: Optional[Union[List[str], str]] = Field(
        None,
        description="The edition of the book.",
    )
    

Book.update_forward_refs()
