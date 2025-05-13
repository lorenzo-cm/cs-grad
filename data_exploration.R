library(sf)
library(terra)
library(dplyr)
library(ggplot2)
source("robust_mapping.R")

# Load Chicago crimes
chicago_crimes = "data/chicago/points/chicago_crimes.shp"
crimes <- sf::read_sf(chicago_crimes)
crimes <- crimes[!st_is_empty(crimes), ]

# Load Chicago boundaries
chicago_boundaries = "data/chicago/boundaries/Chicago_City_Limits.shp"
boundaries <- sf::read_sf(chicago_boundaries)

if (st_crs(crimes) != st_crs(boundaries)) {
  crimes <- st_transform(crimes, st_crs(boundaries))
}

# Create a data frame with coordinates
crimes_df <- data.frame(
  x = st_coordinates(crimes)[,1],
  y = st_coordinates(crimes)[,2]
)

# Find the optimal grid size
grid_size <- robust.quadcount(crimes_df, verbose=TRUE)

# Create a spatial grid
grid <- st_make_grid(boundaries, cellsize = c(grid_size$opt_granularity, grid_size$opt_granularity), square = TRUE)

# Plot the map with the optimal grid
ggplot() +
  geom_sf(data = boundaries, fill = NA, color = "black") +
  geom_sf(data = grid, fill = NA, color = "blue", alpha = 0.5) +
  geom_sf(data = crimes, color = "red", size = 0.2, alpha = 0.6) +
  coord_sf(crs = st_crs(boundaries)) +
  theme_minimal() +
  ggtitle("Chicago Crimes with Optimal Grid")

# Save the plot
ggsave("chicago_crimes_optimal_grid.png", width = 10, height = 10, dpi = 300)

