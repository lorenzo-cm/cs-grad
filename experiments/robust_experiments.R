library(spatstat)
library(ggplot2)
library(gridExtra)
library(extraDistr)
library(dplyr)

source("./experiments/robust_functions.R")
source("./experiments/robust_utils.R")

set.seed(123)

# =========================================================
# Configure pattern
# =========================================================

# ≃ 500 points in a 1000x1000 window

win <- owin(c(0, 1000), c(0, 1000))

# Patterns

# pattern_name <- "Thomas_000025_15_20"
# pattern <- rThomas(kappa = 0.000025, scale = 15, mu = 20, win = win)
# details <- "1000x1000, kappa = 0.000025, scale = 15, mu = 20"

pattern_name <- "CSR_0005"
pattern <- rpoispp(lambda = 0.0005, win = win)
details <- "1000x1000, lambda = 0.0005"


# =========================================================
# Configure output directory
# =========================================================

out_dir <- "./results"
save_path <- file.path(out_dir, pattern_name)

if (!dir.exists(save_path)) {
    dir.create(save_path, recursive = TRUE)
}


# =========================================================
# Configure and run the experiment
# =========================================================

# Configuration
g <- 100
nsamples <- 1000
nruns <- 500

# Run the bootstrap experiment
result <- bootstrapped_entropy_score(pattern, g, nsamples, nruns, run_both = TRUE)


# =========================================================
# Export and plot results
# =========================================================

save_pattern_plot(pattern, pattern_name, save_path)


export_entropy_results(result, out_dir = save_path, pattern_name = pattern_name,
 config = list(
    g = g,
    nsamples = nsamples,
    nruns = nruns,
    additional_info = details
))

plot_entropy_results(result, save=TRUE, out_dir = save_path)
