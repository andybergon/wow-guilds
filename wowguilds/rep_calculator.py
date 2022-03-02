import json
from datetime import datetime

from blizzardapi.wow.wow_profile_api import WowProfileApi as ProfileApi

import blizzard_creds
import constants
from roster import get_roster
from wowguilds.constants import ARCHIVISTS_ACHIEVEMENT_ID

profile_api = ProfileApi(client_id=blizzard_creds.CLIENT_ID, client_secret=blizzard_creds.CLIENT_SECRET)


def get_rep(character_name='Berga', realm=constants.DEFAULT_REALM, faction_id=constants.ENLIGHTENED_FACTION_ID):
    """
    Note: Retrieves all reps
    :return: {'raw': 41000, 'value': 0, 'max': 0, 'tier': 5, 'name': 'Tier 6'}
    """
    reps = profile_api.get_character_reputations_summary(
        region=constants.DEFAULT_REGION,
        locale=constants.LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    reps = list(filter(lambda r: r.get('faction').get('id') == faction_id, reps.get('reputations')))
    if reps:
        return reps[0].get('standing')
    else:
        return None


def get_achi_datetime(character_name='Berga', realm=constants.DEFAULT_REALM, achievement_id=ARCHIVISTS_ACHIEVEMENT_ID):
    """
    Note: Retrieves all achievements
    """
    achis = profile_api.get_character_achievements_summary(
        region=constants.DEFAULT_REGION,
        locale=constants.LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    achis = list(filter(lambda a: a.get('id') == achievement_id, achis.get('achievements')))

    if not achis:
        return None

    ts_millis = achis[0].get('completed_timestamp')

    return datetime.fromtimestamp(ts_millis // 1000)


def get_roster_reps(faction_id, achi_id, exclude_no_myth_raid=False, exclude_no_m_plus=False):
    roster = get_roster(exclude_no_myth_raid=exclude_no_myth_raid, exclude_no_m_plus=exclude_no_m_plus)
    rep_roster = []
    i = 1
    for r in roster:
        name = r.get('name')
        print(f'Processing: {name} ({i}/{len(roster)})')
        i += 1

        rep = get_rep(name, faction_id=faction_id)
        if rep:
            r['rep'] = rep
        else:
            continue

        if achi_id:
            dt = get_achi_datetime(name)
            if dt:
                r['rep_date'] = dt.isoformat()

        rep_roster.append(r)

    return rep_roster


def write_to_file(members, filename):
    with open(filename, 'w+') as f:
        json.dump(members, f, indent=4)


def read_from_file(filename):
    with open(filename) as f:
        return json.load(f)


def print_members(members):
    print(f'{len(members)=}')
    members = sorted(members,
                     key=sort_by_rep,
                     reverse=True)

    # pprint(members, sort_dicts=False)

    for m in members:
        rep = m["rep"]
        print(f'{m["name"]} - {rep["raw"]} - {rep.get("value")}/{rep.get("max")} - {m.get("rep_date", None)}')


def sort_by_rep(m):
    achi_date = m.get('rep_date')

    if achi_date:
        rev_achi_time = datetime.max - datetime.fromisoformat(achi_date)
    else:
        rev_achi_time = datetime.min

    return m.get('rep').get('raw'), rev_achi_time


def main(faction=constants.Faction.ENLIGHTENED, retrieve=True):
    filename = f'data/{faction.name.lower()}.json'
    if retrieve:
        members = get_roster_reps(*constants.faction_to_ids[faction])
        write_to_file(members, filename)
    members = read_from_file(filename)
    print_members(members)


if __name__ == '__main__':
    main(faction=constants.Faction.ENLIGHTENED, retrieve=False)
