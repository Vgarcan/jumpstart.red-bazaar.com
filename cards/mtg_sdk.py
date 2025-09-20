from mtgsdk import Card, Set
from datetime import datetime
import time

# ======= Carga de sets una única vez (lookup O(1)) =======
ALL_SETS = {s.code: s for s in Set.all()}


def _parse_date(d: str | None) -> datetime:
    """Convierte 'YYYY-MM-DD' a datetime; si no hay fecha, usa datetime.min."""
    if not d:
        return datetime.min
    return datetime.strptime(d, "%Y-%m-%d")


def get_latest_card(card_name: str, limit: int = 5, startswith: bool = True, order_by: str = "date", print_info: bool = False):
    """
    Devuelve hasta `limit` cartas únicas por nombre, quedándose con la edición más nueva.

    Args:
        card_name (str): término de búsqueda.
        limit (int): número máximo de resultados.
        startswith (bool): si True, solo nombres que empiecen por `card_name`.
        order_by (str): 'date' (más nuevo primero) o 'alpha' (orden alfabético A→Z).
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


print("\n==============================\n")
get_latest_card("garruk", limit=5, startswith=True,
                order_by="alpha", print_info=True)
print("\n==============================\n")
get_latest_card("Liliana", limit=5, startswith=True,
                order_by="alpha", print_info=True)
print("\n==============================\n")
get_latest_card("elem", limit=5, startswith=True,
                order_by="alpha", print_info=True)
print("\n==============================\n")
