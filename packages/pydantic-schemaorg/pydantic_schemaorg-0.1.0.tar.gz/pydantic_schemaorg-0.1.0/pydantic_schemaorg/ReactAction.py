from pydantic import Field
from pydantic_schemaorg.AssessAction import AssessAction


class ReactAction(AssessAction):
    """The act of responding instinctively and emotionally to an object, expressing a sentiment.

    See https://schema.org/ReactAction.

    """
    type_: str = Field("ReactAction", const=True, alias='@type')
    

ReactAction.update_forward_refs()
