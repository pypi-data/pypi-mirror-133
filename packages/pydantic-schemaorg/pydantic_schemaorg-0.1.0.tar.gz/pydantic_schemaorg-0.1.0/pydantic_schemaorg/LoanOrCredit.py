from pydantic import AnyUrl, StrictBool, Field
from pydantic_schemaorg.RepaymentSpecification import RepaymentSpecification
from typing import List, Optional, Any, Union
from pydantic_schemaorg.Thing import Thing
from decimal import Decimal
from pydantic_schemaorg.MonetaryAmount import MonetaryAmount
from pydantic_schemaorg.Duration import Duration
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from pydantic_schemaorg.FinancialProduct import FinancialProduct


class LoanOrCredit(FinancialProduct):
    """A financial product for the loaning of an amount of money, or line of credit, under agreed"
     "terms and charges.

    See https://schema.org/LoanOrCredit.

    """
    type_: str = Field("LoanOrCredit", const=True, alias='@type')
    loanRepaymentForm: Optional[Union[List[Union[RepaymentSpecification, str]], Union[RepaymentSpecification, str]]] = Field(
        None,
        description="A form of paying back money previously borrowed from a lender. Repayment usually takes"
     "the form of periodic payments that normally include part principal plus interest in"
     "each payment.",
    )
    requiredCollateral: Optional[Union[List[Union[str, Thing]], Union[str, Thing]]] = Field(
        None,
        description="Assets required to secure loan or credit repayments. It may take form of third party pledge,"
     "goods, financial instruments (cash, securities, etc.)",
    )
    renegotiableLoan: Optional[Union[List[Union[StrictBool, str]], Union[StrictBool, str]]] = Field(
        None,
        description="Whether the terms for payment of interest can be renegotiated during the life of the loan.",
    )
    loanType: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The type of a loan or credit.",
    )
    amount: Optional[Union[List[Union[Decimal, MonetaryAmount, str]], Union[Decimal, MonetaryAmount, str]]] = Field(
        None,
        description="The amount of money.",
    )
    recourseLoan: Optional[Union[List[Union[StrictBool, str]], Union[StrictBool, str]]] = Field(
        None,
        description="The only way you get the money back in the event of default is the security. Recourse is"
     "where you still have the opportunity to go back to the borrower for the rest of the money.",
    )
    gracePeriod: Optional[Union[List[Union[Duration, str]], Union[Duration, str]]] = Field(
        None,
        description="The period of time after any due date that the borrower has to fulfil its obligations before"
     "a default (failure to pay) is deemed to have occurred.",
    )
    loanTerm: Optional[Union[List[Union[QuantitativeValue, str]], Union[QuantitativeValue, str]]] = Field(
        None,
        description="The duration of the loan or credit agreement.",
    )
    currency: Optional[Union[List[str], str]] = Field(
        None,
        description="The currency in which the monetary amount is expressed. Use standard formats: [ISO 4217"
     "currency format](http://en.wikipedia.org/wiki/ISO_4217) e.g. \"USD\"; [Ticker"
     "symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies"
     "e.g. \"BTC\"; well known names for [Local Exchange Tradings Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)"
     "(LETS) and other currency types e.g. \"Ithaca HOUR\".",
    )
    

LoanOrCredit.update_forward_refs()
