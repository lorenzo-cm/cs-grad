from abc import ABC, abstractmethod
from typing import Sequence, Self
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


class BoundingBoxBase(ABC):
    
    # ------------------------------
    # Properties
    # ------------------------------
    
    @property
    @abstractmethod
    def mins(self) -> Sequence[float]:
        """
        Minimum values per axis (len == 2 in 2D, len == 3 in 3D).
        Equivalent to (minx, miny) or (minx, miny, minz) in 2D/3D.
        """

    @property
    @abstractmethod
    def maxs(self) -> Sequence[float]:
        """
        Maximum values per axis (same dimension as `mins`).
        Equivalent to (maxx, maxy) or (maxx, maxy, maxz) in 2D/3D.
        """
        
    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Hypervolume measure:
          - 2D: area
          - 3D: volume
        """
        
    @property
    def area(self) -> float:
        """
        Hypervolume measure:
          - 2D: area
          - 3D: volume
        """
        return self.volume

    @property
    def ndim(self) -> int:
        """Dimensionality (derived)."""
        return len(self.mins)
    
    
    # ------------------------------
    # Constructors
    # ------------------------------
    
    @classmethod
    @abstractmethod
    def from_coords(
        cls,
        mins: Sequence[float],
        maxs: Sequence[float],
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> Self:
        """Create the bounding box from explicit coordinates."""

    @classmethod
    @abstractmethod
    def from_points(
        cls,
        points: np.ndarray,
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> Self:
        """Create the bounding box from a set of points in nD."""
        
        
    # ------------------------------
    # Utils
    # ------------------------------
    
    @dataclass
    class PointsInside:
        count: int
        points: NDArray[np.float64]

    @abstractmethod
    def points_inside(self, points: NDArray[np.float64]) -> PointsInside:
        """Return the points that are inside the bounding box."""

    @abstractmethod
    def create_random_points(self, n_points: int) -> NDArray[np.float64]:
        """Generate random points inside the bounding box."""

    @abstractmethod
    def create_random_quadrats(
        self,
        quadrat_size: float,
        n_quadrats: int,
    ) -> list[Self]:
        """Generate random quadrats (square sub-boxes) inside the bounding box."""

    @abstractmethod
    def gen_scales_from_bbox(self, size: int = 10, as_int: bool = False) -> NDArray:
        """Generate spatial analysis scales from the bounding box dimensions."""


