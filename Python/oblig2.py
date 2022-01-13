from collections import defaultdict, deque
import heapq as h


ratings = defaultdict(lambda: float("NaN"))
# movieid: (rating, movie_name)

actor_dict = {}
# actor: (actor_name [(movie1, rating1), (movie2, rating2), ...])

movie_dict = {}
# movie: [actor1, actor2, ...]

actor_names = {}

movie_names = {}


with open("movies.tsv") as infile1, open("actors.tsv") as infile2:
    for line in infile1:
        line = line.strip("\n").split("\t")

        ratings[line[0]] = float(line[2])

        movie_dict[line[0]] = []

        movie_names[line[0]] = line[1]
    for line in infile2:

        line = line.strip("\n").split("\t")

        actor_names[line[0]] = line[1]

        actor_dict[line[0]] = []

        for element in line[2:]:
            try:
                movie_dict[element].append(line[0])
                actor_dict[line[0]].append((element, ratings[element]))
            except:
                None

imdb_graph = {} #Key: name_id ; Value: [((movie_id, rating), name_id), xxx]

for element in actor_dict:
    imdb_graph[element] = []
    for movie in actor_dict[element]:
        for act in movie_dict[movie[0]]:
            if act != element:
                imdb_graph[element].append((movie, act))

def shortest_path(ID_one, ID_two): #name_id
    path = []
    temp = defaultdict(lambda: "None")
    queue = []

    queue.append(ID_one)
    temp[ID_one] = "Root"

    def BFS(ID_one, ID_two):
        while temp[ID_two] == "None":
            for actor in imdb_graph[ID_one]:
                if temp[actor[1]] == "None":
                    queue.append(actor[1])
                    temp[actor[1]] = ID_one
                    continue
                else:
                    continue

            queue.pop(0)
            BFS(queue[0],ID_two)

    BFS(ID_one, ID_two)

    current = ID_two
    while current != "Root":
        path.append(current)
        current = temp[current]

    print(actor_names[path[-1]])
    for i in range(len(path)-1, 0, -1):
        for element in imdb_graph[path[i]]:
            if element[1] == path[i-1]:
                print(f"==={movie_names[element[0][0]], element[0][1]} ===> {actor_names[element[1]]}")
                break
    print("\n")

    return

def dijkstra_path(graph, start, stop=None):
    unvisited = []
    visited = set()
    dijkstra_path = {}
    dijkstra_path[start] = ("Root", ("", 0))
    answer = []

    D = defaultdict(lambda: float("inf"))
    D[start] = 0

    h.heappush(unvisited, (D[start], start))

    while len(unvisited) > 0:
        _, v = h.heappop(unvisited)
        visited.add(v)
        for node in graph[v]:
            c, t = node
            cost = 10 - float(c[1])
            if D[v] + cost < D[t]:
                dijkstra_path[t] = (v, c)
                D[t] = D[v] + cost
                if t != visited:
                     h.heappush(unvisited, (D[t], t))
                else:
                    unvisited = replace_in_heap(unvisited, cost, t)

    current = stop
    cost = 0
    while dijkstra_path[current][0] != "Root":
        answer.append(((movie_names[dijkstra_path[current][1][0]], \
        dijkstra_path[current][1][1]), actor_names[current]))
        cost += 10 - dijkstra_path[current][1][1]
        current = dijkstra_path[current][0]

    print(f"{actor_names[start]}")
    for i in range(len(answer)-1, -1, -1):
        print(f"==={answer[i][0][0], answer[i][0][1]} ===> {answer[i][1]}")
    print(f"Total weight: {cost:.1f}")
    print("\n")

    return

def replace_in_heap(heap, cost, node):
    new_heap = []
    while heap:
        v = h.heappop(heap)
        if v[1] == node:
            h.heappush(new_heap, (cost, node))
        else:
            h.heappush(new_heap, (v[0], v[1]))
    return new_heap

def BFS_count(graph):
    unvisited = set(imdb_graph.keys())
    components = {}
    while unvisited:
        root = unvisited.pop()
        def BFS2(graph,start):
            visited = set([start])
            queue = deque([start])
            count = 1
            while queue:
                v = deque.popleft(queue)
                for u in graph[v]:
                    if u[1] not in visited:
                        visited.add(u[1])
                        unvisited.remove(u[1])
                        queue.append(u[1])
                        count = count + 1
            return count
        count = BFS2(graph,root)
        try:
            components[count] += 1
        except:
            components[count] = 1

    finito = sorted(components.keys())
    for i in reversed(finito):
        print(f"There are {components[i]} components of size {i}")

    return

if __name__ == "__main__":
    print("========== Oppgave 1 ==========")
    sum1 = 0
    sum2 = 0
    for element1 in imdb_graph:
        sum1 += 1
        for element2 in imdb_graph[element1]:
            sum2 += 1

    print(f"Nodes : {sum1}")
    print(f"Edges : {int(sum2/2)}")
    print("")
    print("========== Oppgave 2 ==========")
    print("")
    shortest_path('nm2255973', 'nm0000460')
    shortest_path('nm0424060', 'nm0000243')
    shortest_path('nm4689420', 'nm0000365')
    shortest_path('nm0000288', 'nm0001401')
    shortest_path('nm0031483', 'nm0931324')
    print("========== Oppgave 3 ==========")
    print("")
    dijkstra_path(imdb_graph, 'nm2255973', 'nm0000460')
    dijkstra_path(imdb_graph, 'nm0424060', 'nm0000243')
    dijkstra_path(imdb_graph, 'nm4689420', 'nm0000365')
    dijkstra_path(imdb_graph, 'nm0000288', 'nm0001401')
    dijkstra_path(imdb_graph, 'nm0031483', 'nm0931324')

    print("========== Oppgave 4 ==========")
    print("")
    BFS_count(imdb_graph)
