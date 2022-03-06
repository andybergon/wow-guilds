import argparse
from datetime import datetime
from pathlib import Path

from wowguilds import constants
from wowguilds.constants import DEFAULT_GUILD_COORDINATES
from wowguilds.rep_calculator import get_roster_reps, print_and_get_table, read_from_file, write_to_file


def save_end_result(table, guild_coord, faction):
    filename = f'data1/{faction.name.lower()}-{guild_coord.get("region")}-{guild_coord.get("realm")}-{guild_coord.get("guild")}-{datetime.utcnow().isoformat()}.txt'.lower()
    print(f'Saving results in: {filename}')

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, 'w+') as f:
        f.write(table)


def run(rep_faction=constants.Faction.ENLIGHTENED, guild_coordinates=DEFAULT_GUILD_COORDINATES, refresh_data=True):
    filename = f'data/{rep_faction.name.lower()}.json'
    if refresh_data:
        members = get_roster_reps(guild_coordinates, *constants.faction_to_ids[rep_faction])
        write_to_file(members, filename)
    members = read_from_file(filename)
    table = print_and_get_table(members)
    save_end_result(table, guild_coordinates, rep_faction)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--region', default='eu')
    parser.add_argument('--realm', default='Nemesis')
    parser.add_argument('--guild', default='IgnorHunters')
    return parser.parse_args()


def main():
    args = get_args()
    guild_coordinates = {'region': args.region, 'realm': args.realm, 'guild': args.guild}
    run(rep_faction=constants.Faction.ENLIGHTENED, guild_coordinates=guild_coordinates, refresh_data=args.refresh)


if __name__ == '__main__':
    main()
