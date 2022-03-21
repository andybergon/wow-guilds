import unittest

from wowguilds.legendary.items import LegendaryBaseItem
from wowguilds.legendary.legendary_rank import LegendaryRank


class TestItems(unittest.TestCase):
    def test_leg_item(self):
        lbi = LegendaryBaseItem('Umbrahide Leggins', 123, LegendaryRank.RANK_7)
        print(lbi)


if __name__ == '__main__':
    unittest.main()
