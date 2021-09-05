from raiderio import RaiderIO

import defaults

rio = RaiderIO()


def get_roster(region=defaults.REGION, realm=defaults.REALM, guild=defaults.GUILD,
               exclude_no_raid=True, exclude_no_m_plus=True):
    with rio:
        roster = rio.get_guild_roster(
            region=region,
            realm=realm,
            guild=guild
        )

    roster_list = roster.get('guildRoster').get('roster')
    roster = list(map(lambda r: to_simple_roster_member(r), roster_list))

    if exclude_no_raid:
        roster = list(filter(lambda r: has_myth_raid(r), roster))

    if exclude_no_m_plus:
        roster = list(filter(lambda r: r.get('m+') > 0, roster))

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
