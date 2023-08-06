import logging
from typing import Optional, List, Union
from uuid import UUID, uuid4

from slapp_py.core_classes.battlefy import Battlefy
from slapp_py.core_classes.discord import Discord
from slapp_py.core_classes.friend_code import FriendCode
from slapp_py.core_classes.name import Name
from slapp_py.core_classes.skill import Skill
from slapp_py.core_classes.socials.plus_membership import PlusMembership
from slapp_py.core_classes.socials.sendou import Sendou
from slapp_py.core_classes.socials.twitch import Twitch
from slapp_py.core_classes.socials.twitter import Twitter
from slapp_py.helpers.dict_helper import from_list, to_list, deserialize_uuids, serialize_uuids


class Player:
    _COUNTRY_FLAG_OFFSET = 0x1F1A5
    """This is the result of '🇦' - 'A'"""

    battlefy: Battlefy
    """Back-store for player's Battlefy information."""

    country: Optional[str]
    """Back-store for player's Country information."""

    discord: Discord
    """Back-store for player's Discord information."""

    friend_codes: List[FriendCode]
    """Back-store for player's FCs."""

    names: List[Name]
    """Back-store for the names of this player. The first element is the current name."""

    plus_membership: List[PlusMembership]
    """Back-store for the PlusMembership Profiles of this player."""

    skill: Skill
    """This player's calculated TrueSkill values"""

    sendou_profiles: List[Sendou]
    """Back-store for the Sendou Profiles of this player."""

    teams: List[UUID]
    """Back-store for the team GUIDs for this player. The first element is the current team.
    No team represented by Team.NoTeam.Id."""

    top500: bool
    """Back-store for player's top 500 flag."""

    twitch_profiles: List[Twitch]
    """Back-store for the Twitch Profiles of this player."""

    twitter_profiles: List[Twitter]
    """Back-store for the Twitter Profiles of this player."""

    weapons: List[str]
    """Back-store for the weapons that the player uses (if any)."""

    guid: UUID
    """The GUID of the player."""

    def __init__(self,
                 names: Union[None, Name, List[Name], str, List[str]] = None,
                 teams: Union[None, UUID, List[UUID]] = None,
                 battlefy: Optional[Battlefy] = None,
                 discord: Optional[Discord] = None,
                 friend_codes: Optional[List[FriendCode]] = None,
                 skill: Optional[Skill] = None,
                 plus_membership: Optional[List[PlusMembership]] = None,
                 sendou_profiles: Optional[List[Sendou]] = None,
                 twitch_profiles: Optional[List[Twitch]] = None,
                 twitter_profiles: Optional[List[Twitter]] = None,
                 weapons: Optional[List[str]] = None,
                 country: Optional[str] = None,
                 top500: bool = False,
                 guid: Union[None, str, UUID] = None):
        # When adding params please update filter_to_source

        if not isinstance(names, list):
            names = [names]

        self.names = []
        for i in range(0, len(names)):
            if isinstance(names[i], str):
                if not any(n == names[i] for n in self.names):
                    self.names.append(Name(names[i], None))
            elif isinstance(names[i], Name):
                if not any(n == names[i].value for n in self.names):
                    self.names.append(names[i])
            else:
                logging.error(f"player: Can't handle {names[i]} -- expected Name or str. Ignoring.")

        if not teams:
            self.teams = []
        else:
            if not isinstance(teams, list):
                teams = [teams]

            self.teams = []
            for i in range(0, len(teams)):
                assert isinstance(teams[i], UUID)
                self.teams.append(teams[i])

        self.battlefy = battlefy or Battlefy()
        self.discord = discord or Discord()
        self.friend_codes = friend_codes or []
        self.skill = skill or Skill()
        self.plus_membership = plus_membership or []
        self.sendou_profiles = sendou_profiles or []
        self.twitter_profiles = twitter_profiles or []
        self.twitch_profiles = twitch_profiles or []
        self.weapons = weapons or []
        self.country = country.upper() if country and len(country) == 2 else None
        self.top500 = top500

        if isinstance(guid, str):
            guid = UUID(guid)
        self.guid = guid or uuid4()

    @property
    def name(self) -> Name:
        """The last known used name for the Player or UnknownPlayerName."""
        from slapp_py.core_classes.builtins import UnknownPlayerName
        return self.names[0] if len(self.names) > 0 else UnknownPlayerName

    @property
    def country_flag(self) -> Optional[str]:
        """Country information as a flag. May be None."""
        if not self.country:
            return None

        return chr(ord(self.country[0]) + Player._COUNTRY_FLAG_OFFSET) + \
            chr(ord(self.country[1]) + Player._COUNTRY_FLAG_OFFSET)

    @property
    def latest_plus_membership(self) -> Optional[PlusMembership]:
        """Order PlusMembership by date, get the last (most recent) or None"""
        return (sorted(self.plus_membership, key=lambda pm: pm.date)[-1]) if self.plus_membership else None

    def filter_to_source(self, source_id: Union[str, UUID]) -> 'Player':
        """Filter this Player instance down to the components made by a source id."""
        search_uuid = source_id if isinstance(source_id, UUID) else UUID(source_id)
        return Player(
            names=[name for name in self.names if search_uuid in name.sources],
            teams=self.teams,  # TODO - teams don't have associated Sources at this level. Needs adding.
            battlefy=self.battlefy.filter_to_source(source_id),
            discord=self.discord.filter_to_source(source_id),
            friend_codes=self.friend_codes,  # TODO - FCs don't have associated Sources at this level. Needs adding.
            skill=None,
            plus_membership=[name for name in self.plus_membership if search_uuid in name.sources],
            sendou_profiles=[name for name in self.sendou_profiles if search_uuid in name.sources],
            twitch_profiles=[name for name in self.twitch_profiles if search_uuid in name.sources],
            twitter_profiles=[name for name in self.twitter_profiles if search_uuid in name.sources],
            weapons=None,
            country=self.country,
            top500=self.top500,
            guid=self.guid)

    @property
    def sources(self):
        return \
            list(
                sorted(
                    set(
                        sum([x.sources for x in self.names]
                            + [x.sources for x in self.plus_membership]
                            + [x.sources for x in self.sendou_profiles]
                            + [x.sources for x in self.twitch_profiles]
                            + [x.sources for x in self.twitter_profiles]
                            + [x.sources for x in self.battlefy.persistent_ids]
                            + [x.sources for x in self.battlefy.slugs]
                            + [x.sources for x in self.battlefy.usernames]
                            + [x.sources for x in self.discord.ids]
                            + [x.sources for x in self.discord.usernames], [])
                    ),
                    reverse=True
                )
            )

    @staticmethod
    def from_dict(obj: dict) -> 'Player':
        assert isinstance(obj, dict)
        return Player(
            battlefy=Battlefy.from_dict(obj.get("Battlefy")) if "Battlefy" in obj else None,
            discord=Discord.from_dict(obj.get("Discord")) if "Discord" in obj else None,
            friend_codes=from_list(lambda x: FriendCode.from_dict(x), obj.get("FCs")),
            names=from_list(lambda x: Name.from_dict(x), obj.get("N")),
            plus_membership=from_list(lambda x: PlusMembership.from_dict(x), obj.get("Plus")),
            sendou_profiles=from_list(lambda x: Sendou.from_dict(x), obj.get("Sendou")),
            skill=Skill.from_dict(obj.get("Skill")) if "Skill" in obj else Skill(),
            teams=deserialize_uuids(obj, "Teams"),
            twitch_profiles=from_list(lambda x: Twitch.from_dict(x), obj.get("Twitch")),
            twitter_profiles=from_list(lambda x: Twitter.from_dict(x), obj.get("Twitter")),
            weapons=from_list(lambda x: str(x), obj.get("Weapons")),
            country=obj.get("Country", None),
            top500=obj.get("Top500", False),
            guid=UUID(obj.get("Id"))
        )

    def to_dict(self) -> dict:
        result = {}
        if len(self.battlefy.slugs) > 0 or len(self.battlefy.usernames) > 0:
            result["Battlefy"] = self.battlefy.to_dict()
        if self.country:
            result["Country"] = self.country
        if len(self.discord.ids) > 0 or len(self.discord.usernames) > 0:
            result["Discord"] = self.discord.to_dict()
        if len(self.friend_codes) > 0:
            result["FCs"] = to_list(lambda x: FriendCode.to_dict(x), self.friend_codes)
        result["Id"] = self.guid.__str__()
        if len(self.names) > 0:
            result["N"] = to_list(lambda x: Name.to_dict(x), self.names)
        if len(self.plus_membership) > 0:
            result["Plus"] = to_list(lambda x: PlusMembership.to_dict(x), self.plus_membership)
        if len(self.sendou_profiles) > 0:
            result["Sendou"] = to_list(lambda x: Sendou.to_dict(x), self.sendou_profiles)
        if not self.skill.is_default:
            result["Skill"] = self.skill.to_dict(),
        if len(self.teams) > 0:
            result["Teams"] = serialize_uuids(self.teams)
        if self.top500:
            result["Top500"] = self.top500
        if len(self.twitch_profiles) > 0:
            result["Twitch"] = to_list(lambda x: Twitch.to_dict(x), self.twitch_profiles)
        if len(self.twitter_profiles) > 0:
            result["Twitter"] = to_list(lambda x: Twitter.to_dict(x), self.twitter_profiles)
        if len(self.weapons) > 0:
            result["Weapons"] = to_list(lambda x: str(x), self.weapons)
        return result

    @staticmethod
    def soft_merge_from_multiple(*players: 'Player'):
        if not players:
            return None

        if len(players) == 1:
            return players[0]

        result = players[0]
        for player in players[1:]:
            result.teams.extend(player.teams)
            result.teams = list(set(result.teams))

            result.names.extend(player.names)
            result.names = list(set(result.names))

            result.weapons.extend(player.weapons)
            result.weapons = list(set(result.weapons))

            result.battlefy.slugs.extend(player.battlefy.slugs)
            result.battlefy.slugs = list(set(result.battlefy.slugs))

            result.battlefy.usernames.extend(player.battlefy.usernames)
            result.battlefy.usernames = list(set(result.battlefy.usernames))

            result.battlefy.persistent_ids.extend(player.battlefy.persistent_ids)
            result.battlefy.persistent_ids = list(set(result.battlefy.persistent_ids))

            result.discord.ids.extend(player.discord.ids)
            result.discord.ids = list(set(result.discord.ids))

            result.discord.usernames.extend(player.discord.usernames)
            result.discord.usernames = list(set(result.discord.usernames))

            result.plus_membership.extend(player.plus_membership)
            result.plus_membership = list(set(result.plus_membership))

            result.sendou_profiles.extend(player.sendou_profiles)
            result.sendou_profiles = list(set(result.sendou_profiles))

            result.twitch_profiles.extend(player.twitch_profiles)
            result.twitch_profiles = list(set(result.twitch_profiles))

            result.twitter_profiles.extend(player.twitter_profiles)
            result.twitter_profiles = list(set(result.twitter_profiles))

            result.friend_codes.extend(player.friend_codes)
            result.friend_codes = list(set(result.friend_codes))

            if player.country and result.country != player.country:
                result.country = player.country

            if player.top500:
                result.top500 = True
