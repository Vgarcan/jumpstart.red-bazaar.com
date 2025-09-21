from mtgsdk import Card, Set
from datetime import datetime
import time

# ======= Carga de sets una única vez (lookup O(1)) =======
ALL_SETS = {s.code: s for s in Set.all()}


def _parse_date(d: str | None) -> datetime:
    """
    Parses a date string in the format 'YYYY-MM-DD' into a datetime object.

    Args:
        d (str | None): The date string to parse. If None or an empty string, 
                        returns the minimum possible datetime value.

    Returns:
        datetime: The parsed datetime object, or datetime.min if the input is None or empty.
    """
    if not d:
        return datetime.min
    return datetime.strptime(d, "%Y-%m-%d")


def get_latest_card(card_name: str, limit: int = 5, startswith: bool = True, order_by: str = "date", print_info: bool = False):
    """
    Retrieve the latest versions of a card by name, optionally filtering and sorting the results.
    Args:
        card_name (str): The name of the card to search for.
        limit (int, optional): The maximum number of results to return. Defaults to 5.
        startswith (bool, optional): If True, only include cards whose names start with the given `card_name`. Defaults to True.
        order_by (str, optional): The sorting criteria for the results. 
            - "alpha": Sort alphabetically by card name.
            - "date": Sort by release date (most recent first). Defaults to "date".
        print_info (bool, optional): If True, print detailed information about the process and results. Defaults to False.
    Returns:
        list[dict]: A list of dictionaries, each containing information about a card:
            - "name" (str): The name of the card.
            - "set_name" (str or None): The name of the set the card belongs to.
            - "set" (str): The set code.
            - "type" (str): The type of the card.
            - "mana_cost" (str or None): The mana cost of the card.
            - "release_date" (str or None): The release date of the set.
    Notes:
        - The function fetches all cards matching the `card_name` from the API and filters them based on the `startswith` parameter.
        - It keeps only the latest version of each card based on the release date.
        - Results are sorted according to the `order_by` parameter and limited to the specified `limit`.
        - If `print_info` is True, the function prints diagnostic information about the process and the results.
    Example:
        get_latest_card("Liliana", limit=3, startswith=True, order_by="date", print_info=True)
    Example Output:
        Found 10 cards with name 'Liliana'. API call took 0.123s.
        Liliana, the Last Hope > {1}{B}{B} > Legendary Planeswalker — Liliana > Eldritch Moon (EMN) > 2016-07-22
        Liliana of the Veil > {1}{B}{B} > Legendary Planeswalker — Liliana > Innistrad (ISD) > 2011-09-30
        Liliana, Death's Majesty > {3}{B}{B} > Legendary Planeswalker — Liliana > Amonkhet (AKH) > 2017-04-28
        Processing took 0.045s. Total: 0.168s.
    """

    t0 = time.perf_counter()

    # 1) Traer candidatos
    cards = Card.where(name=card_name).all()
    t1 = time.perf_counter()
    if print_info:
        print(
            f"Found {len(cards)} cards with name '{card_name}'. API call took {t1 - t0:.3f}s.")

    q = card_name.strip().lower()

    # 2) Un pase: quedarnos con la versión más nueva por nombre
    latest_by_name = {}

    for c in cards:
        name_norm = c.name.lower()
        if startswith and not name_norm.startswith(q):
            continue

        s = ALL_SETS.get(c.set)
        rel_dt = _parse_date(s.release_date if s else None)

        info = {
            "name": c.name,
            "set_name": s.name if s else None,
            "set": c.set,
            "type": c.type,
            "mana_cost": c.mana_cost,
            "release_date": s.release_date if s else None,
            "_rel_dt": rel_dt,
        }

        prev = latest_by_name.get(c.name)
        if (prev is None) or (rel_dt > prev["_rel_dt"]):
            latest_by_name[c.name] = info

    # 3) Ordenar según order_by
    if order_by == "alpha":
        results = sorted(latest_by_name.values(),
                         key=lambda x: x["name"].lower())
    else:  # por fecha (default)
        results = sorted(latest_by_name.values(),
                         key=lambda x: x["_rel_dt"], reverse=True)

    # Limitar
    results = results[:limit]

    # Limpiar clave interna y mostrar
    for r in results:
        r.pop("_rel_dt", None)
        if print_info:
            print(r["name"], ">", r["mana_cost"], ">", r["type"], ">",
                  f'{r["set_name"]} ({r["set"]})', ">", r["release_date"])

    t2 = time.perf_counter()
    if print_info:
        print(f"Processing took {t2 - t1:.3f}s. Total: {t2 - t0:.3f}s.")

    return results


# Ejemplos de uso
# get_latest_card("Liliana", limit=5, startswith=True, order_by="date")   # por fecha
# get_latest_card("Liliana", limit=5, startswith=True, order_by="alpha")  # por orden alfabético


# print("\n==============================\n")
# get_latest_card("garruk", limit=5, startswith=True,
#                 order_by="alpha", print_info=True)
# print("\n==============================\n")
# get_latest_card("Liliana", limit=5, startswith=True,
#                 order_by="alpha", print_info=True)
# print("\n==============================\n")
# get_latest_card("elem", limit=5, startswith=True,
#                 order_by="alpha", print_info=True)
# print("\n==============================\n")


def get_card_by_name_and_set(card_name: str = None, set_code: str = None, set_name: str = None):
    """
    Retrieve Magic: The Gathering card information by card name and set.

    Args:
        card_name (str, optional): The name of the card to search for. Required.
        set_code (str, optional): The code of the set to filter cards by. If provided, takes precedence over set_name.
        set_name (str, optional): The name of the set to filter cards by. Used if set_code is not provided.

    Returns:
        dict or None: 
            - If multiple cards are found (e.g., double-faced cards), returns a dictionary with "front" and "back" keys containing card details.
            - If a single card is found, returns a dictionary with a "front" key containing card details.
            - Returns None if no card_name is provided or no cards are found.

    Notes:
        - Prints diagnostic information about the search and results.
        - Card details include name, set, set_name, type, mana_cost, text, power, toughness, loyalty, rarity, artist, flavor, and image_url.

    Example:
        get_card_by_name_and_set(card_name='Archangel Avacyn', set_code='SOI')
        get_card_by_name_and_set(card_name='Shock', set_name='Tenth Edition')

    Example Output:
        {
            "front": {
                "name": "Archangel Avacyn",
                "set": "SOI",
                "set_name": "Shadows over Innistrad",
                "type": "Legendary Creature — Angel",
                "mana_cost": "{3}{W}{W}",
                "text": "Flash, flying, vigilance\nWhen Archangel Avacyn enters the battlefield, creatures you control gain indestructible until end of turn.\nWhen Archangel Avacyn transforms into Avacyn, the Purifier, it deals 3 damage to each creature and each player.",
                "power": "4",
                "toughness": "4",
                "loyalty": None,
                "rarity": "Mythic",
                "image_url": "https://img.scryfall.com/cards/large/en/soi/1.jpg?1517813031"
            },
            "back": {
                "name": "Avacyn, the Purifier",                 
                "set": "SOI",
                "set_name": "Shadows over Innistrad",
                "type": "Legendary Creature — Angel",
                "mana_cost": "",    
                "text": "Flying, vigilance\nWhen this creature transforms into Avacyn, the Purifier, it deals 3 damage to each creature and each player.",
                "power": "6",
                "toughness": "6",
                "loyalty": None,
                "rarity": "Mythic",
                "image_url": "https://img.scryfall.com/cards/large/en/soi/1b.jpg?1517813031"
            }
        }       

    """

    if not card_name:
        print("Card name is required.")
        return None

    if set_code:
        cards = Card.where(name=card_name.lower()).where(
            set=set_code.lower()).all()
    elif set_name:
        cards = Card.where(name=card_name.lower()).where(
            setName=set_name.lower()).all()

    # Comprobar cuantas cartas se han encontrado
    print(
        f"Found {len(cards)} cards with name '{card_name}' in set '{set_code}'.")

    if len(cards) > 1:
        print("Double faced card detected. Returning both faces.")

        returned_card = {
            "front": {
                "name": cards[0].name,
                "set": cards[0].set,
                "set_name": cards[0].set_name,
                "type": cards[0].type,
                "subtypes": cards[0].subtypes,
                "mana_cost": cards[0].mana_cost,
                "text": cards[0].text,
                "power": cards[0].power,
                "toughness": cards[0].toughness,
                "loyalty": cards[0].loyalty,
                "rarity": cards[0].rarity,
                "image_url": cards[0].image_url,
            },
            "back": {
                "name": cards[1].name,
                "set": cards[1].set,
                "set_name": cards[1].set_name,
                "type": cards[1].type,
                "subtypes": cards[0].subtypes,
                "mana_cost": cards[1].mana_cost,
                "text": cards[1].text,
                "power": cards[1].power,
                "toughness": cards[1].toughness,
                "loyalty": cards[1].loyalty,
                "rarity": cards[1].rarity,
                "image_url": cards[1].image_url,
            }
        }

        print(returned_card)
        return returned_card

    elif len(cards) == 1:
        returned_card = {
            "front": {
                "name": cards[0].name,
                "set": cards[0].set,
                "set_name": cards[0].set_name,
                "type": cards[0].type,
                "subtypes": cards[0].subtypes,
                "mana_cost": cards[0].mana_cost,
                "text": cards[0].text,
                "power": cards[0].power,
                "toughness": cards[0].toughness,
                "loyalty": cards[0].loyalty,
                "rarity": cards[0].rarity,
                "image_url": cards[0].image_url,
            },
        }

        print(returned_card)
        return returned_card


# print("\n==============================\n")
# print("\n==============================\n")

# card_name = 'Archangel Avacyn'
# card_set = 'SOI'

# get_card_by_name_and_set(card_name=card_name.lower(),
#                          set_code=card_set.lower())


# print("\n==============================\n")
# print("\n==============================\n")

# card_name = 'shock'
# card_set = 'Tenth Edition'

# get_card_by_name_and_set(card_name=card_name.lower(),
#                          set_name=card_set.lower())


# get_card_by_name_and_set(card_name='Liliana of the Veil', set_code='ISD')
