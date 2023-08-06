from pydantic import Field
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Union
from pydantic_schemaorg.ChooseAction import ChooseAction


class VoteAction(ChooseAction):
    """The act of expressing a preference from a fixed/finite/structured set of choices/options.

    See https://schema.org/VoteAction.

    """
    type_: str = Field("VoteAction", const=True, alias='@type')
    candidate: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="A sub property of object. The candidate subject of this action.",
    )
    

VoteAction.update_forward_refs()
