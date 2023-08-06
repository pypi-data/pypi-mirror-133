# [machine-parts-pp](https://bitbucket.org/Bakkelund/machine-parts-pp/)

# Planted partitions over machine part structures

This python module offers data and functionality to generate planted partitions over directed acyclic graphs with dissimilarities. The directed acyclic graphs represent machine parts, where the vertices are parts, and the edges are "part-of" relations. The planted partitions simulate a copy-paste scenario where a machine (graph) is duplicated, but the parts (vertices) are given new identifiers, and the copy-relation is forgotten. The planted partitions represent the copy-paste links, and the presented problem is to recover the planted partition from the family of graphs and the dissimilarities.

The machine parts data is extracted from a large database of subsea oil and gas machinery owned by TechnipFMC ([https://www.technipfmc.com/](https://www.technipfmc.com/)), and the dissimilarities are obtained from an in-company data science project using machine learning to develop a similarity measure over the machine parts calculated from metadata.

For a detailed description of the data and the planted partition generation mechanism, please see the article _Machine part data with part-of relations and part dissimilarities for planted partition generation_.

## Requirements
* `python 3+`
* `numpy`

## License
The software in this module is licensed under the GNU Lesser General Public License ([https://www.gnu.org/licenses/lgpl-3.0.en.html](https://www.gnu.org/licenses/lgpl-3.0.en.html)).

## Installation
`python -m pip install machine-parts-pp [--user]`

## How to get hold of the data

The data can be obtained either as files at [Mendeley Data](https://data.mendeley.com/):

<https://data.mendeley.com/datasets/dhhxzdzm3v/1>

Or they can be obtained through the python API as follows:

```python
import machine_parts_pp as pp

parts = pp.get_all_machine_parts()
dists = pp.get_all_dissimilarities()
```

In the above code, `parts` is a `dict` mapping a part id (integer) to a list of part-ids, namely to the list of directly contained parts. That is; `b`is a *part of* `a` if `b in parts[a]`.
The object `dists` is a symmetric `N x N` `numpy` array holding the pairwise dissimilarities of all the machine parts.

However, if the goal is to use the data to generate clustering problems, the following sections give a description of how the APIs can be used for this.

## Examples involving planted partitions

The below examples demonstrate how to 

1. Obtain a generated problem instance together with a planted partition.
2. Solve the problem using a library for clustering. We provide two examples, one using [dbscan](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html), and one example using [ophac](https://bitbucket.org/Bakkelund/ophac/wiki/Home).
3. Evaluate the quality of the solution by computing the adjusted Rand index relative the planted partition. We employ the python library [clusim](https://github.com/Hoosier-Clusters/clusim) for this computation.

### Obtaining a problem instance with a planted partition

We start by obtaining the problem instance and the planted partition

```python
import machine_parts_pp as pp

# number of copy-paste operations
mult=5

# The base data before copy-pasting
base = pp.get_all_machine_parts()

# mean and variance of the noise to be added to the dissimilarity data
mean = 0.05
var  = 0.15

# Generate the problem and obtain the planted partition
graph, dissims, planted_partition = pp.planted_partition(base,mult,mean,var)
```
We now have

* `graph` - a dict on the form (`x,[y1,y2,...])` where `x` is an integer and `[y1,...]` are the "parts of" `x`, i.e. the descendants of `x` when we consider `graph` to be a directed acyclic graph.
* `dissims` - An `NxN` `numpy` array with pair-wise dissimilarities of the vertices in graph. All dissimilarities are in the range `[0,1]`.
* `planted_partition` - A list of lists, each list a cluster, and each cluster a collection of copy-paste pairs. 

We can now use this for testing and benchmarking of algorithms that take `(graph,dissims)` as input and try to use this information to recover `planted_partition`.

The following two examples continue by first clustering the data, and then evaluate the result by computing the adjusted rand index. 

### Using DBSCAN for clustering

This example requires the python modules `sklern` and `clusim` to be installed.<br/>
The full source can be downloaded via this link:
[example_dbscan.py](https://bitbucket.org/Bakkelund/machine-parts-pp/src/master/python/example/example_dbscan.py)

```python
from sklearn.cluster import DBSCAN

# Use dbscan to cluster, using 3 as the core point threshold (min_samples),
# and specifying metric='precomputed', since we have pre-computed dissimilarities
dbscan     = DBSCAN(eps=0.085, min_samples=3, metric='precomputed')
clustering = dbscan.fit(dissims)

# number of clusters
nClusters = max(*clustering.labels_)+1

# extracting the physical clusters
nElts    = len(graph)
clusters = [[] for _ in range(nClusters)]
for elt in range(nElts):
    clusters[clustering.labels_[elt]].append(elt)

# We can now compare the 'clustering' clusters with the 'planted_partition'
# clusters to evaluate the degree of precision in recovering the planted
# partition
#
# We have chosen to use the library 'clusim', which requires the clustering to
# be represented by a dict mapping (eltId,clustId)
# See the documentaton of clusim for details.

import clusim.clustering
import clusim.sim

# Planted partition clustering representation
pp_cluster_idx = pp.clustering_to_cluster_index_mapping(planted_partition)
pp_dict = {x : [pp_cluster_idx[x]] for x in range(nElts)}
pp_clst = clusim.clustering.Clustering(elm2clu_dict=pp_dict)

# dbscan clustering representation
db_dict = {x : [clustering.labels_[x]] for x in range(nElts)}
db_clst = clusim.clustering.Clustering(elm2clu_dict=db_dict)

# Since the dbscan clustering is not pre-set to have a fixed number of clusters,
# we consider the clustering to be "drawn" from the family of all clusterings
ari = clusim.sim.adjrand_index(db_clst, pp_clst, 'all1')

print('Adjusted Rand index:', ari)
```

### Using ophac for clustering

`ophac` is a library that is tailored especially for clustering of directed acyclic graphs (see [https://bitbucket.org/Bakkelund/ophac/wiki/Home](https://bitbucket.org/Bakkelund/ophac/wiki/Home) for details).<br/>
This example requires the python modules `ophac` and `clusim` to be installed.<br/>
The full source can be downloaded via this link:
[example_ophac.py](https://bitbucket.org/Bakkelund/machine-parts-pp/src/master/python/example/example_ophac.py)

```python
# We now cluster the elements using order preserving clustering through the
# ophac library. See the documentation of ophac for details.

import ophac.hierarchy       as hc
import ophac.dtypes          as dt

# Formatting the part-of relations as required by ophac
N = len(graph)
Q = [sorted(graph[x]) for x in range(N)]

# Formatting the dissimilarity as required by ophac
D = []
for i in range(N):
    for j in range(i+1,N):
        D.append(dissims[i,j])

# Run the ophac approximation algorithm
ac = hc.approx_linkage(D,Q,'complete')

# Plotting the merge dissimilarities to find the location of the
# so called knee. Inspection of the below plot shows that a useful 
# cutoff may be at about 150 merges --> we extract the clustering 
# at this point
import matplotlib.pyplot as plt
nCut = 150
plt.plot(ac[0].dists, label='merges')
plt.plot([nCut],[ac[0].dists[nCut]], c='red', marker='o',
         label=('cut at %d merges' % nCut))
plt.legend()
plt.title('Choosing to cut at %d merges based on inspection' % nCut)
plt.show()

# Using ophac libraries to extract the clustering at nCut merges
cutoff_partition = dt.merge(dt.Partition(n=N),ac[0].joins[:nCut])
clusters         = cutoff_partition.data

# We can now compare the 'clusters' with the 'planted_partition'
# to evaluate the degree of precision in recovering the planted partition.
#
# We have chosen to use the library 'clusim', which requires the clustering to
# be represented by a dict mapping (eltId,clustId)
# See the documentaton of clusim for details.

import clusim.clustering
import clusim.sim

# Planted partition clusim representation
pp_cluster_idx = pp.clustering_to_cluster_index_mapping(planted_partition)
pp_dict = {x : [pp_cluster_idx[x]] for x in range(N)}
pp_clst = clusim.clustering.Clustering(elm2clu_dict=pp_dict)

# ophac clustering clusim representation
db_cluster_idx = pp.clustering_to_cluster_index_mapping(clusters)
db_dict = {x : [db_cluster_idx[x]] for x in range(N)}
db_clst = clusim.clustering.Clustering(elm2clu_dict=db_dict)

# Since the ophac clustering is not pre-set to have a fixed number of clusters,
# we consider the clustering to be "drawn" from the family of all clusterings
ari = clusim.sim.adjrand_index(db_clst, pp_clst, 'all1')

print('Adjusted Rand index:', ari)
```

###Repository

The source code for this `python` module is available at
<https://bitbucket.org/Bakkelund/machine-parts-pp/>