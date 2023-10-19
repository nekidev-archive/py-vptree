# py-vptree

A library to create vantage point trees in Python.

## Installation

You can install this library from PyPI:

```shell
pip install py-vptree
```

> [WARNING!]
> This library has only been tested with Python 3.11. It may not work with other versions of Python.
> Contributors are encouraged to test it with other versions of Python.

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

### Get all points in the tree

To get all points in the tree, you can use the `.all()` method:

```py
>>> sorted(list(tree.all()))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
```

The method returns a generator that yields all points in the tree (unordered).

### Insert a point to the tree

To insert a point to the tree, you can use the `insert` method:

```py
>>> tree.insert(2)
```

### Remove a point from the tree

To remove a point from the tree, you can use the `remove` method:

```py
>>> tree.remove(2)
```

This method won't rebuild the tree, but instead it'll promote another node to cover the space left by the removed point. No errors will be raised if the point is not in the tree.

### Count the number of points in the tree

To count the number of points in the tree, you can use the `len` built-in function:

```py
>>> len(tree)
10000
```

### Search for the k-nearest neighbors

To get the k-nearest neighbors, you can use the `knn` method:

```py
>>> knn = tree.knn(query=2, k=5)
>>> knn
[(2, 0), (0, 1), (3, 1), (1, 2), (4, 2)]
```

The result will be a list of tuples, where the first element is the point and the second element is the distance from the `query`.

### Search within a radius

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

### Custom points and distance function

The examples above use plain integers and a simple hamming distance function, but you can use the tree however you need it.

<details>
    <summary>Example using named tuples</summary>

```py
import random
import collections

from vptree import VPTree


Item = collections.namedtuple("Item", ["id", "value"])

tree = VPTree(
    points=[
        Item(id=i, value=random.randint(0, 10000)) for i in range(10000)
    ],
    dist_fn=lambda x, y: bin(x[1] ^ y[1]).count("1"),
)

tree.knn((2, 2), 5)
# [(Item(id=4885, value=8322), 2), (Item(id=3622, value=22), 2), (Item(id=8197, value=8195), 2), (Item(id=9380, value=4610), 2), (Item(id=984, value=7), 2)]
```
</details>

<details>
    <summary>Example using euclidean distance</summary>

```py
from math import sqrt

import random
import collections

from vptree import VPTree


Item = collections.namedtuple("Item", ["id", "value"])

tree = VPTree(
    points=[
        Item(id=i, value=random.uniform(0, 10000)) for i in range(10000)
    ],
    dist_fn=lambda x, y: sqrt((x[1] - y[1]) ** 2),
)

tree.knn((2, 2), 5)
# [(Item(id=7562, value=235.7541538751584), 233.7541538751584), (Item(id=5077, value=235.89421426943758), 233.89421426943758), (Item(id=5772, value=235.92818023762007), 233.92818023762007), (Item(id=6621, value=236.29613677601412), 234.29613677601412), (Item(id=6293, value=238.94108967773886), 236.94108967773886)]
```
</details>