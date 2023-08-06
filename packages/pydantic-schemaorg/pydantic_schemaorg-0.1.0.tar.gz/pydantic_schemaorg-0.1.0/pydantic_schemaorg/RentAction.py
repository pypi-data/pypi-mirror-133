from pydantic import Field
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Union
from pydantic_schemaorg.RealEstateAgent import RealEstateAgent
from pydantic_schemaorg.TradeAction import TradeAction


class RentAction(TradeAction):
    """The act of giving money in return for temporary use, but not ownership, of an object such"
     "as a vehicle or property. For example, an agent rents a property from a landlord in exchange"
     "for a periodic payment.

    See https://schema.org/RentAction.

    """
    type_: str = Field("RentAction", const=True, alias='@type')
    landlord: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="A sub property of participant. The owner of the real estate property.",
    )
    realEstateAgent: Optional[Union[List[Union[RealEstateAgent, str]], Union[RealEstateAgent, str]]] = Field(
        None,
        description="A sub property of participant. The real estate agent involved in the action.",
    )
    

RentAction.update_forward_refs()
