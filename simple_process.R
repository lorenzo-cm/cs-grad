library(terra)
library(magrittr)
library(spatstat)
library(spatstat.geom)
library(spatstat.explore)
library(MASS)

# Source the robust mapping function
source("r-code/robust_mapping.R")

# Get CSV files
csv_files <- list.files("samples", pattern = "*.csv", full.names = TRUE)

# Process each file and save separately
for (file in csv_files) {
  cat("Processing:", basename(file), "\n")
  
  # Read data
  data <- read.csv(file)
  point_set <- data.frame(x = data[,1], y = data[,2])
  point_set <- point_set[complete.cases(point_set), ]
  
  # Extract file name without extension
  file_name <- tools::file_path_sans_ext(basename(file))

    result <- robust.quadcount(point_set, verbose = FALSE)
    
    # Create results for this file only
    file_results <- data.frame(
      scale = result$granularities.tested,
      uniformity = result$uniformity.curve,
      robustness = result$robustness.curve,
      optimal_granularity = result$opt_granularity
    )
    
    # Save to separate CSV file
    output_file <- paste0(file_name, "_results.csv")
    write.csv(file_results, output_file, row.names = FALSE)
    
    cat("  Optimal granularity:", result$opt_granularity, "\n")
    cat("  Saved to:", output_file, "\n")
    
    cat("\n")
}
