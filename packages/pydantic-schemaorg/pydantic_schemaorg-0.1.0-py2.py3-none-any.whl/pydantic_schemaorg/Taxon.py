from pydantic import AnyUrl, Field
from pydantic_schemaorg.DefinedTerm import DefinedTerm
from typing import List, Optional, Union
from pydantic_schemaorg.PropertyValue import PropertyValue
from pydantic_schemaorg.Thing import Thing


class Taxon(Thing):
    """A set of organisms asserted to represent a natural cohesive biological unit.

    See https://schema.org/Taxon.

    """
    type_: str = Field("Taxon", const=True, alias='@type')
    hasDefinedTerm: Optional[Union[List[Union[DefinedTerm, str]], Union[DefinedTerm, str]]] = Field(
        None,
        description="A Defined Term contained in this term set.",
    )
    childTaxon: Optional[Union[List[Union[AnyUrl, str, 'Taxon']], Union[AnyUrl, str, 'Taxon']]] = Field(
        None,
        description="Closest child taxa of the taxon in question.",
    )
    parentTaxon: Optional[Union[List[Union[AnyUrl, str, 'Taxon']], Union[AnyUrl, str, 'Taxon']]] = Field(
        None,
        description="Closest parent taxon of the taxon in question.",
    )
    taxonRank: Optional[Union[List[Union[AnyUrl, str, PropertyValue]], Union[AnyUrl, str, PropertyValue]]] = Field(
        None,
        description="The taxonomic rank of this taxon given preferably as a URI from a controlled vocabulary"
     "– (typically the ranks from TDWG TaxonRank ontology or equivalent Wikidata URIs).",
    )
    

Taxon.update_forward_refs()
