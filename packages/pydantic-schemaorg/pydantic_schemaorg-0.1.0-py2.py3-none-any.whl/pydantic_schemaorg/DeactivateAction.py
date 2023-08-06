from pydantic import Field
from pydantic_schemaorg.ControlAction import ControlAction


class DeactivateAction(ControlAction):
    """The act of stopping or deactivating a device or application (e.g. stopping a timer or"
     "turning off a flashlight).

    See https://schema.org/DeactivateAction.

    """
    type_: str = Field("DeactivateAction", const=True, alias='@type')
    

DeactivateAction.update_forward_refs()
