from pydantic import AnyUrl, Field
from pydantic_schemaorg.Person import Person
from typing import List, Optional, Union
from pydantic_schemaorg.VideoObject import VideoObject
from pydantic_schemaorg.Thing import Thing
from pydantic_schemaorg.GamePlayMode import GamePlayMode
from pydantic_schemaorg.CreativeWork import CreativeWork
from pydantic_schemaorg.GameServer import GameServer
from pydantic_schemaorg.MusicGroup import MusicGroup
from pydantic_schemaorg.SoftwareApplication import SoftwareApplication
from pydantic_schemaorg.Game import Game


class VideoGame(SoftwareApplication, Game):
    """A video game is an electronic game that involves human interaction with a user interface"
     "to generate visual feedback on a video device.

    See https://schema.org/VideoGame.

    """
    type_: str = Field("VideoGame", const=True, alias='@type')
    actors: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="An actor, e.g. in tv, radio, movie, video games etc. Actors can be associated with individual"
     "items or with a series, episode, clip.",
    )
    trailer: Optional[Union[List[Union[VideoObject, str]], Union[VideoObject, str]]] = Field(
        None,
        description="The trailer of a movie or tv/radio series, season, episode, etc.",
    )
    director: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="A director of e.g. tv, radio, movie, video gaming etc. content, or of an event. Directors"
     "can be associated with individual items or with a series, episode, clip.",
    )
    gamePlatform: Optional[Union[List[Union[AnyUrl, str, Thing]], Union[AnyUrl, str, Thing]]] = Field(
        None,
        description="The electronic systems used to play <a href=\"http://en.wikipedia.org/wiki/Category:Video_game_platforms\">video"
     "games</a>.",
    )
    playMode: Optional[Union[List[Union[GamePlayMode, str]], Union[GamePlayMode, str]]] = Field(
        None,
        description="Indicates whether this game is multi-player, co-op or single-player. The game can be"
     "marked as multi-player, co-op and single-player at the same time.",
    )
    cheatCode: Optional[Union[List[Union[CreativeWork, str]], Union[CreativeWork, str]]] = Field(
        None,
        description="Cheat codes to the game.",
    )
    actor: Optional[Union[List[Union[Person, str]], Union[Person, str]]] = Field(
        None,
        description="An actor, e.g. in tv, radio, movie, video games etc., or in an event. Actors can be associated"
     "with individual items or with a series, episode, clip.",
    )
    gameTip: Optional[Union[List[Union[CreativeWork, str]], Union[CreativeWork, str]]] = Field(
        None,
        description="Links to tips, tactics, etc.",
    )
    gameServer: Optional[Union[List[Union[GameServer, str]], Union[GameServer, str]]] = Field(
        None,
        description="The server on which it is possible to play the game.",
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
    

VideoGame.update_forward_refs()
