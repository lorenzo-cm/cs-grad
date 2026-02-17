library(sf)
library(terra)
library(dplyr)
library(ggplot2)
source("r-code/robust_mapping.R")

# Get CSV files
csv_files <- list.files("samples", pattern = "*.csv", full.names = TRUE)

# Process each file and save separately
for (file in csv_files) {
    file_name <- basename(file)
    file_name_without_ext <- tools::file_path_sans_ext(file_name)

    cat("Processing:", file_name, "\n")
    
    # Read data
    data <- read.csv(file)

    point_set <- data.frame(x = data[,1], y = data[,2])

    result <- robust.quadcount(point_set, uniformity_method='Quadratcount', verbose = FALSE)
        
    # Create results for this file only
    file_results <- data.frame(
        scale = result$granularities.tested,
        uniformity = result$uniformity.curve,
        robustness = result$robustness.curve,
        optimal_granularity = result$opt_granularity
    )
    
    # Save to separate CSV file in uniformity folder
    output_file <- file.path("r-code/results/test/uniformity", paste0(file_name, "_results.csv"))
    write.csv(file_results, output_file, row.names = FALSE)
    
    cat("  Optimal granularity:", result$opt_granularity, "\n")
    cat("  Saved to:", output_file, "\n")
    
    cat("\n")
}
