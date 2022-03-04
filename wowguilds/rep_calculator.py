import json
from datetime import datetime

from blizzardapi.wow.wow_profile_api import WowProfileApi as ProfileApi
from tabulate import tabulate

from .blizzard_creds import CLIENT_ID, CLIENT_SECRET
from .constants import ARCHIVISTS_ACHIEVEMENT_ID, DEFAULT_REALM, DEFAULT_REGION, ENLIGHTENED_FACTION_ID, LOCALE
from .roster import get_roster

profile_api = ProfileApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def get_rep(character_name='Berga', realm=DEFAULT_REALM, faction_id=ENLIGHTENED_FACTION_ID):
    """
    Note: Retrieves all reps
    :return: {'raw': 41000, 'value': 0, 'max': 0, 'tier': 5, 'name': 'Tier 6'}
    """
    reps = profile_api.get_character_reputations_summary(
        region=DEFAULT_REGION,
        locale=LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    reps = list(filter(lambda r: r.get('faction').get('id') == faction_id, reps.get('reputations')))
    if reps:
        return reps[0].get('standing')
    else:
        return None


def get_achi_datetime(character_name='Berga', realm=DEFAULT_REALM, achievement_id=ARCHIVISTS_ACHIEVEMENT_ID):
    """
    Note: Retrieves all achievements
    """
    achis = profile_api.get_character_achievements_summary(
        region=DEFAULT_REGION,
        locale=LOCALE,
        realm_slug=realm.lower(),
        character_name=character_name.lower()
    )

    achis = list(filter(lambda a: a.get('id') == achievement_id, achis.get('achievements')))

    if not achis:
        return None

    ts_millis = achis[0].get('completed_timestamp')

    return datetime.fromtimestamp(ts_millis // 1000)


def get_roster_reps(faction_id, achievement_id, exclude_no_myth_raid=False, exclude_no_m_plus=False):
    roster = get_roster(exclude_no_myth_raid=exclude_no_myth_raid, exclude_no_m_plus=exclude_no_m_plus)
    rep_roster = []
    i = 1
    for r in roster:
        name = r.get('name')
        print(f'Processing: {name} ({i}/{len(roster)})')
        i += 1

        rep = get_rep(character_name=name, faction_id=faction_id)
        if rep:
            r['rep'] = rep
        else:
            continue

        if achievement_id:
            dt = get_achi_datetime(character_name=name, achievement_id=achievement_id)
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


def get_tabulate_element(m):
    rep = m.get('rep')
    return [m["name"], rep["raw"], f'{rep.get("value")}/{rep.get("max")}', m.get("rep_date", None)]


def print_and_get_table(members):
    print(f'Members with rep: {len(members)}')
    members = sorted(members,
                     key=sort_by_rep,
                     reverse=True)

    tabulate_list = [get_tabulate_element(m) for m in members]
    table = tabulate(tabulate_list,
                     headers=['Character', 'Raw Rep', 'Rep Tier Progress', 'Achievement Date'],
                     showindex=True)
    print(table)
    return table


def sort_by_rep(m):
    achi_date = m.get('rep_date')

    if achi_date:
        rev_achi_time = datetime.max - datetime.fromisoformat(achi_date)
    else:
        rev_achi_time = datetime.min

    return m.get('rep').get('raw'), rev_achi_time
