from wowguilds import constants
from wowguilds.rep_calculator import get_roster_reps, print_members, read_from_file, write_to_file


def main(faction=constants.Faction.ENLIGHTENED, retrieve=True):
    filename = f'data/{faction.name.lower()}.json'
    if retrieve:
        members = get_roster_reps(*constants.faction_to_ids[faction])
        write_to_file(members, filename)
    members = read_from_file(filename)
    print_members(members)


if __name__ == '__main__':
    main(faction=constants.Faction.ENLIGHTENED, retrieve=False)
