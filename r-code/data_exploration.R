library(sf)
library(terra)
library(dplyr)
library(ggplot2)
source("robust_mapping.R")

# -------------------
# Load data
# -------------------

# Load Chicago crimes
chicago_crimes = "data/chicago/points/chicago_crimes.shp"
crimes <- sf::read_sf(chicago_crimes)
crimes <- crimes[!st_is_empty(crimes), ]

# Load Chicago boundaries
chicago_boundaries = "data/chicago/boundaries/Chicago_City_Limits.shp"
boundaries <- sf::read_sf(chicago_boundaries)


# -------------------
# Data treatment
# -------------------

# Check if the coordinate reference systems (CRS) are the same
# If not, transform the crimes data to match the boundaries CRS
if (st_crs(crimes) != st_crs(boundaries)) {
  crimes <- st_transform(crimes, st_crs(boundaries))
}

# Create a data frame with coordinates
# st_coordinates() extracts the coordinates from the sf object
# and creates a data frame with x and y columns
crimes_df <- data.frame(
  x = st_coordinates(crimes)[,1],
  y = st_coordinates(crimes)[,2]
)


# -----------------------
# Find optimal grid size
# -----------------------

grid_size <- robust.quadcount(crimes_df, verbose=TRUE)


# --------------------------------------
# Plot uniformity and robustness curves
# --------------------------------------
point_set = crimes_df
W <- c(min(point_set[,1]),max(point_set[,1]),min(point_set[,2]),max(point_set[,2]))
maxscale <- 0.10*min(c(W[2] - W[1],W[4] - W[3]))
minscale <- maxscale*0.02
my_scales <-  seq(minscale,maxscale,minscale)

plot(my_scales, grid_size$uniformity.curve)
plot(my_scales, grid_size$robustness.curve)


# -------------------
# Counts Histogram
# -------------------
count_values <- terra::values(grid_size$counts, mat = FALSE, na.rm = TRUE)

df <- data.frame(counts = count_values)
df_filtered <- df %>% filter(counts > 0)

ggplot(df_filtered, aes(x=counts)) + geom_histogram(binwidth = 5) + theme_minimal()


# -------------------
# Counts raster
# -------------------
terra::plot(grid_size$counts, axes = TRUE)
