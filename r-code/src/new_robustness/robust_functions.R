library(pbapply)

##############################################################################
# Entropy-based robustness score
#

bootstrapped_entropy_score <- function(pp, g, nsamples=500, nruns=100, run_both = FALSE) {
    # Runs a bootstrap over entropy_score

    if (run_both) {
        # Run bootstrap for both methods (sturges and unique)
        sturges_relative <- numeric(nruns)
        sturges_entropy <- numeric(nruns)
        sturges_max <- numeric(nruns)
        unique_relative <- numeric(nruns)
        unique_entropy <- numeric(nruns)
        unique_max <- numeric(nruns)
        
        pb <- txtProgressBar(min = 0, max = nruns, style = 3)
        for (i in 1:nruns) {
            result <- entropy_score(pp, g, nsamples, test_both = TRUE)
            sturges_relative[i] <- result$sturges$relative_entropy
            sturges_entropy[i] <- result$sturges$entropy
            sturges_max[i] <- result$sturges$max_entropy
            unique_relative[i] <- result$unique$relative_entropy
            unique_entropy[i] <- result$unique$entropy
            unique_max[i] <- result$unique$max_entropy

            setTxtProgressBar(pb, i)
        }
        close(pb)
        
        # Calculate statistics for both methods
        return(list(
            sturges = calculate_stats_full(sturges_relative, sturges_entropy, sturges_max, nruns),
            unique = calculate_stats_full(unique_relative, unique_entropy, unique_max, nruns)
        ))
        
    } else {
        # Original single method bootstrap
        relative_values <- numeric(nruns)
        entropy_values <- numeric(nruns)
        max_values <- numeric(nruns)

        pb <- txtProgressBar(min = 0, max = nruns, style = 3)
        for (i in 1:nruns) {
            result <- entropy_score(pp, g, nsamples)
            relative_values[i] <- result$relative_entropy
            entropy_values[i] <- result$entropy
            max_values[i] <- result$max_entropy

            setTxtProgressBar(pb, i)
        }
        close(pb)

        return(calculate_stats_full(relative_values, entropy_values, max_values, nruns))
    }
}


calculate_stats_full <- function(relative_values, entropy_values, max_values, nruns) {
    # Calculate statistics for all three entropy measures
    calc_measure_stats <- function(values) {
        mean_val <- mean(values, na.rm = TRUE)
        
        if (nruns == 1) {
            # When only 1 run, we can't calculate variance-based statistics
            return(list(
                mean = mean_val,
                std = 0,
                cv = 0,
                confidence_interval = c(mean_val, mean_val)
            ))
        } else {
            sd_val <- sd(values, na.rm = TRUE)
            cv_val <- if (mean_val != 0) sd_val / mean_val else 0
            se_val <- sd_val / sqrt(nruns)
            ci_lower <- mean_val - 1.96 * se_val
            ci_upper <- mean_val + 1.96 * se_val
            
            return(list(
                mean = mean_val,
                std = sd_val,
                cv = cv_val,
                confidence_interval = c(ci_lower, ci_upper)
            ))
        }
    }
    
    return(list(
        relative_entropy = calc_measure_stats(relative_values),
        entropy = calc_measure_stats(entropy_values),
        max_entropy = calc_measure_stats(max_values),
        raw_values = list(
            relative_entropy = relative_values,
            entropy = entropy_values,
            max_entropy = max_values
        ),
        n_runs = nruns
    ))
}

calculate_stats <- function(values) {
    mean_entropy <- mean(values, na.rm = TRUE)
    sd_entropy <- sd(values, na.rm = TRUE)
    cv_entropy <- sd_entropy / mean_entropy
    se_entropy <- sd_entropy / sqrt(nruns)
    ci_lower <- mean_entropy - 1.96 * se_entropy
    ci_upper <- mean_entropy + 1.96 * se_entropy
    
    return(list(
        mean_entropy = mean_entropy,
        std_entropy = sd_entropy,
        cv_entropy = cv_entropy,
        confidence_interval = c(ci_lower, ci_upper),
        raw_values = values,
        n_runs = nruns
    ))
}


# Randomly sample quadrats and obtain a count distribution. Next,
# obtain the relative entropy
entropy_score <- function(pp, g, nsamples = 500, breaks = "sturges", test_both = FALSE) {
    # Randomly sample quadrats and evaluate the entropy of the count distribution
    # Input: pp is a point pattern
    #        g is the quadrat side
    #        nsamples is the number of random quadrats
    # Output: scalar value of the entropy

    # Preallocate vector to store random counts
    counts_quadrats <- numeric(nsamples)

    # sample quadrats and count the points within
    for (i in 1:nsamples) {
        # Randomly select the bottom-left corner of a square cell of size g x g
        # Use a guard region to create neighboring cells around the target cell
        x0 <- runif(1, min = 0, max = 1000 - g)
        y0 <- runif(1, min = 0, max = 1000 - g)

        # Define the sampling cell
        cell <- owin(c(x0, x0 + g), c(y0, y0 + g))
        # Count how many points fall inside the cell
        counts_quadrats[i] <- npoints(pp[cell])
    }

    if (test_both) {
        # if test_both, we will test both methods Sturges and unique
        sturges_result <- estimate_entropy(counts_quadrats, "sturges")
        unique_result <- estimate_entropy(counts_quadrats, "unique")

        return(
            list(
                sturges = list(
                    relative_entropy = sturges_result$relative_entropy,
                    entropy = sturges_result$entropy,
                    max_entropy = sturges_result$max_entropy
                ),
                unique = list(
                    relative_entropy = unique_result$relative_entropy,
                    entropy = unique_result$entropy,
                    max_entropy = unique_result$max_entropy
                )
            )
        )
    }

    entropy <- estimate_entropy(counts_quadrats, breaks)

    return(list(
        relative_entropy = entropy$relative_entropy,
        entropy = entropy$entropy,
        max_entropy = entropy$max_entropy
    ))
}

# Function to estimate entropy using histogram-based binning
estimate_entropy <- function(x, breaks = "sturges") {

    # Compute histogram without plotting
    if (breaks == "sturges") {
        h <- hist(x, breaks = "Sturges", plot = FALSE)
        counts <- h$counts
    }

    if (breaks == "unique") {
        unique_vals <- unique(x)
        counts <- table(factor(x, levels = unique_vals))
    }
    
    total <- sum(counts)

    # Proportions -> this division is a vector division
    probs <- counts / total

    # Non-zero probabilities
    non_zero_probs <- probs[probs > 0]
    k <- length(non_zero_probs) # number of non-empty bins

    # Entropy in bits
    entropy <- -sum(non_zero_probs * log2(non_zero_probs))

    # Two options:
    #  Maximum possible entropy over k non-empty bins (uniform distribution)
    # max_entropy <- log2(k)
    # or better: consider all bins, even the empty ones (due to sampling variation)
    max_entropy <- log2(length(probs))

    # Relative entropy
    relative_entropy <- entropy / max_entropy

    return(list(
        proportions = probs,
        entropy = entropy,
        max_entropy = max_entropy,
        relative_entropy = relative_entropy
    ))
}

###########################################################################