library(ggplot2)
library(jsonlite)
library(dplyr)

plot_entropy_results <- function(results, save = FALSE, out_dir = NULL) {
    sturges_df <- data.frame(
        mean = results$sturges$mean_entropy,
        sd = results$sturges$std_entropy,
        cv = results$sturges$cv_entropy,
        ci_lower = results$sturges$confidence_interval[1],
        ci_upper = results$sturges$confidence_interval[2],
        method = "Sturges"
    )
    
    unique_df <- data.frame(
        mean = results$unique$mean_entropy,
        sd = results$unique$std_entropy,
        cv = results$unique$cv_entropy,
        ci_lower = results$unique$confidence_interval[1],
        ci_upper = results$unique$confidence_interval[2],
        method = "Unique"
    )
    
    combined_df <- rbind(sturges_df, unique_df)
    
    ggplot(combined_df, aes(x = method, y = mean)) +
        geom_bar(stat = "identity", position = position_dodge(), fill = "steelblue") +
        geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2) +
        labs(y = "Mean Entropy Score", x = "Method") +
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
        
        # Save the plot
        ggsave(filename, width = 8, height = 6, bg = "white")

    }
}

export_entropy_results <- function(results, out_dir, pattern_name, config) {
    # Create the same dataframe structure as in plot_entropy_results
    structured_results <- list(
        Sturges = list(
            mean = results$sturges$mean_entropy,
            sd = results$sturges$std_entropy,
            cv = results$sturges$cv_entropy,
            ci_lower = results$sturges$confidence_interval[1],
            ci_upper = results$sturges$confidence_interval[2],
            pattern = pattern_name,
            g = config$g,
            nsamples = config$nsamples,
            nruns = config$nruns,
            additional_info = ifelse(is.null(config$additional_info), NA, config$additional_info)
        ),
        Unique = list(
            mean = results$unique$mean_entropy,
            sd = results$unique$std_entropy,
            cv = results$unique$cv_entropy,
            ci_lower = results$unique$confidence_interval[1],
            ci_upper = results$unique$confidence_interval[2],
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
    
    # Export to JSON
    jsonlite::write_json(structured_results, filename, pretty = TRUE, auto_unbox = TRUE)
    
    return(filename)
}


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