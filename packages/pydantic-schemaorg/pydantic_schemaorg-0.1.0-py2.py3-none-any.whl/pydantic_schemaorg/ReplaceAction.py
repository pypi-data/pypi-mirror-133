from pydantic import Field
from pydantic_schemaorg.Thing import Thing
from typing import List, Optional, Union
from pydantic_schemaorg.UpdateAction import UpdateAction


class ReplaceAction(UpdateAction):
    """The act of editing a recipient by replacing an old object with a new object.

    See https://schema.org/ReplaceAction.

    """
    type_: str = Field("ReplaceAction", const=True, alias='@type')
    replacer: Optional[Union[List[Union[Thing, str]], Union[Thing, str]]] = Field(
        None,
        description="A sub property of object. The object that replaces.",
    )
    replacee: Optional[Union[List[Union[Thing, str]], Union[Thing, str]]] = Field(
        None,
        description="A sub property of object. The object that is being replaced.",
    )
    

ReplaceAction.update_forward_refs()
