import constants.buildtypes as types

builds = [
    {
        "name": "Cursors",
        "description": "Cursors to tap for you.",
        "owned": 0,
        "cost": 15,
        "known": False,
        "boost": 0.1,  # cps boost
        "type": types.CURSOR,
    },
    {
        "name": "Grandma",
        "description": "A nice grandma to bake you more cookies.",
        "owned": 0,
        "cost": 100,
        "known": False,
        "boost": 1,  # cps boost
        "type": types.GRANDMA,
    },
    {
        "name": "Farms",
        "description": "Farm is poop.",
        "owned": 0,
        "cost": 1100,
        "known": False,
        "boost": 8,  # cps boost
        "type": types.FARM,
    },
    {
        "name": "Mines",
        "description": "Mine some gold.",
        "owned": 0,
        "cost": 1200,
        "known": False,
        "boost": 47,  # cps boost
        "type": types.MINE,
    },
]
