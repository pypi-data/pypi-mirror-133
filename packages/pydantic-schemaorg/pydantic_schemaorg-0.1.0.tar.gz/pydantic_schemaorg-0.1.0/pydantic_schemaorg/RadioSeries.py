from pydantic import AnyUrl, Field
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Union
from pydantic_schemaorg.CreativeWorkSeason import CreativeWorkSeason
from pydantic_schemaorg.VideoObject import VideoObject
from pydantic_schemaorg.Episode import Episode
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.MusicGroup import MusicGroup
from pydantic_schemaorg.CreativeWorkSeries import CreativeWorkSeries


class RadioSeries(CreativeWorkSeries):
    """CreativeWorkSeries dedicated to radio broadcast and associated online delivery.

    See https://schema.org/RadioSeries.

    """
    type_: str = Field("RadioSeries", const=True, alias='@type')
    actors: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="An actor, e.g. in tv, radio, movie, video games etc. Actors can be associated with individual"
     "items or with a series, episode, clip.",
    )
    containsSeason: Optional[Union[List[Union[CreativeWorkSeason, str]], Union[CreativeWorkSeason, str]]] = Field(
        None,
        description="A season that is part of the media series.",
    )
    numberOfSeasons: Optional[Union[List[Union[int, str]], Union[int, str]]] = Field(
        None,
        description="The number of seasons in this series.",
    )
    trailer: Optional[Union[List[Union[VideoObject, str]], Union[VideoObject, str]]] = Field(
        None,
        description="The trailer of a movie or tv/radio series, season, episode, etc.",
    )
    episodes: Optional[Union[List[Union[Episode, str]], Union[Episode, str]]] = Field(
        None,
        description="An episode of a TV/radio series or season.",
    )
    numberOfEpisodes: Optional[Union[List[Union[int, str]], Union[int, str]]] = Field(
        None,
        description="The number of episodes in this season or series.",
    )
    director: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="A director of e.g. tv, radio, movie, video gaming etc. content, or of an event. Directors"
     "can be associated with individual items or with a series, episode, clip.",
    )
    productionCompany: Optional[Union[List[Union[Organization, str]], Union[Organization, str]]] = Field(
        None,
        description="The production company or studio responsible for the item e.g. series, video game, episode"
     "etc.",
    )
    seasons: Optional[Union[List[Union[CreativeWorkSeason, str]], Union[CreativeWorkSeason, str]]] = Field(
        None,
        description="A season in a media series.",
    )
    season: Optional[Union[List[Union[AnyUrl, CreativeWorkSeason, str]], Union[AnyUrl, CreativeWorkSeason, str]]] = Field(
        None,
        description="A season in a media series.",
    )
    actor: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="An actor, e.g. in tv, radio, movie, video games etc., or in an event. Actors can be associated"
     "with individual items or with a series, episode, clip.",
    )
    episode: Optional[Union[List[Union[Episode, str]], Union[Episode, str]]] = Field(
        None,
        description="An episode of a tv, radio or game media within a series or season.",
    )
    directors: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="A director of e.g. tv, radio, movie, video games etc. content. Directors can be associated"
     "with individual items or with a series, episode, clip.",
    )
    musicBy: Optional[Union[List[Union[MusicGroup, Person, str]], Union[MusicGroup, Person, str]]] = Field(
        None,
        description="The composer of the soundtrack.",
    )
    

RadioSeries.update_forward_refs()
