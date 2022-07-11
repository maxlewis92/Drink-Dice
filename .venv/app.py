# Drink Dice game
# Generates a random drink prompt

import random
from flask import Flask, render_template

app = Flask(__name__)

TEMPLATES = [
    ["Old Fashioned", [
        "Honey",
        "Fresh Fruit",
        "Maple Syrup",
        "Improved",
        "Agave"
        ], 
        "2<sub>oz</sub> spirit, ¼<sub>oz</sub> sweetener, bitters"
    ],
    ["Manhattan", [
        "Sweet Vermouth",
        "Dry Vermouth",
        "Gentiane",
        "Amaro",
        "Fortified Wine",
        "Liqueur"
        ], 
        "2<sub>oz</sub> spirit, 1<sub>oz</sub> variation, optional bitters"
    ],
    ["Sour", [
        "Grapefruit",
        "Fresh Fruit",
        "Cinnamon",
        "Honey",
        "Ginger",
        "Wine"
        ],
        "2<sub>oz</sub> spirit, ¾<sub>oz</sub> sweetener, ¾<sub>oz</sub> citrus"
    ],
    ["Sidecar", [
        "Curacao",
        "Amaro",
        "Maraschino",
        "Amaro Nonino",
        "Benedictine",
        "Chartreuse"
        ],
        "2<sub>oz</sub> spirit, 1<sub>oz</sub> variation, ¾<sub>oz</sub> citrus"
    ],
    ["Highball", [
        "Beer",
        "Champagne",
        "Grapefruit",
        "Absinthe",
        "Fresh Fruit",
        "Mint"
        ],
        "2<sub>oz</sub> spirit, 3/4<sub>oz</sub> citrus, ¾<sub>oz</sub> sweetener, top with soda water",
    ],
    ["Last Word", [
        "Fortified Wine",
        "Coffee",
        "Amaro",
        "Campari",
        "Amaro Nonino",
        "Cynar"
        ],
        "¾<sub>oz</sub> spirit, ¾<sub>oz</sub> variation, ¾<sub>oz</sub> liqueur, ¾<sub>oz</sub> citrus",
    ],
    ["Negroni", [
        "Fortified Wine",
        "Coffee",
        "Amaro",
        "Campari",
        "Amaro Nonino",
        "Cynar"
        ],
        "1<sub>oz</sub> spirit, 1<sub>oz</sub> variation, 1<sub>oz</sub> liqueur or vermouth",
    ]
]

SPIRITS = [
    "Bourbon",
    "Rye",
    "Scotch",
    "Rum",
    "Tequila",
    "Mezcal",
    "Gin",
    "Amaro",
    "Brandy",
    "Bitters"
]

def roll_drink():
    templateRoll = random.randint(0, len(TEMPLATES) - 1)
    spiritRoll = random.randint(0, len(SPIRITS) - 1)
    variationRoll = random.randint(0, len(TEMPLATES[templateRoll]) - 1)

    roll = {
        "spirit"    : SPIRITS[spiritRoll],
        "template"  : TEMPLATES[templateRoll][0],
        "variation" : TEMPLATES[templateRoll][1][variationRoll],
        "recipe"    : TEMPLATES[templateRoll][2]
    }

    #Get rid of repeated ingredients, such as "Amaro Manhattan with Amaro"
    while roll["spirit"].lower == roll["variation"].lower:
        roll_drink()

    #Replace appropriate recipe text
    roll["recipe"] = roll["recipe"].replace("spirit",roll["spirit"].lower())
    roll["recipe"] = roll["recipe"].replace("variation",roll["variation"].lower())

    #Prettify fractions
    roll["recipe"] = roll["recipe"].replace("1/2","&frac12;".lower())
    roll["recipe"] = roll["recipe"].replace("1/3","&frac13;".lower())
    roll["recipe"] = roll["recipe"].replace("2/3","&frac23;".lower())
    roll["recipe"] = roll["recipe"].replace("1/4","&frac14;".lower())
    roll["recipe"] = roll["recipe"].replace("3/4","&frac34;".lower())

    #Temporary special recipe formatting
    if roll["template"] == "Highball" and roll["variation"] in ("Beer","Champagne"):
        roll["recipe"] = roll["recipe"].replace("soda water",roll["variation"].lower())

    return roll


@app.route("/")
def index():
    return render_template('index.html', result = roll_drink())

if __name__ == '__main__':
    app.run(debug=True)