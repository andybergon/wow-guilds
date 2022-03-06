from raiderio import RaiderIO

rio = RaiderIO()


def get_roster(guild_coordinates, exclude_no_myth_raid=True, exclude_no_m_plus=True):
    with rio:
        roster = rio.get_guild_roster(
            region=guild_coordinates.get('region'),
            realm=guild_coordinates.get('realm'),
            guild=guild_coordinates.get('guild')
        )

    roster = roster.get('guildRoster').get('roster')
    roster = list(filter(lambda m: m.get('character').get('level') == 60, roster))

    roster = list(map(lambda m: to_simple_roster_member(m), roster))

    if exclude_no_myth_raid:
        roster = list(filter(lambda m: has_myth_raid(m), roster))

    if exclude_no_m_plus:
        roster = list(filter(lambda m: m.get('m+') > 0, roster))

    return roster


def has_hc_or_myth_raid(r):
    raid = r.get('raid')
    hc_num = raid.get('heroic')
    myth_num = raid.get('mythic')

    return hc_num + myth_num > 0


def has_myth_raid(r):
    raid = r.get('raid')
    myth_num = raid.get('mythic')

    return myth_num > 0


def to_simple_roster_member(r):
    return {
        "name": r.get('character').get('name'),
        "raid": r.get('raidProgress').get('progress'),
        "m+": r.get('keystoneScores').get('allScore')
    }
