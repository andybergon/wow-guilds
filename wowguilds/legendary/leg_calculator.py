LEG_ILS = [190, 210, 225, 235, 249, 262, 291]

LEG_NAME_TO_ID = {
    # (.175 / .190)
    'Umbrahide Treads': 172315,
    'Grim Veiled Cape': 173242,  # considered cloth?
}

MAT_NAME_TO_ID = {
    'Desolate Leather': 172089,
}

LEG_TO_MATS = {
    'Umbrahide Treads': {
        'Enchanted Heavy Callous Hide': 15,
        'Heavy Callous Hide': 15,
        'Heavy Desolate Leather': 40,
        'Desolate Leather': 170,
        'Orboreal Shard': 40,
    }
}

IL_TO_REAGENT = {
    291: 'Vestige of the Eternal'
}

REAGENT_TO_PROF_TO_MATS = {
    'Vestige of the Eternal': {  # +3 ranks
        'Leatherworking': {
            'Protogenic Pelt': 40,
            'Heavy Callous Hide': 3,
            'Progenitor Essentia': 2,
        }
    },
    'Vestige of Origins': {
        'Leatherworking': {
            'Heavy Desolate Leather': 15,
            'Callous Hide': 15,
            'Pallid Bone': 70,
            'Korthite Crystal': 40,
        }
    }
}


def get_leg_id_by_name(leg_name):
    return LEG_NAME_TO_ID[leg_name]


def get_cost(mats):
    # todo
    pass


def get_leg_mats(leg_id):
    # todo
    pass


def get_leg_mats_cost(leg_id):
    mats = get_leg_mats(leg_id)
    get_cost(mats)
    pass


def main():
    # get legendary cost # blizzard api / TUJ
    # get legendary mats # hard code for now

    leg_id = get_leg_id_by_name('Umbrahide Treads')
    # maybe: mat, slot => item => item_id

    # get mats costs # blizzard api / TUJ
    get_leg_mats_cost(leg_id)
    pass


if __name__ == '__main__':
    main()
