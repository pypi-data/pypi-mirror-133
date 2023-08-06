from pydantic import Field
from pydantic_schemaorg.WearableSizeSystemEnumeration import WearableSizeSystemEnumeration


class WearableSizeSystemGS1(WearableSizeSystemEnumeration):
    """GS1 (formerly NRF) size system for wearables.

    See https://schema.org/WearableSizeSystemGS1.

    """
    type_: str = Field("WearableSizeSystemGS1", const=True, alias='@type')
    

WearableSizeSystemGS1.update_forward_refs()
