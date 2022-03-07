from pygame.image import load

import constants.upgradetypes as types

upgrades = [
    {
        "name": "Plastic mouse",
        "description": "Tappin gains + 1.1% of your, CpS.",
        "cost": 100,
        "surface": load(
            "./assets/upgrades/Arrow_Plain_v15.png"
        ),
        "type": types.CLICK,
        "amount": 5.1,
    },
    {
        "name": "Iron mouse",
        "description": "Tappin gains + 1.2% of your CpS.",
        "cost": 500,
        "surface": load(
            "./assets/upgrades/Arrow_Berrylium_v15.png"
        ),
        "type": types.CLICK,
        "amount": 9.2,
    },
    {
        "name": "Titanium mouse",
        "description": "Tappin gains + 2% of your CpS.",
        "cost": 1000,
        "surface": load(
            "./assets/upgrades/Arrow_Blueberrylium_v15.png"
        ),
        "type": types.CLICK,
        "amount": 10,
    },
    {
        "name": "Adamantium mouse",
        "description": "Tappin gains + 2.1% of your CpS.",
        "cost": 5000,
        "surface": load(
            "./assets/upgrades/Arrow_Chalcedhoney_v15.webp"
        ),
        "type": types.CLICK,
        "amount": 100.1,
    },
    {
        "name": "Unobtainium mouse",
        "description": "Tappin gains + 2.5% of your CpS.",
        "cost": 50000,
        "surface": load(
            "./assets/upgrades/Arrow_Buttergold_v15.png"
        ),
        "type": types.CLICK,
        "amount": 500.5,
    },
    {
        "name": "Eludium mouse",
        "description": "Tappin gains + 3% of your CpS.",
        "cost": 100000,
        "surface": load(
            "./assets/upgrades/Arrow_Sugarmuck_v15.png"
        ),
        "type": types.CLICK,
        "amount": 100000,
    },
]