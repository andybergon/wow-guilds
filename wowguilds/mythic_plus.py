from raiderio import RaiderIO

from constants import ALL_FACTIONS, DEFAULT_GUILD, DEFAULT_REALM, DEFAULT_REGION, MYTHIC_DIFFICULTY, SOD_RAID


# TODO: OTS has 2800-2700: 1, 2700-2600: 3
# https://raider.io/guilds/eu/nemesis/One%20Tier%20Stand/roster#mode=all

def main():
    # get_guilds_m_buckets()
    print(get_m_scores_buckets('One Tier Stand'))


def get_guilds_m_buckets():
    guilds = get_guilds()
    for guild in guilds:
        buckets = get_m_scores_buckets(guild)
        count = sum({k: v for k, v in buckets.items() if k != '2000-0'}.values())
        print(f'{guild} ({count}) -> {buckets}')


def get_guilds(raid=SOD_RAID, difficulty=MYTHIC_DIFFICULTY,
               region=DEFAULT_REGION, realm=DEFAULT_REALM, factions=ALL_FACTIONS):
    with RaiderIO() as rio:
        rankings = rio.get_raid_instance_ranking(raid, difficulty, region, realm, factions)
        guilds = [g.get('guild').get('name') for g in rankings.get('raidRankings').get('rankedGuilds')]
        return guilds


def get_m_scores_buckets(guild):
    scores = get_m_scores(guild)
    return bucket_scores(scores)


def bucket_scores(scores):
    count = len(scores)
    # print(f'{count=}')
    step = 100
    maximum = int(max(scores))
    bins = range(2000, maximum, step)
    # TODO: fix, maybe without numpy
    # histogram = np.histogram(scores, bins)  # ([4,7,6], [2000,2100,2200])
    histogram = []
    # print(f'{histogram=}')
    buckets = {f'{histogram[1][i[0]] + step}-{histogram[1][i[0]]}': histogram[0][i[0]] for i in
               enumerate(histogram[0])}  # {"2000": 12, "2100": 10}
    # print(f'{buckets=}')
    buckets = dict(sorted(buckets.items(), reverse=True))
    # print(f'{buckets=}')
    more_two_thousand = sum(buckets.values())
    buckets = {**buckets, '2000-0': count - more_two_thousand}
    # print(f'{buckets=}')
    return buckets


def get_m_scores(guild=DEFAULT_GUILD):
    with RaiderIO() as rio:
        roster = rio.get_guild_roster(DEFAULT_REGION, DEFAULT_REALM, guild)
        roster_list = roster.get('guildRoster').get('roster')
        scores = list(sorted(filter(lambda s: s != 0, [r.get('keystoneScores').get('allScore') for r in roster_list]),
                             reverse=True))
        return scores


if __name__ == '__main__':
    main()
