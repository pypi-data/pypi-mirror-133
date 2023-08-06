from pydantic import AnyUrl, Field
from pydantic_schemaorg.CreativeWork import CreativeWork
from typing import List, Optional, Union
from pydantic_schemaorg.AboutPage import AboutPage
from pydantic_schemaorg.Article import Article
from pydantic_schemaorg.Organization import Organization


class NewsMediaOrganization(Organization):
    """A News/Media organization such as a newspaper or TV station.

    See https://schema.org/NewsMediaOrganization.

    """
    type_: str = Field("NewsMediaOrganization", const=True, alias='@type')
    actionableFeedbackPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
     "about public engagement activities (for news media, the newsroom’s), including involving"
     "the public - digitally or otherwise -- in coverage decisions, reporting and activities"
     "after publication.",
    )
    diversityPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]."
     "For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity"
     "policy on both staffing and sources, typically providing staffing data.",
    )
    ethicsPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="Statement about ethics policy, e.g. of a [[NewsMediaOrganization]] regarding journalistic"
     "and publishing practices, or of a [[Restaurant]], a page describing food source policies."
     "In the case of a [[NewsMediaOrganization]], an ethicsPolicy is typically a statement"
     "describing the personal, organizational, and corporate standards of behavior expected"
     "by the organization.",
    )
    correctionsPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For an [[Organization]] (e.g. [[NewsMediaOrganization]]), a statement describing"
     "(in news media, the newsroom’s) disclosure and correction policy for errors.",
    )
    missionCoveragePrioritiesPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For a [[NewsMediaOrganization]], a statement on coverage priorities, including any"
     "public agenda or stance on issues.",
    )
    ownershipFundingInfo: Optional[Union[List[Union[AnyUrl, str, CreativeWork, AboutPage]], Union[AnyUrl, str, CreativeWork, AboutPage]]] = Field(
        None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
     "a description of organizational ownership structure; funding and grants. In a news/media"
     "setting, this is with particular reference to editorial independence. Note that the"
     "[[funder]] is also available and can be used to make basic funder information machine-readable.",
    )
    noBylinesPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
     "explaining when authors of articles are not named in bylines.",
    )
    verificationFactCheckingPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="Disclosure about verification and fact-checking processes for a [[NewsMediaOrganization]]"
     "or other fact-checking [[Organization]].",
    )
    diversityStaffingReport: Optional[Union[List[Union[AnyUrl, Article, str]], Union[AnyUrl, Article, str]]] = Field(
        None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
     "a report on staffing diversity issues. In a news context this might be for example ASNE"
     "or RTDNA (US) reports, or self-reported.",
    )
    unnamedSourcesPolicy: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about"
     "policy on use of unnamed sources and the decision process required.",
    )
    masthead: Optional[Union[List[Union[AnyUrl, CreativeWork, str]], Union[AnyUrl, CreativeWork, str]]] = Field(
        None,
        description="For a [[NewsMediaOrganization]], a link to the masthead page or a page listing top editorial"
     "management.",
    )
    

NewsMediaOrganization.update_forward_refs()
