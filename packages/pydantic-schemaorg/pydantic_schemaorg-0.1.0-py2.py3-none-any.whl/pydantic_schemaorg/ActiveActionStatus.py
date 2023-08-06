from pydantic import Field
from pydantic_schemaorg.ActionStatusType import ActionStatusType


class ActiveActionStatus(ActionStatusType):
    """An in-progress action (e.g, while watching the movie, or driving to a location).

    See https://schema.org/ActiveActionStatus.

    """
    type_: str = Field("ActiveActionStatus", const=True, alias='@type')
    

ActiveActionStatus.update_forward_refs()
