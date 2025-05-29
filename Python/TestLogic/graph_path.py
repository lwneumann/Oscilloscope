import util
from collections import defaultdict


class Graph:
    def __init__(self, lines):
        self.graph = defaultdict(list)
        # To track visited edges
        self.edges = {}
        self.build_graph(lines)
        return

    def build_graph(self, lines):
        """Convert list of points and lines into an adjacency list."""
        for i, j in lines:
            self.graph[i].append(j)
            self.graph[j].append(i)
            # Mark edges as unvisited
            self.edges[(i, j)] = False
            # Since it's undirected
            self.edges[(j, i)] = False
        return

    def find_path(self, node, path):
        """Recursive DFS traversal ensuring all edges are visited at least once."""
        for neighbor in self.graph[node]:
            # Check if edge is unvisited
            if not self.edges[(node, neighbor)]:
                # Mark as visited
                self.edges[(node, neighbor)] = True
                # Mark reverse as visited
                self.edges[(neighbor, node)] = True
                self.find_path(neighbor, path)
        path.append(node)
        return

    def get_edge_covering_path(self, start):
        """Returns a path that covers all edges at least once."""
        path = []
        self.find_path(start, path)
        # Reverse the path to maintain order
        return path[::-1]


def parameterize_lines(point_path, numer_of_samples = 1000):
    """
    Across total length with uniform speed created points along the whole path touching all points
    point_path - [
            [x, y],
            ...
        ]
    """
    # Ignore single points
    if len(point_path) == 1:
        return point_path

    # Setup
    lengths = [0]
    for p_i in range(len(point_path)-1):
        lengths.append(lengths[-1] + util.distance(point_path[p_i], point_path[p_i+1]))
    total_length = lengths[-1]

    # Get x, y step for each step
    render_path = []
    for step in range(numer_of_samples):
        # Get distance of step
        t = (step / (numer_of_samples)) * total_length
        
        # find the arc the step is from
        for arc in range(len(point_path)-1):
            if lengths[arc] <= t < lengths[arc+1]:
                # Linear interpolation
                p1, p2 = point_path[arc], point_path[arc+1]
                t1, t2 = lengths[arc], lengths[arc+1]
                ratio = (t - t1) / (t2 - t1)
                x = p1[0] + ratio * (p2[0] - p1[0])
                y = p1[1] + ratio * (p2[1] - p1[1])
                render_path.append((x, y))
                break
    return render_path


if __name__ == "__main__":
    print(parameterize_lines([[0, 0], [1, 1], [0, 5]]))