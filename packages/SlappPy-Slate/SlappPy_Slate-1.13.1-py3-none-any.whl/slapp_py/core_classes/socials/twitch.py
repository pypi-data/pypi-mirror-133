from typing import Optional, Union, List
from uuid import UUID

from slapp_py.core_classes.socials.social import Social

TWITCH_BASE_ADDRESS = "twitch.tv"


class Twitch(Social):
    def __init__(self,
                 handle: Optional[str] = None,
                 sources: Union[None, UUID, List[UUID]] = None):
        super().__init__(
            value=handle,
            sources=sources,
            social_base_address=TWITCH_BASE_ADDRESS
        )

    @staticmethod
    def from_dict(obj: dict) -> 'Twitch':
        assert isinstance(obj, dict)
        social = Social._from_dict(obj, TWITCH_BASE_ADDRESS)
        return Twitch(social.handle, social.sources)
