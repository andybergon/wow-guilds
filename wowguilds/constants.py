# RaiderIO
from enum import Enum

from wowguilds.guild_coordinates import GuildCoordinates

DEFAULT_REGION = 'eu'
DEFAULT_REALM = 'nemesis'
DEFAULT_GUILD = 'IgnorHunters'
DEFAULT_GUILD_COORDINATES = GuildCoordinates(region=DEFAULT_REGION, realm=DEFAULT_REALM, guild=DEFAULT_GUILD)

SOD_RAID = 'sanctum-of-domination'
SFO_RAID = 'sepulcher-of-the-first-ones'
MYTHIC_DIFFICULTY = 'mythic'
HEROIC_DIFFICULTY = 'heroic'
ALL_FACTIONS = ''

# Blizzard API
LOCALE = 'en_US'

# WowHead / Game
ARCHIVISTS_FACTION_ID = 2472  # The Archivists' Codex
ARCHIVISTS_ACHIEVEMENT_ID = 15069  # The Archivists' Codex
ENLIGHTENED_FACTION_ID = 2478  # The Enlightened
ENLIGHTENED_ACHIEVEMENT_ID = 15220  # The Enlightened


class Faction(Enum):
    ARCHIVISTS = 1
    ENLIGHTENED = 2


faction_to_ids = {
    Faction.ARCHIVISTS: (ARCHIVISTS_FACTION_ID, ARCHIVISTS_ACHIEVEMENT_ID),
    Faction.ENLIGHTENED: (ENLIGHTENED_FACTION_ID, ENLIGHTENED_ACHIEVEMENT_ID)
}
