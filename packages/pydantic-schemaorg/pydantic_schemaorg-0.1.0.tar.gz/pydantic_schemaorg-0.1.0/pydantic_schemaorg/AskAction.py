from pydantic import Field
from pydantic_schemaorg.Question import Question
from typing import List, Optional, Union
from pydantic_schemaorg.CommunicateAction import CommunicateAction


class AskAction(CommunicateAction):
    """The act of posing a question / favor to someone. Related actions: * [[ReplyAction]]:"
     "Appears generally as a response to AskAction.

    See https://schema.org/AskAction.

    """
    type_: str = Field("AskAction", const=True, alias='@type')
    question: Optional[Union[List[Union[Question, str]], Union[Question, str]]] = Field(
        None,
        description="A sub property of object. A question.",
    )
    

AskAction.update_forward_refs()
