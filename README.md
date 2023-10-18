# py-vptree

A library to create vantage point trees in Python.

## Installation

This library has no dependencies, so you can just clone this repository or copy-paste the [__init__.py](./vptree/__init__.py) file into your project.

## Usage

You can import the library from `vptree`. You'll probably only use the `VPTree` class inside it.

```py
import vptree

tree = vptree.VPTree(
    initial=list(range(1000)),                  # Must be a list
    dist_fn=lambda x, y: bin(x ^ y).count("1")  # This is the default
)
```

The `initial` argument must be a list. It can contain anything inside it. The `dist_fn` must be a callable that takes in two arguments and returns an integer (the distance between the two arguments). The same arguments must return the same distance.

To get the `n` nearest points, use the `.search()` method:

```py
tree.search(query=100, limit=10)
# [(0, 100), (1, 36), (3, 20), (3, 0), (1, 68), (4, 2), (5, 24), (5, 3), (3, 12), (4, 1)]
```

The results aren't ordered, but you can easily sort them using the built-in `sorted()` function.

```py
results = tree.search(100, 10)
sorted(results)
# [(0, 100), (1, 36), (1, 68), (3, 0), (3, 12), (3, 20), (4, 1), (4, 2), (5, 3), (5, 24)]
```

To get all the points within a certain distance from another point, you can use the `radius()` method:

```py
tree.radius(query=100, distance=5)
# [(2, 4), (2, 37), (2, 38), (2, 69), (2, 70), (1, 36), (1, 68), (0, 100), (2, 164), (2, 292), ...]
```

You can sort the results the same way you did with the `search()` method.