from pydantic import AnyUrl, Field
from pydantic_schemaorg.ContactPoint import ContactPoint
from typing import List, Optional, Union
from pydantic_schemaorg.HealthPlanNetwork import HealthPlanNetwork
from pydantic_schemaorg.HealthPlanFormulary import HealthPlanFormulary
from pydantic_schemaorg.Intangible import Intangible


class HealthInsurancePlan(Intangible):
    """A US-style health insurance plan, including PPOs, EPOs, and HMOs.

    See https://schema.org/HealthInsurancePlan.

    """
    type_: str = Field("HealthInsurancePlan", const=True, alias='@type')
    contactPoint: Optional[Union[List[Union[ContactPoint, str]], Union[ContactPoint, str]]] = Field(
        None,
        description="A contact point for a person or organization.",
    )
    healthPlanDrugOption: Optional[Union[List[str], str]] = Field(
        None,
        description="TODO.",
    )
    healthPlanMarketingUrl: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The URL that goes directly to the plan brochure for the specific standard plan or plan"
     "variation.",
    )
    usesHealthPlanIdStandard: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The standard for interpreting thePlan ID. The preferred is \"HIOS\". See the Centers"
     "for Medicare & Medicaid Services for more details.",
    )
    benefitsSummaryUrl: Optional[Union[List[Union[AnyUrl, str]], Union[AnyUrl, str]]] = Field(
        None,
        description="The URL that goes directly to the summary of benefits and coverage for the specific standard"
     "plan or plan variation.",
    )
    healthPlanId: Optional[Union[List[str], str]] = Field(
        None,
        description="The 14-character, HIOS-generated Plan ID number. (Plan IDs must be unique, even across"
     "different markets.)",
    )
    includesHealthPlanNetwork: Optional[Union[List[Union[HealthPlanNetwork, str]], Union[HealthPlanNetwork, str]]] = Field(
        None,
        description="Networks covered by this plan.",
    )
    healthPlanDrugTier: Optional[Union[List[str], str]] = Field(
        None,
        description="The tier(s) of drugs offered by this formulary or insurance plan.",
    )
    includesHealthPlanFormulary: Optional[Union[List[Union[HealthPlanFormulary, str]], Union[HealthPlanFormulary, str]]] = Field(
        None,
        description="Formularies covered by this plan.",
    )
    

HealthInsurancePlan.update_forward_refs()
