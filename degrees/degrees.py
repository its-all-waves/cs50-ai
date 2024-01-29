import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set(),
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set(),
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # # DEBUG REMOVE ME ///////////////////////////
    # source = person_id_for_name("kevin bacon")
    # # ///////////////////////////////////////////
    source = person_id_for_name(input("Name: "))  # UNCOMMENT ME
    if source is None:
        sys.exit("Person not found.")

    # # DEBUG REMOVE ME ///////////////////////////
    # target = person_id_for_name("tom hanks")
    # # ///////////////////////////////////////////
    target = person_id_for_name(input("Name: "))  # UNCOMMENT ME
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# TODO implement breadth first search
def shortest_path(source: str, target: str) -> list[tuple[str, str]]:
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    :arg: source = id string
    :arg: target = id string

    NOTE: node.state = .actor, .parent = .previous, .action = .movie
    """

    shortest_path: list[tuple[str, str]] = []

    start = Node(actor=source, previous=None, movie=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    while True:
        # IF FRONTIER IS EMPTY, RETURN NO SOLUTION
        if frontier.empty():
            print("No connection found.")
            return None

        # REMOVE A NODE FROM THE FRONTIER
        node = frontier.remove()

        # IF NODE CONTAINS GOAL STATE, RETURN THE SOLUTION
        if node.actor == target:
            while node.previous:
                shortest_path.append((node.movie, node.actor))
                node = node.previous
            shortest_path.reverse()
            return shortest_path

        # ADD THE NODE TO THE EXPLORED SET
        explored.add(node.actor)

        # EXPAND NODE: ADD RESULTING NODES TO THE FRONTIER IF NOT ALREADY
        # IN THE FRONTIER OR EXPLORED SET
        for movie, actor in neighbors_for_person(node.actor):
            if not frontier.contains(actor) and actor not in explored:
                new_node = Node(actor=actor, previous=node, movie=movie)
                frontier.add(new_node)


def person_id_for_name(name) -> str:
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id) -> set:
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
