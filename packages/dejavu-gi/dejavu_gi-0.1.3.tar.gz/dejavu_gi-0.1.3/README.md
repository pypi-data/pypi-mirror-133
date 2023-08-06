# Bindings to graph isomorphism solver dejavu

This package provides a basic ctypes wrapper to the graph isomorphism solver `dejavu` (https://www.mathematik.tu-darmstadt.de/dejavu). The goal of the package is to provide easy-to-use, quick access to the main functionality of `dejavu`. For performance critical software, consider using the C++ version of `dejavu` directly. 

# Features

The package exposes methods of the probabilistic graph isomorphism solver `dejavu`. The main features include easy access to a probabilistic graph isomorphism test, probabilistic computation of graph automorphisms (AKA symmetries), color refinement (AKA 1-WL) and random walks of IR trees.

# Quickstart

Once installed using pip, the package can simply be imported using `import dejavu_gi`. 

Lets assume we want to compute the symmetries of the 5-cycle. Graphs in the package are represented using the number of vertices `n` (in this case 5) and an (undirected) edgelist, in this case `[[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]`. We can then simply compute the symmetries as follows.
```
import dejavu_gi

group = dejavu_gi.get_automorphisms(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]])
print(group)
```
The above code outputs the following representation of the automorphism group:
```
{'generators': [[4, 3, 2, 1, 0], [2, 3, 4, 0, 1]], 'base': [2, 4], 'size': 10.0}
```
`generators` is a generating set of the automorphism group, whereas `base` is a base and `size` is the order of the automorphism group. Note that this computation is probabilistic. More precisely, the solver is only guaranteed to return all the symmetries with some bounded error probability (which can be set using `err`). For more precise information on this, see the code documentation.

If we want to test two graphs for isomorphism, we can do so using:
```
import dejavu_gi

is_iso1 = dejavu_gi.are_isomorphic(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 5, [[1, 0], [1, 2], [3, 2], [3, 4], [4, 0]])
is_iso2 = dejavu_gi.are_isomorphic(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 5, [[1, 0], [1, 2], [3, 2], [3, 4], [4, 1]])
print(is_iso1)
print(is_iso2)
```
The output for the above would be:
```
0
0
```

We can also use the color refinement of `dejavu`, using the following code:
```
colors = dejavu_gi.color_refinement(3, [[0, 1],[0, 2]])
print(colors)
```
This returns a mapping from vertices to colors, in the above example this is:
```
[2, 0, 0]
```
