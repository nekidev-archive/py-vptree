# py-vptree

A library to create vantage point trees in Python.

## Installation

This library has no dependencies, so you can just clone this repository or copy-paste the [__init__.py](./vptree/\_\_init\_\_.py) file into your project.

## Usage

You can create a new VP tree with the `VPTree` class:

```py
from vptree import VPTree

tree = VPTree(
    points=list(range(10000)),
    dist_fn=lambda x, y: bin(x ^ y).count("1"),
)
```

Both arguments are optional. If the `points` argument is not provided, an empty tree will be created. If the `dist_fn` argument is not provided, the default hamming distance function will be used.

The `points` arguments can be anything you want as long as it's measurable with the `dist_fn` function. The same two `dist_fn` arguments must return the same numeric distance.

The `dist_fn` takes two points as arguments and returns a positive numeric distance. E.g.:

```py
hamming = lambda x, y: bin(x ^ y).count("1")
```

## Insert a point to the tree

To insert a point to the tree, you can use the `insert` method:

```py
>>> tree.insert(2)
```

## Remove a point from the tree

To remove a point from the tree, you can use the `remove` method:

```py
>>> tree.remove(2)
```

This method won't rebuild the tree, but instead it'll promote another node to cover the space left by the removed point. No errors will be raised if the point is not in the tree.

## Search for the k-nearest neighbors

To get the k-nearest neighbors, you can use the `knn` method:

```py
>>> knn = tree.knn(query=2, k=5)
>>> knn
[(2, 0), (0, 1), (3, 1), (1, 2), (4, 2)]
```

The result will be a list of tuples, where the first element is the point and the second element is the distance from the `query`.

## Search within a radius

To search within a radius, you can use the `within` method:

```py
>>> within = tree.within(query=2, radius=2)
>>> within
[(66, 1), (3, 1), (6, 1), (18, 1), (2, 0), (34, 1), (10, 1), (0, 1)]
```

The result will be a list of tuples, where the first element is the point and the second element is the distance from the `query`. The distance of the results will be less than the `radius` (equal points aren't included).

Dislike `knn`, this method will not return points ordered by distance. If you want to order the results by distance, you can use the `sort` method:

```py
>>> within.sort(key=lambda x: x[1])
>>> within
[(2, 0), (66, 1), (3, 1), (6, 1), (18, 1), (34, 1), (10, 1), (0, 1)]
```