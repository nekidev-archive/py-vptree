import sys
import heapq
import statistics


def hamming(a: int, b: int) -> int:
    """Calculate the hamming distance between two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The hamming distance between the two integers.
    """
    return bin(a ^ b).count("1")


class Node(object):
    """A node in the VPTree."""

    point: object
    threshold: int
    inside: "Node" = None
    outside: "Node" = None

    def __init__(
        self, point: object, dist_fn: callable, subitems: list
    ) -> None:
        self.point = point

        if len(subitems) == 0:
            self.threshold = 0
            return

        distances = [(dist_fn(self.point, d), d) for d in subitems]
        self.threshold = statistics.median([d[0] for d in distances])

        inside = [d[1] for d in distances if d[0] <= self.threshold]
        outside = [d[1] for d in distances if d[0] > self.threshold]

        if len(inside):
            self.inside = Node(inside.pop(0), dist_fn, inside)

        if len(outside):
            self.outside = Node(outside.pop(0), dist_fn, outside)

    def __len__(self) -> int:
        return (len(self.inside) + 1 if self.inside is not None else 0) + (
            len(self.outside) + 1 if self.outside is not None else 0
        )

    def __repr__(self) -> str:
        return f"Node(point={self.point!r})"


class VPTree(object):
    """A vantage point tree.

    Args:
        dist_fn (callable): The distance function to use. It takes two arguments and returns an integer.
    """

    vantage_point: Node | None = None

    def __init__(self, initial: list, dist_fn: callable = hamming) -> None:
        self.dist_fn = dist_fn

        if len(initial) == 0:
            return

        vp_choice = initial.pop(0)

        distances = [self.dist_fn(vp_choice, d) for d in initial]
        self.threshold = statistics.median(distances)

        # Update the system's recursion limit to the length of the initial list
        # so that the recursion limit is not exceeded.
        recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(len(initial))

        self.vantage_point = Node(vp_choice, dist_fn, initial)
        
        # Restore the system's default recursion limit.
        sys.setrecursionlimit(recursion_limit)

    def search(self, query: object, limit: int = 10) -> list:
        """Returns the `limit` nearest points to `query`.

        Args:
            query (object): The query point.
            limit (int, optional): The number of nearest points. Defaults to 10.

        Returns:
            list: The `limit` nearest points to `query`.
        """

        if not self.vantage_point:
            return []

        nearest_neighbors = []

        def node_search(node):
            if node is None:
                return

            distance = self.dist_fn(query, node.point)
            
            if len(nearest_neighbors) < limit:
                heapq.heappush(nearest_neighbors, (distance, node.point))
            elif distance < nearest_neighbors[0][0]:
                heapq.heappop(nearest_neighbors)
                heapq.heappush(nearest_neighbors, (distance, node.point))
            
            if distance <= node.threshold:
                node_search(node.inside)
            
            if distance < node.threshold or len(nearest_neighbors) < limit:
                node_search(node.outside)

        node_search(self.vantage_point)

        return nearest_neighbors

    def radius(self, query: object, radius: int) -> list:
        """Returns all points within `radius` of `query`.

        Args:
            query (object): The query point.
            radius (int): The maximum distance.

        Returns:
            list: All points within `radius` of `query`.
        """

        if self.vantage_point is None:
            return list()

        def node_search(node):
            points = []

            d = self.dist_fn(query, node.point)
            if d <= radius:
                points.append((d, node.point))

            if node.inside and d - radius <= node.threshold:
                points += node_search(node.inside)

            if node.outside and d + radius >= node.threshold:
                points += node_search(node.outside)

            return points

        return node_search(self.vantage_point)

    def __len__(self) -> int:
        return len(self.vantage_point) + 1 if self.vantage_point is not None else 0

    def __repr__(self) -> str:
        return f"VPTree(vantage_point={self.vantage_point!r}, threshold={self.threshold!r}, dist_fn={self.dist_fn!r})"
