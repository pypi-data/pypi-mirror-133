from pydantic import AnyUrl, Field
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Union
from decimal import Decimal
from pydantic_schemaorg.PriceSpecification import PriceSpecification
from datetime import datetime, date
from pydantic_schemaorg.Seat import Seat
from pydantic_schemaorg.Intangible import Intangible


class Ticket(Intangible):
    """Used to describe a ticket to an event, a flight, a bus ride, etc.

    See https://schema.org/Ticket.

    """
    type_: str = Field("Ticket", const=True, alias='@type')
    underName: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="The person or organization the reservation or ticket is for.",
    )
    ticketNumber: Optional[Union[List[str], str]] = Field(
        None,
        description="The unique identifier for the ticket.",
    )
    ticketToken: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="Reference to an asset (e.g., Barcode, QR code image or PDF) usable for entrance.",
    )
    priceCurrency: Optional[Union[List[str], str]] = Field(
        None,
        description="The currency of the price, or a price component when attached to [[PriceSpecification]]"
     "and its subtypes. Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217)"
     "e.g. \"USD\"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)"
     "for cryptocurrencies e.g. \"BTC\"; well known names for [Local Exchange Tradings Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)"
     "(LETS) and other currency types e.g. \"Ithaca HOUR\".",
    )
    totalPrice: Optional[Union[List[Union[Decimal, str, PriceSpecification]], Union[Decimal, str, PriceSpecification]]] = Field(
        None,
        description="The total price for the reservation or ticket, including applicable taxes, shipping,"
     "etc. Usage guidelines: * Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030)"
     "to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols. * Use"
     "'.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid"
     "using these symbols as a readability separator.",
    )
    dateIssued: Optional[Union[List[Union[datetime, date, str]], Union[datetime, date, str]]] = Field(
        None,
        description="The date the ticket was issued.",
    )
    ticketedSeat: Optional[Union[List[Union[Seat, str]], Union[Seat, str]]] = Field(
        None,
        description="The seat associated with the ticket.",
    )
    issuedBy: Optional[Union[List[Union[Organization, str]], Union[Organization, str]]] = Field(
        None,
        description="The organization issuing the ticket or permit.",
    )
    

Ticket.update_forward_refs()
