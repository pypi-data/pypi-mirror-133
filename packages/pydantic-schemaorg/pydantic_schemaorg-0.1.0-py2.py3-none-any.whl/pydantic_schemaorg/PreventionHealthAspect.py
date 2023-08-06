from pydantic import Field
from pydantic_schemaorg.HealthAspectEnumeration import HealthAspectEnumeration


class PreventionHealthAspect(HealthAspectEnumeration):
    """Information about actions or measures that can be taken to avoid getting the topic or"
     "reaching a critical situation related to the topic.

    See https://schema.org/PreventionHealthAspect.

    """
    type_: str = Field("PreventionHealthAspect", const=True, alias='@type')
    

PreventionHealthAspect.update_forward_refs()
