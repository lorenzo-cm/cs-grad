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

# pattern_name <- "CSR_0005"
# pattern <- rpoispp(lambda = 0.0005, win = win)
# details <- "1000x1000, lambda = 0.0005"

# pattern_name <- "CSR_0005_THOMAS_000025_15_20"
# patternT <- rThomas(kappa = 0.000025, scale = 15, mu = 20, win = win)
# patternC <- rpoispp(lambda = 0.0005, win = win)
# pattern <- superimpose(patternC, patternT)
# details <- "1000x1000, Thomas: kappa = 0.000025, scale = 15, mu = 20, CSR: lambda = 0.0005"

# pattern_name <- "MULTI_THOMAS"
# p1 <- rThomas(kappa = 0.00005, scale = 30, mu = 15, win = win)
# p2 <- rThomas(kappa = 0.0001, scale = 10, mu = 10, win = win)
# pattern <- superimpose(p1, p2)
# details <- "1000x1000, Thomas1: kappa = 0.00005, scale = 30, mu = 15; Thomas2: kappa = 0.0001, scale = 10, mu = 10"

pattern_name <- "COMPLEX_MULTI"
p1 <- rThomas(kappa = 0.00003, scale = 50, mu = 25, win = win)
p2 <- rMatClust(kappa = 0.0001, scale = 20, mu = 12, win = win)
p3 <- rSSI(r = 35, n = 150, win = win)
lambda_gradient <- function(x, y) {
    cx <- 500; cy <- 500
    r <- sqrt((x - cx)^2 + (y - cy)^2)
    base <- 0.0001
    peak <- 0.0008
    return(base + peak * exp(-r/200))
}
p4 <- rpoispp(lambda_gradient, win = win)
win_corner <- owin(c(700, 1000), c(700, 1000))
p5 <- rHardcore(beta = 0.005, R = 12, W = win_corner)
pattern <- superimpose(p1, p2, p3, p4, p5)
details <- paste(
    "1000x1000, Complex pattern with:",
    "Thomas (kappa=0.00003, scale=50, mu=25),",
    "Matérn (kappa=0.0001, scale=20, mu=12),",
    "SSI (r=35, n=150),",
    "Gradient Poisson (radial, center=(500,500)),",
    "Hardcore corner (beta=0.005, R=12, region=700-1000)"
)



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
