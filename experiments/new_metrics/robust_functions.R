library(pbapply)

##############################################################################
# Entropy-based robustness score
#

bootstrapped_entropy_score <- function(pp, g, nsamples=500, nruns=100, run_both = FALSE) {
    # Runs a bootstrap over entropy_score

    if (run_both) {
        # Run bootstrap for both methods (sturges and unique)
        sturges_values <- numeric(nruns)
        unique_values <- numeric(nruns)
        
        pb <- txtProgressBar(min = 0, max = nruns, style = 3)
        for (i in 1:nruns) {
            result <- entropy_score(pp, g, nsamples, test_both = TRUE)
            sturges_values[i] <- result$sturges
            unique_values[i] <- result$unique

            setTxtProgressBar(pb, i)
        }
        close(pb)
        
        # Calculate statistics for both methods
        return(list(
            sturges = calculate_stats(sturges_values),
            unique = calculate_stats(unique_values)
        ))
        
    } else {
        # Original single method bootstrap
        entropy_values <- numeric(nruns)

        pb <- txtProgressBar(min = 0, max = nruns, style = 3)
        for (i in 1:nruns) {
            entropy_values[i] <- entropy_score(pp, g, nsamples)

            setTxtProgressBar(pb, i)
        }
        close(pb)

        return(calculate_stats(entropy_values))
    }
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
        return(
            list(
                sturges = estimate_entropy(counts_quadrats, "sturges")$relative_entropy,
                unique =  estimate_entropy(counts_quadrats, "unique" )$relative_entropy
            )
        )
    }

    return(estimate_entropy(counts_quadrats, breaks)$relative_entropy)
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

    # Proportions
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
        relative_entropy = relative_entropy
    ))
}

###########################################################################