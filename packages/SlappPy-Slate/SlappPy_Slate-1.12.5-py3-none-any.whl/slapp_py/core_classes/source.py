import logging
from datetime import datetime, timedelta
from typing import Union, List, Optional
from uuid import UUID, uuid4

from slapp_py.core_classes.bracket import Bracket
from slapp_py.core_classes.player import Player
from slapp_py.core_classes.team import Team
from slapp_py.helpers.dict_helper import to_list, from_list, deserialize_uuids

UNKNOWN_SOURCE = "(Unnamed Source)"
"""Displayed string for an unknown source."""

UNKNOWN_DATE_TIME = datetime.utcfromtimestamp(0)
"""The unknown datetime (epoch)"""


class Source:
    def __init__(self,
                 name: Optional[str] = None,
                 brackets: Optional[List[Bracket]] = None,
                 players: Optional[List[Player]] = None,
                 teams: Optional[List[Team]] = None,
                 uris: Optional[List[str]] = None,
                 start: Optional[datetime] = None,
                 guid: Union[None, str, UUID] = None
                 ):
        self.brackets: List[Bracket] = brackets or []
        self.name: str = name or UNKNOWN_SOURCE
        self.players: List[Player] = players or []
        self.teams: List[Team] = teams or []
        self.uris: List[str] = uris or []
        self.start: datetime = start or UNKNOWN_DATE_TIME

        if isinstance(guid, str):
            guid = UUID(guid)
        self.guid = guid or uuid4()

    def __str__(self):
        return self.name

    @property
    def tournament_id(self) -> str:
        """Get the tournament id from the source name. This substrings past the last -."""
        # rpartition finds the last '-', we want the substring past that to the end which is [2].
        return self.name.rpartition('-')[2]

    @staticmethod
    def deserialize_source_uuids(info: dict, key: Optional[str] = "S") -> List[UUID]:
        return deserialize_uuids(info, key, [(Source, lambda s: s.guid)])

    @staticmethod
    def from_dict(obj: dict) -> 'Source':
        assert isinstance(obj, dict)
        try:
            return Source(
                guid=UUID(obj.get("Id")),
                name=obj.get("Name", UNKNOWN_SOURCE),
                brackets=from_list(lambda x: Bracket.from_dict(x), obj.get("Brackets")),
                players=from_list(lambda x: Player.from_dict(x), obj.get("Players")),
                teams=from_list(lambda x: Team.from_dict(x), obj.get("Teams")),
                uris=from_list(lambda x: str(x), obj.get("Uris")),
                start=Source.cs_ticks_to_datetime(obj["Start"]) if "Start" in obj else UNKNOWN_DATE_TIME,
            )
        except Exception as e:
            logging.exception(exc_info=e, msg=f"Exception occurred loading Source with id {obj.get('Id', '(Unknown)')}: {e}, {e.args}")
            raise e

    def to_dict(self) -> dict:
        result = {"Id": self.guid.__str__(), "Name": self.name}
        if len(self.brackets) > 0:
            result["Brackets"] = to_list(lambda x: Bracket.to_dict(x), self.brackets)
        if len(self.players) > 0:
            result["Players"] = to_list(lambda x: Player.to_dict(x), self.players)
        if len(self.teams) > 0:
            result["Teams"] = to_list(lambda x: Team.to_dict(x), self.teams)
        if len(self.uris) > 0:
            result["Uris"] = self.uris
        if self.start != UNKNOWN_DATE_TIME:
            result["Start"] = Source.datetime_to_ticks(self.start)
        return result

    @staticmethod
    def cs_ticks_to_datetime(ticks) -> datetime:
        return datetime(1, 1, 1) + timedelta(microseconds=ticks/10)

    @staticmethod
    def datetime_to_ticks(dt: datetime) -> int:
        return int((dt - datetime(1, 1, 1)).total_seconds() * 10000000)
