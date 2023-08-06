import pprint
from random import random

from antiheroes.data import hero_list


pp = pprint.PrettyPrinter(indent=4)


def get_hero() -> None:
    num_heros = len(hero_list)
    random_num=int(random() * num_heros)
    hero = hero_list[random_num]["name"]
    print(f"{hero} enters in your room!!!")


def list_heroes() -> None:
    print("ALL ANTI HEROES:")
    pp.pprint(hero_list)


def popular_heroes(count:int) -> None:
    print(f"TOP {count} ANTI HEROES:")
    try:
        for hero in hero_list[:count]:
            print(hero)
    except:
        print("please type a number -> ex. popular_heroes(10)")