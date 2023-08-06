from pydantic import Field
from pydantic_schemaorg.Language import Language
from typing import List, Optional, Union
from pydantic_schemaorg.CreateAction import CreateAction


class WriteAction(CreateAction):
    """The act of authoring written creative content.

    See https://schema.org/WriteAction.

    """
    type_: str = Field("WriteAction", const=True, alias='@type')
    language: Optional[Union[List[Union[Language, str]], Union[Language, str]]] = Field(
        None,
        description="A sub property of instrument. The language used on this action.",
    )
    inLanguage: Optional[Union[List[Union[str, Language]], Union[str, Language]]] = Field(
        None,
        description="The language of the content or performance or used in an action. Please use one of the language"
     "codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also"
     "[[availableLanguage]].",
    )
    

WriteAction.update_forward_refs()
