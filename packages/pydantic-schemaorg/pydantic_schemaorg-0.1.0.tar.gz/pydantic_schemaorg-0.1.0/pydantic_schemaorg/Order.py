from pydantic import AnyUrl, StrictBool, Field
from datetime import datetime, date
from typing import List, Optional, Union
from decimal import Decimal
from pydantic_schemaorg.ParcelDelivery import ParcelDelivery
from pydantic_schemaorg.Product import Product
from pydantic_schemaorg.OrderItem import OrderItem
from pydantic_schemaorg.Service import Service
from pydantic_schemaorg.PostalAddress import PostalAddress
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Person import Person
from pydantic_schemaorg.OrderStatus import OrderStatus
from pydantic_schemaorg.Invoice import Invoice
from pydantic_schemaorg.Offer import Offer
from pydantic_schemaorg.PaymentMethod import PaymentMethod
from pydantic_schemaorg.Intangible import Intangible


class Order(Intangible):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line"
     "items, each represented by an Offer that has been accepted by the customer.

    See https://schema.org/Order.

    """
    type_: str = Field("Order", const=True, alias='@type')
    orderDate: Optional[Union[List[Union[datetime, date, str]], Union[datetime, date, str]]] = Field(
        None,
        description="Date order was placed.",
    )
    paymentDue: Optional[Union[List[Union[datetime, str]], Union[datetime, str]]] = Field(
        None,
        description="The date that payment is due.",
    )
    discount: Optional[Union[List[Union[Decimal, str]], Union[Decimal, str]]] = Field(
        None,
        description="Any discount applied (to an Order).",
    )
    discountCode: Optional[Union[List[str], str]] = Field(
        None,
        description="Code used to redeem a discount.",
    )
    paymentMethodId: Optional[Union[List[str], str]] = Field(
        None,
        description="An identifier for the method of payment used (e.g. the last 4 digits of the credit card).",
    )
    orderDelivery: Optional[Union[List[Union[ParcelDelivery, str]], Union[ParcelDelivery, str]]] = Field(
        None,
        description="The delivery of the parcel related to this order or order item.",
    )
    discountCurrency: Optional[Union[List[str], str]] = Field(
        None,
        description="The currency of the discount. Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217)"
     "e.g. \"USD\"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)"
     "for cryptocurrencies e.g. \"BTC\"; well known names for [Local Exchange Tradings Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)"
     "(LETS) and other currency types e.g. \"Ithaca HOUR\".",
    )
    isGift: Optional[Union[List[Union[StrictBool, str]], Union[StrictBool, str]]] = Field(
        None,
        description="Was the offer accepted as a gift for someone other than the buyer.",
    )
    orderedItem: Optional[Union[List[Union[Product, OrderItem, Service, str]], Union[Product, OrderItem, Service, str]]] = Field(
        None,
        description="The item ordered.",
    )
    billingAddress: Optional[Union[List[Union[PostalAddress, str]], Union[PostalAddress, str]]] = Field(
        None,
        description="The billing address for the order.",
    )
    customer: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="Party placing the order or paying the invoice.",
    )
    seller: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
     "also be a provider.",
    )
    orderStatus: Optional[Union[List[Union[OrderStatus, str]], Union[OrderStatus, str]]] = Field(
        None,
        description="The current status of the order.",
    )
    partOfInvoice: Optional[Union[List[Union[Invoice, str]], Union[Invoice, str]]] = Field(
        None,
        description="The order is being paid as part of the referenced Invoice.",
    )
    paymentDueDate: Optional[Union[List[Union[datetime, date, str]], Union[datetime, date, str]]] = Field(
        None,
        description="The date that payment is due.",
    )
    confirmationNumber: Optional[Union[List[str], str]] = Field(
        None,
        description="A number that confirms the given order or payment has been received.",
    )
    orderNumber: Optional[Union[List[str], str]] = Field(
        None,
        description="The identifier of the transaction.",
    )
    acceptedOffer: Optional[Union[List[Union[Offer, str]], Union[Offer, str]]] = Field(
        None,
        description="The offer(s) -- e.g., product, quantity and price combinations -- included in the order.",
    )
    merchant: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="'merchant' is an out-dated term for 'seller'.",
    )
    paymentUrl: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The URL for sending a payment.",
    )
    paymentMethod: Optional[Union[List[Union[PaymentMethod, str]], Union[PaymentMethod, str]]] = Field(
        None,
        description="The name of the credit card or other method of payment for the order.",
    )
    broker: Optional[Union[List[Union[Organization, Person, str]], Union[Organization, Person, str]]] = Field(
        None,
        description="An entity that arranges for an exchange between a buyer and a seller. In most cases a broker"
     "never acquires or releases ownership of a product or service involved in an exchange."
     "If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms"
     "are preferred.",
    )
    

Order.update_forward_refs()
