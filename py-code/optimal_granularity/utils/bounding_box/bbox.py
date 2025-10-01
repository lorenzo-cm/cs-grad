from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray


@dataclass
class BoundingBox:
    minx: float
    miny: float
    maxx: float
    maxy: float
    area: float

    def __str__(self):
        return f"BoundingBox(minx={self.minx}, miny={self.miny}, maxx={self.maxx}, maxy={self.maxy}, area={self.area}, width={self.maxx - self.minx}, height={self.maxy - self.miny})"

    @classmethod
    def from_coords(
        cls,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBox":
        minx -= margin
        maxx += margin
        miny -= margin
        maxy += margin

        range_x = maxx - minx
        range_y = maxy - miny

        if range_x < eps or range_y < eps:
            raise ValueError(
                "Bounding box has zero area. Points may be too close or identical."
            )

        area = range_x * range_y

        return cls(minx=minx, miny=miny, maxx=maxx, maxy=maxy, area=area)


    @classmethod
    def from_points(
        cls, points: np.ndarray, eps: float = 1e-12, margin: float = 1e-6
    ) -> "BoundingBox":
        """
        Build axis-aligned bounding box of a 2D point set.
        Returns BoundingBox with coordinates and area.

        Args:
            points: Array of shape (n_points, 2) with point coordinates
            eps: Minimum dimension to avoid zero-area box
            margin: Small increment added to extremes to avoid boundary conflicts

        Returns:
            BoundingBox object with coordinates and area
        """
        if points.ndim != 2 or points.shape[1] != 2:
            raise ValueError("points must be array (n,2).")
        if points.shape[0] < 2:
            raise ValueError("Need at least 2 points.")

        minx = float(points[:, 0].min()) - margin
        maxx = float(points[:, 0].max()) + margin
        miny = float(points[:, 1].min()) - margin
        maxy = float(points[:, 1].max()) + margin

        range_x = maxx - minx
        range_y = maxy - miny

        if range_x < eps or range_y < eps:
            raise ValueError(
                "Bounding box has zero area. Points may be too close or identical."
            )

        area = range_x * range_y

        return cls(minx=minx, miny=miny, maxx=maxx, maxy=maxy, area=area)


    def points_inside(self, points: NDArray[np.float64]):
        """
        Check which points are inside the bounding box.

        Args:
            points: Array of shape (n_points, 2) with point coordinates

        Returns:
            PointsInside object with boolean mask and count of points inside
        """ 
        inside_x = (points[:, 0] >= self.minx) & (points[:, 0] < self.maxx)
        inside_y = (points[:, 1] >= self.miny) & (points[:, 1] < self.maxy)
        inside_quadrat = inside_x & inside_y

        points_inside = points[inside_quadrat]
        num_points_inside = points_inside.shape[0]

        return PointsInside(count=num_points_inside, points=points_inside)
    
    
    def create_random_points(
        self,
        n_points: int) -> NDArray[np.float64]:
        """
        Generate random points within the bounding box.
        
        Args:
            bbox: BoundingBox object defining the sampling area
            n_points: Number of points to generate
            
        Returns:
            Array of shape (n_points, 2) with x, y coordinates
        """
        # Generate random x coordinates within bbox
        x_coords = np.random.uniform(self.minx, self.maxx, n_points)
        
        # Generate random y coordinates within bbox
        y_coords = np.random.uniform(self.miny, self.maxy, n_points)
        
        # Stack coordinates into (n_points, 2) array
        points = np.column_stack((x_coords, y_coords))
        
        return points
    
    
    def create_random_quadrats(
        self,
        quadrat_size: float,
        n_quadrats: int) -> list["BoundingBox"]:
        """
        Generate random quadrat positions for sampling within the bounding box.
        
        Args:
            quadrat_size: Size of the quadrat (assuming square quadrats)
            bbox: BoundingBox object defining the sampling area
            n_quadrats: Number of random quadrats to generate
            
        Returns:
            List of BoundingBox objects representing the quadrats
        """
        # Calculate available space for quadrat placement
        # Quadrat must fit entirely within the bounding box
        max_x = self.maxx - quadrat_size
        max_y = self.maxy - quadrat_size
        
        if max_x < self.minx or max_y < self.miny:
            raise ValueError("Quadrat size is too large for the bounding box")
        
        # Generate random bottom-left corner positions
        offset_x = np.random.uniform(self.minx, max_x, n_quadrats)
        offset_y = np.random.uniform(self.miny, max_y, n_quadrats)
        
        # Create list of BoundingBox objects for each quadrat
        quadrat_bboxes = []
        for i in range(n_quadrats):
            minx = offset_x[i]
            miny = offset_y[i]
            maxx = minx + quadrat_size
            maxy = miny + quadrat_size
            area = quadrat_size * quadrat_size
            
            quadrat_bbox = BoundingBox(
                minx=minx,
                miny=miny,
                maxx=maxx,
                maxy=maxy,
                area=area
            )
            quadrat_bboxes.append(quadrat_bbox)
        
        return quadrat_bboxes
    
    def gen_scales_from_bbox(
        self,
        size: int = 10,
        as_int: bool = False) -> NDArray:
        """
        Generate a range of scales for spatial analysis based on bounding box.
        
        Args:
            bbox: BoundingBox object containing the study area bounds
            size: Number of scales to generate
            as_int: If True, round scales to integers; if False, keep as floats
            
        Returns:
            Array of scales ranging from start to stop values
            
        Notes:
            - stop = 0.5 * min_side: Maximum scale at 50% of study min side to ensure coverage
            - start = 0.05 * stop: Minimum scale at 5% of maximum to avoid overly fine granularity
        """
        # 1000x1000 = 1_000_000
        # stop = 1000 * 0.35 = 350
        # start = 350 * 0.1 = 35
        
        min_side = min(self.maxx - self.minx, self.maxy - self.miny)
        stop = 0.5 * min_side
        start = 0.025 * stop
        scales = np.linspace(start, stop, size)
        
        if as_int:
            scales = np.round(scales).astype(int)
            scales = np.unique(scales)
        
        return scales
        

    
@dataclass
class PointsInside:
    count: int
    points: NDArray[np.float64]