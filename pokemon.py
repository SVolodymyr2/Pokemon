import aiohttp
import asyncio
import random


async def fetch_pokemon(session, pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    async with session.get(url) as response:
        return await response.json() if response.status == 200 else None


def calculate_strength(pokemon):
    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon["stats"]}
    return stats["attack"] + stats["defense"] + stats["speed"] + stats["hp"] + stats["special-attack"] + stats[
        "special-defense"]


async def main():
    pokemon_ids = random.sample(range(1, 21), 10)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, pid) for pid in pokemon_ids]
        pokemon_data = [p for p in await asyncio.gather(*tasks) if p]

    pokemon_list = [
        {
            "name": p["name"],
            "strength": calculate_strength(p),
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in p["stats"]},
        }
        for p in pokemon_data
    ]

    pokemon_list.sort(key=lambda x: x["strength"], reverse=True)

    print("List of Pokemon:")
    for p in pokemon_list:
        print(f"{p['name'].capitalize()} | Strength: {p['strength']} | Stats: {p['stats']}")

    print("\nBattle Simulation:")
    for _ in range(5):
        p1, p2 = random.sample(pokemon_list, 2)
        print(f"Battle: {p1['name'].capitalize()} ({p1['strength']}) vs {p2['name'].capitalize()} ({p2['strength']})")
        if p1["strength"] > p2["strength"]:
            print(f"Winner: {p1['name'].capitalize()}")
        elif p2["strength"] > p1["strength"]:
            print(f"Winner: {p2['name'].capitalize()}")
        else:
            print("A draw!")
        print()

    if pokemon_list:
        strongest = pokemon_list[0]
        print(f"The strongest pokemon: {strongest['name'].capitalize()} with the power {strongest['strength']}.")


if __name__ == "__main__":
    asyncio.run(main())
