#!/usr/bin/env python3
"""Download actual images from GitHub repos and create dark-themed 400x400 thumbnails."""
import urllib.request
import io
import os
import numpy as np
from PIL import Image

BASE = "/home/k1/public/k1monfared.github.io"
OUT_DIR = os.path.join(BASE, "images/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)

RAW = "https://raw.githubusercontent.com/k1monfared"

def download_and_process(url, name, size=400):
    """Download image from URL, apply dark theme, save as webp thumbnail."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=15).read()
        img = Image.open(io.BytesIO(data)).convert('RGB')
        arr = np.array(img)
        # Dark theme: invert if light background
        if arr.mean() > 140:
            arr = 255 - arr
        img = Image.fromarray(arr)
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
        img = img.resize((size, size), Image.LANCZOS)
        # Vignette
        Y, X = np.ogrid[:size, :size]
        dist = np.sqrt((X - size/2)**2 + (Y - size/2)**2) / np.sqrt((size/2)**2 + (size/2)**2)
        vignette = 1 - 0.3 * dist**2
        arr2 = np.array(img, dtype=float)
        for c in range(3):
            arr2[:, :, c] *= np.clip(vignette, 0, 1)
        img = Image.fromarray(np.clip(arr2, 0, 255).astype(np.uint8))
        img.save(os.path.join(OUT_DIR, f"{name}.webp"), "WEBP", quality=85)
        print(f"  OK: {name}.webp")
        return True
    except Exception as e:
        print(f"  FAIL: {name} - {e}")
        return False

# ============================================================
# MACHINE LEARNING - 12 course folders
# ============================================================
print("=== Machine Learning ===")
ml_images = {
    'ml-01-linear-regression': f'{RAW}/machine_learning/main/01_linear_regression/linear_regression_visualization.png',
    'ml-02-logistic-regression': f'{RAW}/machine_learning/main/02_logistic_regression/logistic_regression_visualization.png',
    'ml-06-svm': f'{RAW}/machine_learning/main/06_support_vector_machines/svm_visualization.png',
    'ml-07-kmeans': f'{RAW}/machine_learning/main/07_kmeans_clustering/kmeans_visualization.png',
    'ml-08-pca': f'{RAW}/machine_learning/main/08_principal_component_analysis/pca_visualization.png',
    'ml-09-anomaly': f'{RAW}/machine_learning/main/09_anomaly_detection/anomaly_detection_visualization.png',
}
for name, url in ml_images.items():
    download_and_process(url, name)

# ============================================================
# CLUSTERING - 6 images in images/ subfolder
# ============================================================
print("\n=== Clustering ===")
clustering_images = {
    'clust-declustering': f'{RAW}/clustering/main/images/declustering.png',
    'clust-fiedler': f'{RAW}/clustering/main/images/fiedler_clustering.png',
    'clust-iterative-vs-generalized': f'{RAW}/clustering/main/images/iterative_vs_generalized_fiedler.png',
    'clust-kuramoto': f'{RAW}/clustering/main/images/kuramoto_clustering.png',
    'clust-spectral': f'{RAW}/clustering/main/images/spectral_coordinates_clustering.png',
    'clust-graph-routines': f'{RAW}/clustering/main/images/graph_routines_overview.png',
}
for name, url in clustering_images.items():
    download_and_process(url, name)

# ============================================================
# ARTS & RECREATION
# ============================================================
print("\n=== Arts & Recreation ===")
arts_images = {
    'arts-optical-illusion': f'{RAW}/arts_and_recreation/main/an_optical_illusion/output.png',
    'arts-timestable': f'{RAW}/arts_and_recreation/main/modular_timestable_graph/gallery.png',
    'arts-lissajous': f'{RAW}/arts_and_recreation/main/lissajouse_curve_table/6x6fast_loop.gif',
    'arts-random-walkers': f'{RAW}/arts_and_recreation/main/random_walkers_art/random_walker_colored_100.png',
}
for name, url in arts_images.items():
    download_and_process(url, name)

# ============================================================
# EDUCATION
# ============================================================
print("\n=== Education ===")
edu_images = {
    'edu-newtons-method': f'{RAW}/education/main/calculus/newtons_method/newtons_method_x2_1.png',
    'edu-newton-animated': f'{RAW}/education/main/calculus/newtons_method_animated/newtons_method_animated.png',
    'edu-taylor': f'{RAW}/education/main/calculus/taylor_expansion_animated_dir/taylor_sin.png',
    'edu-partial-fractions': f'{RAW}/education/main/calculus/step_by_step_partial_fraction_decomposition/output4.jpg',
    'edu-level-curves': f'{RAW}/education/main/calculus/plot3d_level_curves/plot3d_level_curves.png',
    'edu-cross-sections': f'{RAW}/education/main/calculus/plot3d_cross_sections/plot3d_cross_sections.png',
    'edu-gradient-descent': f'{RAW}/education/main/calculus/gradient_descent_for_two_variables_with_plot/gradient_descent_large.png',
    'edu-linearize-jacobian': f'{RAW}/education/main/linear_algebra/linearize_jacobian/linearize_jacobian.png',
}
for name, url in edu_images.items():
    download_and_process(url, name)

# ============================================================
# EXPERIMENTAL MATH
# ============================================================
print("\n=== Experimental Math ===")
exp_images = {
    'exp-goldbach-comet': f'{RAW}/experimental_math/main/statistical_goldbach/goldbach_comet.png',
    'exp-goldbach-minimum': f'{RAW}/experimental_math/main/statistical_goldbach/goldbach_minimum.png',
}
for name, url in exp_images.items():
    download_and_process(url, name)

# ============================================================
# STATISTICS
# ============================================================
print("\n=== Statistics ===")
stats_images = {
    'stats-balls-in-box': f'{RAW}/statistics/main/balls_in_a_box/random_walk_snapshots.png',
    'stats-causal-inference': f'{RAW}/statistics/main/causal_inference/potential_outcomes_framework.png',
}
for name, url in stats_images.items():
    download_and_process(url, name)

# ============================================================
# STATES DURING REGIME CHANGE
# ============================================================
print("\n=== States During Regime Change ===")
states_images = {
    'ds-regime-heatmap': f'{RAW}/states_during_regime_change/main/plots/readme/full_heatmap.png',
    'ds-regime-regions': f'{RAW}/states_during_regime_change/main/plots/readme/all_regions_panel.png',
    'ds-regime-violent': f'{RAW}/states_during_regime_change/main/plots/readme/violent_vs_peaceful.png',
    'ds-regime-iraq': f'{RAW}/states_during_regime_change/main/plots/readme/iraq_dimensions.png',
}
for name, url in states_images.items():
    download_and_process(url, name)

# ============================================================
# LARGE DOG BREEDS
# ============================================================
print("\n=== Large Dog Breeds ===")
dogs_images = {
    'ds-dogs-scatter': f'{RAW}/large_dog_breeds/main/charts/weight_vs_height.png',
    'ds-dogs-heatmap': f'{RAW}/large_dog_breeds/main/charts/trait_heatmap.png',
    'ds-dogs-service': f'{RAW}/large_dog_breeds/main/charts/service_dog_scores.png',
    'ds-dogs-correlation': f'{RAW}/large_dog_breeds/main/charts/correlation_matrix.png',
}
for name, url in dogs_images.items():
    download_and_process(url, name)

# ============================================================
# MAP DESIGN
# ============================================================
print("\n=== Map Design ===")
map_images = {
    'ds-map-world': f'{RAW}/map_design/main/world-map-final.png',
    'ds-map-topo': f'{RAW}/map_design/main/topo-map-initial.png',
}
for name, url in map_images.items():
    download_and_process(url, name)

# ============================================================
# DECISION THEORY (already have some, get fresh ones)
# ============================================================
print("\n=== Decision Theory ===")
dt_images = {
    'ds-mutual-info': f'{RAW}/decision_theory/main/mutual_information_joint_entropy/lag_test_python.png',
    'ds-gale-shapley': f'{RAW}/decision_theory/main/visual_gale_shapley/gale_shapley_matching.png',
}
for name, url in dt_images.items():
    download_and_process(url, name)

# ============================================================
# CODING
# ============================================================
print("\n=== Coding ===")
coding_images = {
    'ds-pandas-benchmark': f'{RAW}/coding/main/pandas-apply-vs-applymap/images/summary_comparison.png',
}
for name, url in coding_images.items():
    download_and_process(url, name)

# ============================================================
# DIFFERENCES
# ============================================================
print("\n=== Differences ===")
diff_images = {
    'ds-differences-logo': f'{RAW}/differences/main/doc/source/images/logo/bw/logo_name_bw.png',
}
for name, url in diff_images.items():
    download_and_process(url, name)

# ============================================================
# ALBERTA SCHOOLS DROPOUT
# ============================================================
print("\n=== Alberta Schools ===")
# Check if there are images in images/ subfolder
alberta_images = {
    'ds-alberta': f'{RAW}/alberta_schools_dropout/main/images/map.png',
}
for name, url in alberta_images.items():
    download_and_process(url, name)

print("\n=== ALL DONE ===")
