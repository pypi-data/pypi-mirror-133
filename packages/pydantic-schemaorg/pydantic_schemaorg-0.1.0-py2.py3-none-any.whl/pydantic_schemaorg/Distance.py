from pydantic import Field
from pydantic_schemaorg.Quantity import Quantity


class Distance(Quantity):
    """Properties that take Distances as values are of the form '&lt;Number&gt; &lt;Length"
     "unit of measure&gt;'. E.g., '7 ft'.

    See https://schema.org/Distance.

    """
    type_: str = Field("Distance", const=True, alias='@type')
    

Distance.update_forward_refs()
