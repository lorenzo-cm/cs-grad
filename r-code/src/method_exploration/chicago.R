library(sf)
library(terra)
library(dplyr)
library(ggplot2)
source("/home/lorenzo-cm/faculdade/tcc/r-code/robust_mapping.R")


# -------------------
# Load data
# -------------------

load_shapefile_points <- function(shapefile_path, epsg = 3857) {
  gdf <- st_read(shapefile_path, quiet = TRUE)
  
  gdf <- gdf[!st_is_empty(gdf), ]
  if (nrow(gdf) == 0) stop("Nenhum registro válido encontrado no shapefile.")
  
  gdf <- gdf[st_geometry_type(gdf) == "POINT", ]
  if (nrow(gdf) == 0) stop("O shapefile não contém geometrias do tipo POINT.")
  
  gdf_m <- st_transform(gdf, epsg)
  
  coords <- st_coordinates(gdf_m)
  return(coords)
}

# Load Chicago crimes
chicago_crimes <- "/home/lorenzo-cm/faculdade/tcc/data/chicago/points/chicago_crimes.shp"
coords <- load_shapefile_points(chicago_crimes)

# Create a data frame with coordinates
# st_coordinates() extracts the coordinates from the sf object
# and creates a data frame with x and y columns
crimes_df <- data.frame(
  x = coords[,1],
  y = coords[,2]
)

# -----------------------
# Find optimal grid size
# -----------------------

grid_size <- robust.quadcount(crimes_df, verbose=TRUE, uniformity_method="Quadratcount")

# -----------------------
# Save results to CSV
# -----------------------

# Function to save results to CSV (similar to Python version)
save_results_to_csv <- function(optimal_scale, tradeoff_values, filename) {
  # Create data frame with scale, uniformity, robustness, and tradeoff values
  results_df <- data.frame(
    Scale = grid_size$granularities.tested,
    Uniformity = grid_size$uniformity.curve,
    Robustness = grid_size$robustness.curve,
    Tradeoff = grid_size$uniformity.curve * grid_size$robustness.curve
  )
  
  # Write the main results
  write.csv(results_df, filename, row.names = FALSE)
  
  # Append optimal scale information
  optimal_info <- data.frame(
    Scale = "Optimal Scale",
    Uniformity = optimal_scale,
    Robustness = NA,
    Tradeoff = NA
  )
}

# Save the results
output_filename <- "/home/lorenzo-cm/faculdade/tcc/r-code/results/new-metrics/chicago/chicago_grid_size_results.csv"

# Create directory if it doesn't exist
output_dir <- dirname(output_filename)
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
  cat("Created directory:", output_dir, "\n")
}

save_results_to_csv(grid_size$opt_granularity, NULL, output_filename)

cat("Results saved to:", output_filename, "\n")
cat("Optimal grid size found:", grid_size$opt_granularity, "\n")


