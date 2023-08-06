from pydantic import Field
from pydantic_schemaorg.PaymentStatusType import PaymentStatusType


class PaymentAutomaticallyApplied(PaymentStatusType):
    """An automatic payment system is in place and will be used.

    See https://schema.org/PaymentAutomaticallyApplied.

    """
    type_: str = Field("PaymentAutomaticallyApplied", const=True, alias='@type')
    

PaymentAutomaticallyApplied.update_forward_refs()
