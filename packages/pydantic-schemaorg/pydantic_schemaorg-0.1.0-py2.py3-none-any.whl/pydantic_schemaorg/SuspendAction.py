from pydantic import Field
from pydantic_schemaorg.ControlAction import ControlAction


class SuspendAction(ControlAction):
    """The act of momentarily pausing a device or application (e.g. pause music playback or"
     "pause a timer).

    See https://schema.org/SuspendAction.

    """
    type_: str = Field("SuspendAction", const=True, alias='@type')
    

SuspendAction.update_forward_refs()
