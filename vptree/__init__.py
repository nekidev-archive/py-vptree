"""
py-vptree

Authors: Nyeki <hello@nyeki.dev>
License: MIT

Copyright (c) 2022 Nyeki
"""

import sys
import typing
import secrets
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
    threshold: int = 0
    inside: "Node" = None
    outside: "Node" = None

    def __init__(self, point: object, dist_fn: callable, subitems: list) -> None:
        self.point = point

        if len(subitems) == 0:
            self.threshold = 0
            return

        distances = [(dist_fn(self.point, d), d) for d in subitems]
        self.threshold = statistics.median([d[0] for d in distances])

        inside = [d[1] for d in distances if d[0] <= self.threshold]
        outside = [d[1] for d in distances if d[0] > self.threshold]

        if len(inside):
            inside_choice = secrets.choice(inside)
            inside.remove(inside_choice)
            self.inside = Node(inside_choice, dist_fn, inside)

        if len(outside):
            outside_choice = secrets.choice(outside)
            outside.remove(outside_choice)
            self.outside = Node(outside_choice, dist_fn, outside)
        
    def insert(self, point: object, dist_fn: callable) -> None:
        distance = dist_fn(self.point, point)

        if distance < self.threshold:
            if self.inside is None:
                self.inside = Node(point, dist_fn, [])
            else:
                self.inside.insert(point, dist_fn)
        else:
            if self.outside is None:
                self.outside = Node(point, dist_fn, [])
            else:
                self.outside.insert(point, dist_fn)

    def __len__(self) -> int:
        return (len(self.inside) + 1 if self.inside is not None else 0) + (
            len(self.outside) + 1 if self.outside is not None else 0
        )

    def __repr__(self) -> str:
        return f"Node(point={self.point!r}, threshold={self.threshold!r})"


class VPTree(object):
    """A vantage point tree.

    Args:
        dist_fn (callable): The distance function to use. It takes two arguments and returns an integer.
    """

    vantage_point: typing.Union[Node, None] = None
    threshold: int = 0

    def __init__(self, points: list = list(), dist_fn: callable = hamming) -> None:
        self.dist_fn = dist_fn

        if len(points) == 0:
            return

        vp_choice = secrets.choice(points)
        points.remove(vp_choice)

        # Update the system's recursion limit to the length of the initial list
        # so that the recursion limit is not exceeded.
        recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(len(points))

        self.vantage_point = Node(vp_choice, dist_fn, points)

        # Restore the system's default recursion limit.
        sys.setrecursionlimit(recursion_limit)

    def knn(
        self, query: object, k: typing.Union[int, float]
    ) -> typing.List[typing.Tuple[object, typing.Union[int, float]]]:
        """Returns the k nearest neighbors to `query`.

        Args:
            query (_type_): The query point.
            k (int): The number of neighbors to return.

        Returns:
            list[tuple[object, int | float]]: A list of the k nearest neighbors to `query`. Each neighbor is a tuple of `(point, distance)`
        """

        if self.vantage_point is None:
            return []

        tau = float("inf")
        to_search = [self.vantage_point]

        results = []

        while to_search:
            current_node = to_search.pop(0)
            dist = self.dist_fn(query, current_node.point)

            if dist < tau:
                results.append((current_node.point, dist))

                if len(results) > k:
                    results.sort(key=lambda node: node[1])
                    results.pop()
                    tau = self.dist_fn(query, results[-1][0])

            if dist < current_node.threshold + tau:
                if current_node.outside is not None:
                    to_search.append(current_node.outside)

            if dist >= current_node.threshold - tau:
                if current_node.inside is not None:
                    to_search.append(current_node.inside)

        return results

    def within(
        self, point: object, radius: typing.Union[int, float]
    ) -> typing.List[typing.Tuple[object, typing.Union[int, float]]]:
        """Returns all points within `radius` of `point`.

        Args:
            point (object): The point point.
            radius (int): The maximum distance.

        Returns:
            list[tuple[object, int | float]]: All points within `radius` of `point`.
        """

        if self.vantage_point is None:
            return []

        def search(node, point, tau, results):
            if node is None:
                return

            distance = self.dist_fn(point, node.point)

            if distance < tau:
                results.append((node.point, distance))

            if distance < node.threshold + tau:
                search(node.inside, point, tau, results)

            if distance >= node.threshold - tau:
                search(node.outside, point, tau, results)

        tau = radius
        results = []
        search(self.vantage_point, point, tau, results)
        return results

    def insert(self, point: object) -> None:
        """Insert a point into the tree.

        Args:
            point (object): The point to insert.
        """

        if self.vantage_point is None:
            self.vantage_point = Node(point, self.dist_fn, [])
            return

        self.vantage_point.insert(point, self.dist_fn)

    def remove(self, point: object) -> None:
        """Remove a point from the tree.

        Args:
            point (object): The point to remove.
        """

        def remove_from_node(node, point):
            if node is None:
                return None, False

            if node.point == point:
                if node.inside:
                    replacement_point, _ = node.inside.get_nearest_neighbor(node.point)
                    node.point = replacement_point
                    node.inside.remove_point(point)
                else:
                    return None, True
            elif point <= node.threshold:
                node.inside, _ = remove_from_node(node.inside, point)
            else:
                node.outside, _ = remove_from_node(node.outside, point)
            
            if node.inside and node.outside:
                node.threshold = max(node.inside.threshold, node.outside.threshold)
            elif node.inside:
                node.threshold = node.inside.threshold
            elif node.outside:
                node.threshold = node.outside.threshold
            else:
                node.threshold = 0

            return node, False

        self.vantage_point, _ = remove_from_node(self.vantage_point, point)

    def __len__(self) -> int:
        return len(self.vantage_point) + 1 if self.vantage_point is not None else 0

    def __repr__(self) -> str:
        return f"VPTree(vantage_point={self.vantage_point!r}, dist_fn={self.dist_fn!r})"
