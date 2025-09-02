from tabnanny import verbose
from typing import Literal
import pandas as pd
import numpy as np
from pathlib import Path

from .main import uniformity
from ..utils import BoundingBox, gen_scales_from_bbox


# Parameters for uniformity calculation
num_random_quadrats = 200
signif = 0.99
method: Literal["clark_evans", "quadrat_count"] = "quadrat_count"
verbose = True

# Define paths
root_folder = Path(__file__).parent.parent.parent.parent  # Navigate to tcc folder
samples_folder = root_folder / "samples"
output_folder = Path(__file__).parent.parent / "test" / "uniformity" / method  # py-code/optimal_granularity/test/

csv_files = list(samples_folder.glob("*.csv"))

output_folder.mkdir(exist_ok=True, parents=True)

for csv_file in csv_files:
    print(f"Processing {csv_file.name}...")
    
    df = pd.read_csv(csv_file)
    
    # Extract points (assuming columns are 'x' and 'y')
    points = df[['x', 'y']].values
    
    bbox = BoundingBox.from_points(points)
    scales = gen_scales_from_bbox(bbox, size=40)
    
    # Calculate uniformity
    uniformity_values = uniformity(
        points=points,
        scales=scales,
        num_random_quadrats=num_random_quadrats,
        bbox=bbox,
        signif=signif,
        method=method,
        verbose=verbose,
    )
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'scale': scales,
        'uniformity': uniformity_values
    })
    
    # Save results
    output_filename = csv_file.stem + "_uniformity_results_quadrat_count.csv"
    output_path = output_folder / output_filename
    results_df.to_csv(output_path, index=False)
    
    print(f"Saved results to {output_path}")
        

print("Processing complete!")
