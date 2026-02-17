# Optimal Granularity in Python

This repository contains python code to find the optimal granularity for spatial and spatio-temporal point data based on uniformity and robustness tests.

The method is originally proposed by Ramos in the paper: [Too fine to be good? Issues of granularity, uniformity and error in spatial crime analysis](https://doi.org/10.1007/s10940-020-09474-6)

This code is a translation of the original R code provided by the author with additional features and improvements:

- Added support for spatio-temporal data (3D bounding box).
- Added a non-parametric robustness test.

## Python Implementation

In the repository, we used `numpy` for numerical computations and points representation.

The points are represented as a 2D numpy array where each row is a point in 2D space.

```py
import numpy as np

points = np.array([[1, 2], [3, 4], [5, 6]])
```

Hence, the shape of the array is `(n_points, n_dim)`.

The bounding box is represented by a class in which it is defined some useful functions. The bounding box have a base class and subclasses for 2D (spatio) and 3D (spatio-temporal) bounding boxes.

From the bounding box, we can get the scales for each dimension to find the optimal granularity. The scales are in the shape `(n_dim, scale_size)`, where `n_dim` is the number of dimensions (2 for spatio, 3 for spatio-temporal) and `scale_size` is the number of scales to evaluate.

The scales are interpreted in the following way:
- First dimension: spatial scale (x and y)
- Second dimension: any other dimension (time for spatio-temporal)
- ...

To evaluate the uniformity and robustness tests, we test each scale and compare the results to find the optimal granularity. The comparison is based on the p-values of the tests and optimized by the sum or product of the robustness and uniformity scores.

## Scales

The scales are generated using the `gen_scales_from_bbox` method of the bounding box. The method is implemented in the `utils/bounding_box/bbox_base.py` file.

It generates the scales for each dimension, but not the permutations of the scales.

The permutations of the scales are generated using the `itertools.product` function