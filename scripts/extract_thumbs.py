#!/usr/bin/env python3
"""
Extract representative figures from PDFs and create dark-themed 400x400 thumbnails.
"""
import fitz  # PyMuPDF
import os
import sys
from PIL import Image, ImageOps, ImageFilter, ImageDraw
import io
import numpy as np

BASE = "/home/k1/public/k1monfared.github.io"
OUT_DIR = os.path.join(BASE, "images/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)

DARK_BG = (17, 17, 17)  # matches website dark theme
SIZE = 400


def extract_best_image_from_pdf(pdf_path, min_size=100):
    """Extract the best (largest, most complex) image from a PDF."""
    doc = fitz.open(pdf_path)
    best_img = None
    best_score = 0

    for page_num in range(min(len(doc), 15)):  # check first 15 pages
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_info in images:
            xref = img_info[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 4:  # not CMYK
                    pass
                else:
                    pix = fitz.Pixmap(fitz.csRGB, pix)  # convert CMYK to RGB

                if pix.width < min_size or pix.height < min_size:
                    continue

                # Score: prefer larger images with more color variety
                score = pix.width * pix.height
                # Bonus for images that aren't too narrow (aspect ratio close to 1)
                ar = min(pix.width, pix.height) / max(pix.width, pix.height)
                score *= (0.5 + 0.5 * ar)
                # Slight penalty for very early pages (often logos)
                if page_num == 0:
                    score *= 0.8

                if score > best_score:
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    # Skip if nearly all white or all one color
                    arr = np.array(img)
                    if arr.std() < 10:
                        continue
                    best_img = img
                    best_score = score
            except Exception:
                continue

    doc.close()
    return best_img


def render_best_page(pdf_path, skip_first=False):
    """Render the page with the most visual content as a fallback."""
    doc = fitz.open(pdf_path)
    best_page = None
    best_score = 0
    start = 1 if skip_first else 0

    for page_num in range(start, min(len(doc), 10)):
        page = doc[page_num]
        # Count images and drawings on page
        images = page.get_images(full=True)
        drawings = page.get_drawings()
        text_blocks = page.get_text("blocks")

        # Score pages with more visual elements
        score = len(images) * 100 + len(drawings) * 10 + len(text_blocks)
        # Bonus for pages with images
        if len(images) > 0:
            score *= 3

        if score > best_score:
            best_score = score
            best_page = page_num

    if best_page is None:
        best_page = min(1, len(doc) - 1)

    page = doc[best_page]
    mat = fitz.Matrix(2, 2)  # 2x zoom for quality
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    doc.close()
    return img


def make_dark_thumb(img, size=SIZE):
    """Convert an image to a dark-themed 400x400 thumbnail."""
    if img is None:
        return None

    arr = np.array(img.convert("RGB"))

    # Check if image is predominantly light (white background paper)
    mean_brightness = arr.mean()

    if mean_brightness > 160:
        # Light image: invert to dark theme
        # First, detect if it's a figure with colored elements
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        color_variance = np.std(r.astype(float) - g.astype(float)) + \
                        np.std(g.astype(float) - b.astype(float))

        if color_variance > 15:
            # Has colors - invert brightness but try to preserve hues
            from colorsys import rgb_to_hsv, hsv_to_rgb
            # Simple approach: invert the lightness
            # Convert to float
            farr = arr.astype(float) / 255.0
            # Invert: dark becomes light, light becomes dark
            inverted = 1.0 - farr
            # Boost saturation slightly
            img_inv = Image.fromarray((inverted * 255).astype(np.uint8))
            img = img_inv
        else:
            # Mostly black and white - simple invert
            img = ImageOps.invert(img.convert("RGB"))
    elif mean_brightness > 120:
        # Medium brightness - darken background
        arr_float = arr.astype(float)
        # Darken light areas more than dark areas
        mask = arr_float.mean(axis=2) > 200
        arr_float[mask] = arr_float[mask] * 0.1
        img = Image.fromarray(arr_float.astype(np.uint8))

    # Crop to center square
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    # Resize to target
    img = img.resize((size, size), Image.LANCZOS)

    # Add slight vignette for polish
    img = add_vignette(img)

    return img


def make_dark_thumb_from_page(img, size=SIZE):
    """For full-page renders: crop to the most interesting region, then dark-theme it."""
    if img is None:
        return None

    w, h = img.size
    arr = np.array(img.convert("RGB"))

    # Find the region with the most "content" (non-white pixels)
    gray = np.mean(arr, axis=2)
    # Mark non-white pixels
    content = gray < 240

    # Find bounding box of content
    rows = np.any(content, axis=1)
    cols = np.any(content, axis=0)
    if rows.any() and cols.any():
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]

        # Add padding
        pad = 20
        rmin = max(0, rmin - pad)
        rmax = min(h - 1, rmax + pad)
        cmin = max(0, cmin - pad)
        cmax = min(w - 1, cmax + pad)

        # Crop to content region
        img = img.crop((cmin, rmin, cmax, rmax))

    return make_dark_thumb(img, size)


def add_vignette(img, strength=0.3):
    """Add a subtle vignette effect."""
    w, h = img.size
    arr = np.array(img, dtype=float)

    # Create radial gradient
    Y, X = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    dist = dist / max_dist  # normalize to 0-1

    # Smooth falloff
    vignette = 1 - strength * (dist ** 2)
    vignette = np.clip(vignette, 0, 1)

    # Apply
    for c in range(3):
        arr[:, :, c] *= vignette
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def process_pdf(pdf_path, output_name, prefer_extracted=True):
    """Process a PDF and save a dark-themed thumbnail."""
    out_path = os.path.join(OUT_DIR, output_name + ".webp")

    if not os.path.exists(pdf_path):
        print(f"  SKIP (not found): {pdf_path}")
        return False

    print(f"  Processing: {os.path.basename(pdf_path)}")

    thumb = None

    if prefer_extracted:
        # Try extracting embedded images first
        img = extract_best_image_from_pdf(pdf_path)
        if img is not None:
            thumb = make_dark_thumb(img)
            print(f"    -> Extracted image: {img.size}")

    if thumb is None:
        # Fallback: render best page
        img = render_best_page(pdf_path, skip_first=True)
        if img is not None:
            thumb = make_dark_thumb_from_page(img)
            print(f"    -> Rendered page")

    if thumb is not None:
        thumb.save(out_path, "WEBP", quality=85)
        print(f"    -> Saved: {out_path}")
        return True
    else:
        print(f"    -> FAILED: no usable content")
        return False


# ============================================================
# MANIFEST: All PDFs referenced in math-and-cs subpages
# ============================================================

RESEARCH = os.path.join(BASE, "research")
TALKS = os.path.join(BASE, "research/talks")

# Papers & patent PDFs (that DON'T already have thumbnails, or we want to regenerate)
PAPER_PDFS = {
    # data-science patent
    "ds-patent-ai-audiences": os.path.join(RESEARCH,
        "2021_US11113707_Artificial_intelligence_identification_of_high-value_audiences.pdf"),
    # matrix-theory: max multiplicity (has webp but not linked)
    "mat-max-multiplicity": os.path.join(RESEARCH,
        "2016_The_maximum_multiplicity_of_an_eigenvalue_of_symmetric_matrices_with_a_given_graph.pdf"),
    # All existing paper thumbs - regenerate in case they need dark theme update
    "mat-matrix-tree": os.path.join(RESEARCH,
        "2018_An_analog_of_Matrix_Tree_Theorem_for_signless_Laplacians.pdf"),
    "mat-infinite-graphs": os.path.join(RESEARCH,
        "2018_A_structured_inverse_spectrum_problem_for_infinite_graphs.pdf"),
    "mat-nonsymmetric": os.path.join(RESEARCH,
        "2017_Existence_of_a_not_necessarily_symmetric_matrix_with_given_distinct_eigenvalues_and_graph.pdf"),
    "mat-nowhere-zero": os.path.join(RESEARCH,
        "2016_The_nowhere-zero_eigenbasis_problem_for_a_graph.pdf"),
    "mat-lambda-tau": os.path.join(RESEARCH,
        "2015_The_lambda-tau_structured_inverse_eigenvalue_problem.pdf"),
    "mat-interlaced": os.path.join(RESEARCH,
        "2013_Construction_of_matrices_with_a_given_graph_and_prescribed_interlaced_spectral_data.pdf"),
    "mat-nowhere-zero-vectors": os.path.join(RESEARCH,
        "2010_On_the_existence_of_nowhere-zero_vectors_for_linear_transformations.pdf"),
    "mat-vibrating": os.path.join(RESEARCH,
        "Inverse_spectral_problems_for_linked_vibrating_systems_and_structured_matrix_polynomials.pdf"),
    # graph-theory
    "gt-perrank": os.path.join(RESEARCH,
        "2016_On_the_principal_permanent_rank_characteristic_sequences_of_graphs_and_digraphs.pdf"),
    "gt-matchings": os.path.join(RESEARCH,
        "2016_Spectral_characterization_of_matchings_in_graphs.pdf"),
    "gt-skew-symmetric": os.path.join(RESEARCH,
        "2015_Construction_of_real_skew-symmetric_matrices_from_interlaced_spectral_data,_and_graph.pdf"),
    # neuroscience
    "neuro-community": os.path.join(RESEARCH,
        "Community_structure_detection_and_evaluation_during_preictal_and_postictal_hippocampal_depth_recordings.pdf"),
    # theses
    "thesis-phd": os.path.join(RESEARCH,
        "2014_The_Jacobian_Method_The_Art_Of_Finding_More_Needles_in_Nearby_Haystacks_(PhD_dissertation).pdf"),
    "thesis-msc": os.path.join(RESEARCH,
        "2012_On_the_Permanent_Conjecture_(Masters_thesis).pdf"),
}

# Talk slides PDFs
TALK_PDFS = {
    "talk-canadam-2019": os.path.join(TALKS, "201906_Vancouver_CanaDAM.pdf"),
    "talk-cms-2019": os.path.join(RESEARCH, "201906_Regina_CMS.pdf"),
    "talk-perrank": os.path.join(TALKS, "Perrank.pdf"),
    "talk-phd-defense": os.path.join(TALKS, "PhD-Defense.pdf"),
    "talk-lambda-mu-long": os.path.join(TALKS, "lambda-mu-long.pdf"),
    "talk-lambda-mu-short": os.path.join(TALKS, "lambda-mu-short.pdf"),
    "talk-lambda-tau": os.path.join(TALKS, "lambda-tau.pdf"),
    "talk-tektalk": os.path.join(TALKS, "the_role_of_intention_and_initiative.pdf"),
}

if __name__ == "__main__":
    print("=== Extracting figures from paper/patent PDFs ===")
    for name, path in PAPER_PDFS.items():
        process_pdf(path, name)

    print("\n=== Extracting figures from talk slides ===")
    for name, path in TALK_PDFS.items():
        process_pdf(path, name, prefer_extracted=False)

    print("\nDone!")
