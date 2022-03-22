import string
from dataclasses import dataclass


@dataclass
class GuildCoordinates:
    region: string
    realm: string
    guild: string
