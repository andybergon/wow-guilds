from datetime import datetime

from wowguilds import constants
from wowguilds.rep_calculator import get_roster_reps, print_and_get_table, read_from_file, write_to_file


def save_end_result(table, faction):
    filename = f'data/{faction.name.lower()}-{datetime.utcnow().isoformat()}.txt'
    with open(filename, 'w+') as f:
        f.write(table)


def main(faction=constants.Faction.ENLIGHTENED, retrieve=True):
    filename = f'data/{faction.name.lower()}.json'
    if retrieve:
        members = get_roster_reps(*constants.faction_to_ids[faction])
        write_to_file(members, filename)
    members = read_from_file(filename)
    table = print_and_get_table(members)
    save_end_result(table, faction)


if __name__ == '__main__':
    main(faction=constants.Faction.ENLIGHTENED, retrieve=False)
