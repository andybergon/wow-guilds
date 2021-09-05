# https://develop.battle.net/documentation/world-of-warcraft/profile-apis
from datetime import datetime

from blizzardapi.wow.wow_profile_api import WowProfileApi as ProfileApi
from raiderio import RaiderIO

import blizzard_creds
import defaults

REPUTATION_FACTION_ID = 2472  # The Archivists' Codex
ACHIEVEMENT_ID = 15069  # The Archivists' Codex

rio = RaiderIO()
profile_api = ProfileApi(client_id=blizzard_creds.CLIENT_ID, client_secret=blizzard_creds.CLIENT_SECRET)


def get_roster(region=defaults.REGION, realm=defaults.REALM, guild=defaults.GUILD):
    with rio:
        rio.get_guild_roster(region=region, realm=realm, guild=guild)


def get_rep(character_name='Berga', realm=defaults.REALM):
    """
    Note: Retrieves all reps
    :return: {'raw': 41000, 'value': 0, 'max': 0, 'tier': 5, 'name': 'Tier 6'}
    """
    reps = profile_api.get_character_reputations_summary(
        region=defaults.REGION,
        locale=defaults.LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    rep = list(filter(lambda r: r.get('faction').get('id') == REPUTATION_FACTION_ID, reps.get('reputations')))[0] \
        .get('standing')

    return rep


def get_achi_datetime(character_name='Berga', realm=defaults.REALM):
    """
    Note: Retrieves all achievements
    """
    achis = profile_api.get_character_achievements_summary(
        region=defaults.REGION,
        locale=defaults.LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    achi = list(filter(lambda a: a.get('id') == ACHIEVEMENT_ID, achis.get('achievements')))[0]

    ts_millis = achi.get('completed_timestamp')

    return datetime.fromtimestamp(ts_millis//1000)


def main():
    # get_roster()
    # rep = get_rep()
    # print(f'{rep=}')
    achi = get_achi_datetime()
    print(f'{achi.isoformat()}')


if __name__ == '__main__':
    main()
