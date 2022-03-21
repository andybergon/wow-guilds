from dataclasses import dataclass

from wowguilds.legendary.legendary_rank import LegendaryRank


@dataclass
class Item:
    name: str
    id: int


@dataclass
class LegendaryBaseItem(Item):
    rank: LegendaryRank