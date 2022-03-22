from dataclasses import dataclass

from wowguilds.legendary.legendary_rank import LegendaryRank


@dataclass
class Item:
    name: str
    id: int


@dataclass
class LegendaryBaseItem(Item):
    rank: LegendaryRank


SPECTRAL_FLASK_OF_POWER = Item('Spectral Flask of Power', 171276)
