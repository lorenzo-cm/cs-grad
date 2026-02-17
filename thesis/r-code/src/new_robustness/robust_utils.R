library(ggplot2)
library(jsonlite)
library(dplyr)


plot_entropy_results <- function(results, save = FALSE, out_dir = NULL) {
    # Extract relative entropy statistics for plotting
    sturges_df <- data.frame(
        mean = results$sturges$relative_entropy$mean,
        sd = results$sturges$relative_entropy$std,
        cv = results$sturges$relative_entropy$cv,
        ci_lower = results$sturges$relative_entropy$confidence_interval[1],
        ci_upper = results$sturges$relative_entropy$confidence_interval[2],
        method = "Sturges"
    )
    
    unique_df <- data.frame(
        mean = results$unique$relative_entropy$mean,
        sd = results$unique$relative_entropy$std,
        cv = results$unique$relative_entropy$cv,
        ci_lower = results$unique$relative_entropy$confidence_interval[1],
        ci_upper = results$unique$relative_entropy$confidence_interval[2],
        method = "Unique"
    )
    
    combined_df <- rbind(sturges_df, unique_df)
    
    # Create the plot and store it
    p <- ggplot(combined_df, aes(x = method, y = mean)) +
        geom_bar(stat = "identity", position = position_dodge(), fill = "steelblue") +
        geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2) +
        labs(y = "Mean Relative Entropy Score", x = "Method") +
        theme_minimal()

    if (save) {
        if (is.null(out_dir)) {
            stop("Output directory must be specified when save is TRUE.")
        }
        
        # Create output directory if it doesn't exist
        if (!dir.exists(out_dir)) {
            dir.create(out_dir, recursive = TRUE)
        }
        
        # Create filename
        filename <- file.path(out_dir, "entropy_results_plot.png")
        
        # Save the plot with white background
        ggsave(filename, plot = p, width = 8, height = 6, bg = "white")
    }
    
    # Return the plot
    return(p)
}


# Export results of sturges and proposed method to json format
export_entropy_results <- function(results, out_dir, pattern_name, config) {
    # Create comprehensive structure with all entropy measures
    structured_results <- list(
        methods = list(
            Sturges = list(
                relative_entropy = list(
                    mean = results$sturges$relative_entropy$mean,
                    sd = results$sturges$relative_entropy$std,
                    cv = results$sturges$relative_entropy$cv,
                    ci_lower = results$sturges$relative_entropy$confidence_interval[1],
                    ci_upper = results$sturges$relative_entropy$confidence_interval[2]
                ),
                entropy = list(
                    mean = results$sturges$entropy$mean,
                    sd = results$sturges$entropy$std,
                    cv = results$sturges$entropy$cv,
                    ci_lower = results$sturges$entropy$confidence_interval[1],
                    ci_upper = results$sturges$entropy$confidence_interval[2]
                ),
                max_entropy = list(
                    mean = results$sturges$max_entropy$mean,
                    sd = results$sturges$max_entropy$std,
                    cv = results$sturges$max_entropy$cv,
                    ci_lower = results$sturges$max_entropy$confidence_interval[1],
                    ci_upper = results$sturges$max_entropy$confidence_interval[2]
                )
            ),
            Unique = list(
                relative_entropy = list(
                    mean = results$unique$relative_entropy$mean,
                    sd = results$unique$relative_entropy$std,
                    cv = results$unique$relative_entropy$cv,
                    ci_lower = results$unique$relative_entropy$confidence_interval[1],
                    ci_upper = results$unique$relative_entropy$confidence_interval[2]
                ),
                entropy = list(
                    mean = results$unique$entropy$mean,
                    sd = results$unique$entropy$std,
                    cv = results$unique$entropy$cv,
                    ci_lower = results$unique$entropy$confidence_interval[1],
                    ci_upper = results$unique$entropy$confidence_interval[2]
                ),
                max_entropy = list(
                    mean = results$unique$max_entropy$mean,
                    sd = results$unique$max_entropy$std,
                    cv = results$unique$max_entropy$cv,
                    ci_lower = results$unique$max_entropy$confidence_interval[1],
                    ci_upper = results$unique$max_entropy$confidence_interval[2]
                )
            )
        ),
        config = list(
            pattern = pattern_name,
            g = config$g,
            nsamples = config$nsamples,
            nruns = config$nruns,
            additional_info = ifelse(is.null(config$additional_info), NA, config$additional_info)
        )
    )
    
    # Create output directory if it doesn't exist
    if (!dir.exists(out_dir)) {
        dir.create(out_dir, recursive = TRUE)
    }
    
    # Create filename
    filename <- file.path(out_dir, paste0(pattern_name, "_entropy_results.json"))
    
    # Export to JSON with auto_unbox = TRUE to avoid arrays for single values
    jsonlite::write_json(structured_results, filename, pretty = TRUE, auto_unbox = TRUE)
    
    return(filename)
}


# Save the pattern generated by the distribution of points generated before
save_pattern_plot <- function(pattern, pattern_name, out_dir) {
    if (!dir.exists(out_dir)) {
        dir.create(out_dir, recursive = TRUE)
    }
    
    filename <- file.path(out_dir, paste0(pattern_name, "_pattern.png"))
    
    # Save the pattern plot
    png(filename, width = 800, height = 600)
    plot(pattern, main = paste("Pattern:", pattern_name))
    dev.off()
}
