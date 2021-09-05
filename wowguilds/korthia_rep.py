import json
from datetime import datetime

from blizzardapi.wow.wow_profile_api import WowProfileApi as ProfileApi

import blizzard_creds
import defaults
from roster import get_roster

FILENAME = 'data/korthia.json'

REPUTATION_FACTION_ID = 2472  # The Archivists' Codex
ACHIEVEMENT_ID = 15069  # The Archivists' Codex

profile_api = ProfileApi(client_id=blizzard_creds.CLIENT_ID, client_secret=blizzard_creds.CLIENT_SECRET)


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

    achis = list(filter(lambda a: a.get('id') == ACHIEVEMENT_ID, achis.get('achievements')))

    if not achis:
        return None

    ts_millis = achis[0].get('completed_timestamp')

    return datetime.fromtimestamp(ts_millis // 1000)


def get_roster_reps():
    roster = get_roster()
    for r in roster:
        name = r.get('name')
        rep = get_rep(name)
        r['rep'] = rep

        dt = get_achi_datetime(name)
        if dt:
            r['rep_date'] = dt.isoformat()

    return roster


def main():
    # members = get_roster_reps()
    # write_to_file(members)
    members = read_from_file()
    print_members(members)


def write_to_file(members):
    with open(FILENAME, 'w+') as f:
        json.dump(members, f, indent=4)


def read_from_file():
    with open(FILENAME) as f:
        return json.load(f)


def print_members(members):
    print(f'{len(members)=}')
    members = sorted(members,
                     key=sort_by_rep,
                     reverse=True)

    from pprint import pprint
    # pprint(members, sort_dicts=False)

    for m in members:
        print(f'{m["name"]} - {m["rep"]["raw"]} - {m.get("rep_date", None)}')


def sort_by_rep(m):
    achi_date = m.get('rep_date')

    if achi_date:
        rev_achi_time = datetime.max - datetime.fromisoformat(achi_date)
    else:
        rev_achi_time = datetime.min

    return m.get('rep').get('raw'), rev_achi_time


if __name__ == '__main__':
    main()
