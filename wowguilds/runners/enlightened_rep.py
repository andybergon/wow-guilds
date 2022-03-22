import argparse
from datetime import datetime
from pathlib import Path

from wowguilds import constants
from wowguilds.constants import DEFAULT_GUILD_COORDINATES
from wowguilds.guild_coordinates import GuildCoordinates
from wowguilds.rep_calculator import get_roster_reps, print_and_get_table, read_from_file, write_to_file


def save_end_result(table, guild_coord, rep_faction):
    filename = f'data1/{rep_faction.name.lower()}-{guild_coord.region}-{guild_coord.realm}-{guild_coord.guild}-{datetime.utcnow().isoformat()}.txt'.lower()
    print(f'Saving results in: {filename}')

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, 'w+') as f:
        f.write(table)


def run(rep_faction=constants.Faction.ENLIGHTENED,
        guild_coordinates: GuildCoordinates = DEFAULT_GUILD_COORDINATES,
        refresh_data=True):
    filename = f'data/{rep_faction.name.lower()}.json'
    if refresh_data:
        members = get_roster_reps(guild_coordinates, *constants.faction_to_ids[rep_faction])
        write_to_file(members, filename)
    members = read_from_file(filename)
    table = print_and_get_table(members)
    save_end_result(table, guild_coordinates, rep_faction)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', default='eu')
    parser.add_argument('--realm', default='Nemesis')
    parser.add_argument('--guild', default='IgnorHunters')
    parser.add_argument('--refresh', action='store_true')
    return parser.parse_args()


def main():
    args = get_args()
    guild_coordinates = GuildCoordinates(args.region, args.realm, args.guild)
    run(rep_faction=constants.Faction.ENLIGHTENED, guild_coordinates=guild_coordinates, refresh_data=args.refresh)


if __name__ == '__main__':
    main()
