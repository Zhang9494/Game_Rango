import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_rango.settings')

import django

django.setup()
from game.models import Category, Game


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through ea    ch data structure, and add the data to our models.

    pc_games = [
        {"title": "Apex Legends",
         "publisher": "EA",
         "url": "https://www.ea.com/games/apex-legends",
         "mark": 90,
         "picture": "game_images/AL.jpg"
         },
        {"title": "Devil May Cry V",
         "publisher": "CAPCOM",
         "url": "http://www.devilmaycry5.com",
         "mark": 95,
         "picture": "game_images/DMC.png"
         },
        {"title": "NBA 2K19",
         "publisher": "2K Sports",
         "url": "https://www.2k.com/en-US/game/nba-2k19-standard-edition/",
         "mark": 88,
         "picture": "game_images/NBA.jpg"
         }]

    mobile_games = [
        {"title": "Arena of Valor",
         "publisher": "Tencent Games",
         "url": "https://www.arenaofvalor.com/",
         "mark": 96,
         "picture": "game_images/AOV.jpg"
         },
        {"title": "Angry Birds",
         "publisher": "Rovio Entertainment",
         "url": "https://www.angrybirds.com/",
         "mark": 85,
         "picture": "game_images/AB.jpg"
         },
        {"title": "Pokémon GO",
         "publisher": "Niantic",
         "url": "https://www.pokemongo.com/en-us/",
         "mark": 91,
         "picture": "game_images/PG.jpeg"
         }]
         

    console_games = [
        {"title": "Super Smash Bros",
         "publisher": "Nintendo",
         "url": "https://mario.nintendo.com/",
         "mark": 98,
         "picture": "game_images/SSB.jpg"
         },
        {"title": "The Legend of Zelda",
         "publisher": "Nintendo",
         "url": "https://www.zelda.com/",
         "mark": 91,
         "picture": "game_images/TLOZ.jpg"
         },
        {"title": "Pokémon: Let's Go, Pikachu!",
         "publisher": "Nintendo",
         "url": "https://www.2k.com/en-US/game/nba-2k19-standard-edition/",
         "mark": 88,
         "picture": "game_images/PLG.jpg"
         }]
         

    cats = {"PC Games": {"games": pc_games, "amount":3},
            "Mobile Games": {"games": mobile_games,"amount":3},
            "Console Games": {"games": console_games,"amount":3}}


    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["amount"])
        for g_data in cat_data["games"]:
            game = add_game(c, g_data["title"], g_data["publisher"], g_data["url"], g_data["mark"], g_data["picture"])


    # Print out the categories we have added.
    for c in Category.objects.all():
        for g in Game.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(g)))


def add_game(cat, title, publisher, url, mark, picture):
    g = Game.objects.get_or_create(category=cat, title=title)[0]
    g.url = url
    g.publisher = publisher
    g.mark = mark
    g.picture = picture
    g.save()
    return g


def add_cat(name, amount):
    c = Category.objects.get_or_create(name=name)[0]
    c.amount = amount
    c.save()
    return c




# Start execution here!
if __name__ == '__main__':
    print("Starting zone population script...")
    populate()
