from pydantic import AnyUrl, Field
from typing import List, Optional, Union
from pydantic_schemaorg.Distance import Distance
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from pydantic_schemaorg.Person import Person
from pydantic_schemaorg.CreativeWork import CreativeWork


class VisualArtwork(CreativeWork):
    """A work of art that is primarily visual in character.

    See https://schema.org/VisualArtwork.

    """
    type_: str = Field("VisualArtwork", const=True, alias='@type')
    artworkSurface: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The supporting materials for the artwork, e.g. Canvas, Paper, Wood, Board, etc.",
    )
    depth: Optional[Union[List[Union[Distance, QuantitativeValue, str]], Union[Distance, QuantitativeValue, str]]] = Field(
        None,
        description="The depth of the item.",
    )
    artEdition: Optional[Union[List[Union[int, str]], Union[int, str]]] = Field(
        None,
        description="The number of copies when multiple copies of a piece of artwork are produced - e.g. for"
     "a limited edition of 20 prints, 'artEdition' refers to the total number of copies (in"
     "this example \"20\").",
    )
    colorist: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The individual who adds color to inked drawings.",
    )
    height: Optional[Union[List[Union[Distance, QuantitativeValue, str]], Union[Distance, QuantitativeValue, str]]] = Field(
        None,
        description="The height of the item.",
    )
    artMedium: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The material used. (e.g. Oil, Watercolour, Acrylic, Linoprint, Marble, Cyanotype,"
     "Digital, Lithograph, DryPoint, Intaglio, Pastel, Woodcut, Pencil, Mixed Media, etc.)",
    )
    artist: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The primary artist for a work in a medium other than pencils or digital line art--for example,"
     "if the primary artwork is done in watercolors or digital paints.",
    )
    width: Optional[Union[List[Union[Distance, QuantitativeValue, str]], Union[Distance, QuantitativeValue, str]]] = Field(
        None,
        description="The width of the item.",
    )
    letterer: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The individual who adds lettering, including speech balloons and sound effects, to"
     "artwork.",
    )
    artform: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="e.g. Painting, Drawing, Sculpture, Print, Photograph, Assemblage, Collage, etc.",
    )
    surface: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="A material used as a surface in some artwork, e.g. Canvas, Paper, Wood, Board, etc.",
    )
    penciler: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The individual who draws the primary narrative artwork.",
    )
    inker: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="The individual who traces over the pencil drawings in ink after pencils are complete.",
    )
    

VisualArtwork.update_forward_refs()
