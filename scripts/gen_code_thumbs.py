#!/usr/bin/env python3
"""
Generate unique dark-themed 400x400 thumbnails for all code items and
remaining items without individual thumbnails.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import io

BASE = "/home/k1/public/k1monfared.github.io"
OUT_DIR = os.path.join(BASE, "images/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)

DARK_BG = '#111111'
ACCENT_COLORS = ['#4fc3f7', '#81c784', '#ffb74d', '#e57373', '#ba68c8', '#4dd0e1', '#fff176']

def setup_dark_fig(figsize=(4, 4)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.tick_params(colors='#888888', labelsize=7)
    for spine in ax.spines.values():
        spine.set_color('#333333')
    return fig, ax

def save_thumb(fig, name, size=400):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    # Center crop to square
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"{name}.webp")
    img.save(out_path, "WEBP", quality=85)
    print(f"  Saved: {name}.webp")

def process_existing_image(img_path, name, size=400):
    """Convert an existing image to dark-themed thumbnail."""
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    if arr.mean() > 140:
        arr = 255 - arr
    img = Image.fromarray(arr)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)
    # Add vignette
    arr = np.array(img, dtype=float)
    Y, X = np.ogrid[:size, :size]
    cx, cy = size / 2, size / 2
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2) / np.sqrt(cx**2 + cy**2)
    vignette = 1 - 0.3 * (dist ** 2)
    for c in range(3):
        arr[:,:,c] *= np.clip(vignette, 0, 1)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    out_path = os.path.join(OUT_DIR, f"{name}.webp")
    img.save(out_path, "WEBP", quality=85)
    print(f"  Saved: {name}.webp (from existing image)")


# ============================================================
# ML CODE ITEMS
# ============================================================
print("=== Machine Learning code thumbnails ===")

# ML from scratch (Octave) - neural network
def gen_ml_octave():
    fig, ax = setup_dark_fig()
    np.random.seed(42)
    layers = [3, 5, 4, 2]
    positions = []
    for i, n in enumerate(layers):
        x = i / (len(layers) - 1)
        ys = np.linspace(0.2, 0.8, n)
        positions.append([(x, y) for y in ys])
    # Draw connections
    for i in range(len(layers) - 1):
        for p1 in positions[i]:
            for p2 in positions[i + 1]:
                w = np.random.uniform(0.1, 0.8)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                       color=ACCENT_COLORS[0], alpha=w * 0.4, linewidth=0.5)
    # Draw nodes
    for i, layer in enumerate(positions):
        for x, y in layer:
            circle = plt.Circle((x, y), 0.025, color=ACCENT_COLORS[i % len(ACCENT_COLORS)],
                              zorder=5)
            ax.add_patch(circle)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Neural Network', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-ml-octave')

gen_ml_octave()

# ML Python - regression with learning curve
def gen_ml_python():
    fig, ax = setup_dark_fig()
    np.random.seed(7)
    x = np.linspace(0, 10, 50)
    y = 2 * x + 1 + np.random.normal(0, 2, 50)
    ax.scatter(x, y, color=ACCENT_COLORS[0], s=15, alpha=0.7, zorder=3)
    # Fit line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), color=ACCENT_COLORS[3], linewidth=2, zorder=4)
    # Confidence band
    ax.fill_between(x, p(x) - 3, p(x) + 3, color=ACCENT_COLORS[3], alpha=0.1)
    ax.set_xlabel('x', color='#888888', fontsize=8)
    ax.set_ylabel('y', color='#888888', fontsize=8)
    ax.set_title('Linear Regression', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-ml-python')

gen_ml_python()

# Clustering - cluster visualization
def gen_clustering():
    fig, ax = setup_dark_fig()
    np.random.seed(12)
    centers = [(2, 2), (6, 6), (2, 7), (7, 2)]
    colors = [ACCENT_COLORS[0], ACCENT_COLORS[1], ACCENT_COLORS[2], ACCENT_COLORS[4]]
    for (cx, cy), c in zip(centers, colors):
        pts = np.random.randn(40, 2) * 0.8 + [cx, cy]
        ax.scatter(pts[:, 0], pts[:, 1], color=c, s=12, alpha=0.7)
        ax.plot(cx, cy, 'x', color=c, markersize=12, markeredgewidth=2)
    ax.set_title('K-Means Clustering', color='#cccccc', fontsize=10, pad=5)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    save_thumb(fig, 'code-clustering')

gen_clustering()

# Statistics - distribution plots
def gen_statistics():
    fig, ax = setup_dark_fig()
    np.random.seed(5)
    x = np.linspace(-4, 4, 200)
    for i, (mu, sig) in enumerate([(0, 1), (-1, 0.5), (1, 1.5)]):
        y = np.exp(-0.5 * ((x - mu) / sig) ** 2) / (sig * np.sqrt(2 * np.pi))
        ax.fill_between(x, y, alpha=0.3, color=ACCENT_COLORS[i])
        ax.plot(x, y, color=ACCENT_COLORS[i], linewidth=1.5)
    ax.set_title('Distributions', color='#cccccc', fontsize=10, pad=5)
    ax.set_xlim(-4, 4)
    save_thumb(fig, 'code-statistics')

gen_statistics()

# Movie recommendation - matrix heatmap
def gen_recommender():
    fig, ax = setup_dark_fig()
    np.random.seed(99)
    M = np.random.choice([0, 1, 2, 3, 4, 5], size=(8, 10), p=[0.4, 0.1, 0.1, 0.1, 0.15, 0.15])
    mask = np.random.random((8, 10)) > 0.6
    M_masked = np.ma.array(M.astype(float), mask=mask)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('dark', ['#111111', '#4fc3f7', '#81c784', '#ffb74d'])
    ax.imshow(M_masked, cmap=cmap, aspect='auto', interpolation='nearest')
    ax.set_xlabel('Items', color='#888888', fontsize=8)
    ax.set_ylabel('Users', color='#888888', fontsize=8)
    ax.set_title('Collaborative Filtering', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-recommender')

gen_recommender()

# ============================================================
# DATA SCIENCE CODE ITEMS
# ============================================================
print("\n=== Data Science code thumbnails ===")

# Decision theory
def gen_decision_theory():
    fig, ax = setup_dark_fig()
    np.random.seed(8)
    t = np.linspace(0, 10, 500)
    signal = np.sin(2 * t) + 0.5 * np.sin(5 * t)
    noise = np.random.normal(0, 0.3, len(t))
    ax.plot(t, signal + noise, color=ACCENT_COLORS[0], alpha=0.5, linewidth=0.5)
    ax.plot(t, signal, color=ACCENT_COLORS[2], linewidth=2)
    # Decision threshold
    ax.axhline(y=0.8, color=ACCENT_COLORS[3], linestyle='--', linewidth=1, alpha=0.7)
    ax.set_title('Signal Detection', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-decision-theory')

gen_decision_theory()

# Alberta schools dropout
def gen_alberta_dropout():
    fig, ax = setup_dark_fig()
    np.random.seed(3)
    categories = ['K-3', '4-6', '7-9', '10-12']
    vals1 = [95, 93, 88, 82]
    vals2 = [96, 94, 90, 85]
    x = np.arange(len(categories))
    ax.bar(x - 0.15, vals1, 0.3, color=ACCENT_COLORS[0], alpha=0.8, label='2015')
    ax.bar(x + 0.15, vals2, 0.3, color=ACCENT_COLORS[1], alpha=0.8, label='2016')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='#888888', fontsize=7)
    ax.set_ylim(75, 100)
    ax.legend(fontsize=7, facecolor=DARK_BG, edgecolor='#333333', labelcolor='#cccccc')
    ax.set_title('School Retention Rate', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-alberta-dropout')

gen_alberta_dropout()

# ============================================================
# NEUROSCIENCE CODE ITEMS
# ============================================================
print("\n=== Neuroscience code thumbnails ===")

# Graph analysis routines
def gen_graph_analysis():
    fig, ax = setup_dark_fig()
    np.random.seed(42)
    n = 20
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)
    # Draw edges
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.random() > 0.7:
                w = np.random.uniform(0.3, 1.0)
                ax.plot([x[i], x[j]], [y[i], y[j]], color=ACCENT_COLORS[0],
                       alpha=w * 0.4, linewidth=0.5)
    # Draw nodes with centrality-based size
    sizes = np.random.uniform(50, 200, n)
    ax.scatter(x, y, s=sizes, c=sizes, cmap='cool', zorder=5, edgecolors='#333333', linewidth=0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Network Analysis', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-graph-analysis')

gen_graph_analysis()

# Kuramoto clustering
def gen_kuramoto():
    fig, ax = setup_dark_fig()
    np.random.seed(15)
    t = np.linspace(0, 20, 500)
    n_osc = 8
    freqs = np.random.uniform(0.5, 2, n_osc)
    phases = np.random.uniform(0, 2 * np.pi, n_osc)
    for i in range(n_osc):
        # Kuramoto-like: oscillators synchronize over time
        coupling = 0.3
        effective_freq = freqs[i] * np.exp(-coupling * t / 10)
        signal = np.sin(effective_freq[:, None] * t[None, :] if False else effective_freq * t + phases[i])
        color_idx = 0 if freqs[i] < 1.2 else (1 if freqs[i] < 1.6 else 2)
        ax.plot(t, signal, color=ACCENT_COLORS[color_idx], alpha=0.6, linewidth=0.8)
    ax.set_title('Oscillator Synchronization', color='#cccccc', fontsize=10, pad=5)
    ax.set_xlabel('Time', color='#888888', fontsize=8)
    save_thumb(fig, 'code-kuramoto')

gen_kuramoto()

# ============================================================
# MATRIX THEORY CODE ITEMS
# ============================================================
print("\n=== Matrix Theory code thumbnails ===")

# Lambda solver for all graphs
def gen_lambda_solver():
    fig, ax = setup_dark_fig()
    np.random.seed(1)
    # Draw a graph with labeled eigenvalues
    n = 6
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / 2
    x = np.cos(angles) * 0.6
    y = np.sin(angles) * 0.6
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,3),(1,4)]
    for i, j in edges:
        ax.plot([x[i], x[j]], [y[i], y[j]], color='#555555', linewidth=1.5)
    ax.scatter(x, y, s=120, color=ACCENT_COLORS[0], zorder=5, edgecolors='white', linewidth=0.5)
    # Show eigenvalues below
    evals = [-2.0, -1.0, 0.0, 0.5, 1.5, 3.0]
    ax.axhline(y=-0.9, color='#333333', linewidth=0.5)
    for i, ev in enumerate(evals):
        xp = -0.5 + i * 0.2
        ax.plot(xp, -0.9, '|', color=ACCENT_COLORS[2], markersize=10, markeredgewidth=2)
        ax.text(xp, -1.05, f'{ev}', color='#888888', fontsize=5, ha='center')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.2, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('λ-SIEP Solver', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-lambda-solver')

gen_lambda_solver()

# Lambda-mu solver for trees
def gen_lambda_mu():
    fig, ax = setup_dark_fig()
    # Draw a tree
    nodes = {0: (0.5, 0.8), 1: (0.2, 0.5), 2: (0.8, 0.5), 3: (0.1, 0.2), 4: (0.3, 0.2), 5: (0.7, 0.2), 6: (0.9, 0.2)}
    edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
    for i, j in edges:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]], color='#555555', linewidth=2)
    for idx, (x, y) in nodes.items():
        ax.plot(x, y, 'o', color=ACCENT_COLORS[1], markersize=12, zorder=5)
    # Spectrum bars
    lambdas = [-2, -1, 0, 1, 2, 3, 4]
    mus = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
    for i, l in enumerate(lambdas):
        ax.plot(0.1 + i * 0.11, -0.1, '|', color=ACCENT_COLORS[0], markersize=15, markeredgewidth=2)
    for i, m in enumerate(mus):
        ax.plot(0.15 + i * 0.12, -0.25, '|', color=ACCENT_COLORS[3], markersize=10, markeredgewidth=1.5)
    ax.text(0.05, -0.05, 'λ', color=ACCENT_COLORS[0], fontsize=9)
    ax.text(0.05, -0.2, 'μ', color=ACCENT_COLORS[3], fontsize=9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.35, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('λ-μ Tree Solver', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-lambda-mu')

gen_lambda_mu()

# Lambda-tau solver for trees
def gen_lambda_tau_code():
    fig, ax = setup_dark_fig()
    # Star graph
    n = 6
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cx, cy = 0.5, 0.55
    r = 0.3
    for a in angles:
        x, y = cx + r * np.cos(a), cy + r * np.sin(a)
        ax.plot([cx, x], [cy, y], color='#555555', linewidth=2)
        ax.plot(x, y, 'o', color=ACCENT_COLORS[4], markersize=10, zorder=5)
    ax.plot(cx, cy, 'o', color=ACCENT_COLORS[2], markersize=14, zorder=5)
    # Interlacing spectrum
    lambdas = np.array([-2, -1, 0, 0.5, 1.5, 2, 3])
    taus = np.array([-1.5, -0.3, 0.3, 1, 1.8, 2.5])
    xbase = np.linspace(0.1, 0.9, len(lambdas))
    for i, l in enumerate(lambdas):
        ax.plot(xbase[i], 0.05, '^', color=ACCENT_COLORS[0], markersize=8)
    xbase2 = np.linspace(0.13, 0.87, len(taus))
    for i, t in enumerate(taus):
        ax.plot(xbase2[i], -0.05, 'v', color=ACCENT_COLORS[5], markersize=6)
    ax.text(0.02, 0.05, 'λ', color=ACCENT_COLORS[0], fontsize=9, va='center')
    ax.text(0.02, -0.05, 'τ', color=ACCENT_COLORS[5], fontsize=9, va='center')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.15, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('λ-τ Tree Solver', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-lambda-tau')

gen_lambda_tau_code()

# Polynomial lambda solver
def gen_poly_lambda():
    fig, ax = setup_dark_fig()
    x = np.linspace(-3, 3, 200)
    # Characteristic polynomial
    p = x**4 - 5*x**2 + 4
    ax.plot(x, p, color=ACCENT_COLORS[0], linewidth=2)
    ax.axhline(y=0, color='#444444', linewidth=0.5)
    roots = [-2, -1, 1, 2]
    ax.scatter(roots, [0]*4, color=ACCENT_COLORS[3], s=60, zorder=5)
    ax.fill_between(x, p, 0, where=(p < 0), color=ACCENT_COLORS[0], alpha=0.1)
    ax.set_title('Polynomial λ-SIEP', color='#cccccc', fontsize=10, pad=5)
    ax.set_ylim(-8, 15)
    save_thumb(fig, 'code-poly-lambda')

gen_poly_lambda()

# Full matrix constructor
def gen_full_matrix():
    fig, ax = setup_dark_fig()
    np.random.seed(7)
    M = np.random.uniform(-3, 3, (5, 5))
    # Make it look like a nowhere-zero matrix
    M[M == 0] = 0.1
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('bwr_dark', ['#e57373', '#111111', '#4fc3f7'])
    ax.imshow(M, cmap=cmap, interpolation='nearest')
    for i in range(5):
        for j in range(5):
            ax.text(j, i, f'{M[i,j]:.1f}', ha='center', va='center', color='white', fontsize=7)
    ax.set_title('Nowhere-Zero Matrix', color='#cccccc', fontsize=10, pad=5)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    save_thumb(fig, 'code-full-matrix')

gen_full_matrix()

# Combinatorial matrix theory
def gen_comb_matrix():
    fig, ax = setup_dark_fig()
    np.random.seed(2)
    n = 5
    # Adjacency pattern
    A = np.zeros((n, n))
    edges = [(0,1),(0,2),(1,2),(2,3),(3,4),(1,4)]
    for i, j in edges:
        A[i, j] = A[j, i] = 1
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('dark2', ['#111111', '#4fc3f7'])
    ax.imshow(A, cmap=cmap, interpolation='nearest')
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{int(A[i,j])}', ha='center', va='center', color='white' if A[i,j] else '#333333', fontsize=9)
    ax.set_title('Adjacency Matrix', color='#cccccc', fontsize=10, pad=5)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    save_thumb(fig, 'code-comb-matrix')

gen_comb_matrix()

# Experimental math
def gen_experimental_math():
    fig, ax = setup_dark_fig()
    # Mandelbrot-like fractal (Julia set)
    xmin, xmax, ymin, ymax = -2, 2, -2, 2
    res = 400
    x = np.linspace(xmin, xmax, res)
    y = np.linspace(ymin, ymax, res)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    c = -0.7 + 0.27015j
    M = np.zeros(Z.shape)
    for i in range(50):
        mask = np.abs(Z) < 4
        Z[mask] = Z[mask]**2 + c
        M[mask] = i
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('fractal',
        ['#111111', '#1a237e', '#4fc3f7', '#81c784', '#ffb74d', '#111111'])
    ax.imshow(M, cmap=cmap, extent=[xmin, xmax, ymin, ymax])
    ax.axis('off')
    ax.set_title('Julia Set', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-experimental-math')

gen_experimental_math()

# Laplacian eigenvalue problems
def gen_laplacian():
    fig, ax = setup_dark_fig()
    np.random.seed(3)
    # Spectrum of a Laplacian
    n = 10
    evals = sorted([0] + list(np.random.uniform(0.5, 8, n - 1)))
    ax.stem(range(n), evals, linefmt=ACCENT_COLORS[0], markerfmt='o', basefmt='#333333')
    ax.set_xlabel('Index', color='#888888', fontsize=8)
    ax.set_ylabel('Eigenvalue', color='#888888', fontsize=8)
    ax.set_title('Laplacian Spectrum', color='#cccccc', fontsize=10, pad=5)
    # Color the markers
    for line in ax.get_children():
        if hasattr(line, 'set_markerfacecolor'):
            line.set_markerfacecolor(ACCENT_COLORS[0])
            line.set_markeredgecolor(ACCENT_COLORS[0])
    save_thumb(fig, 'code-laplacian')

gen_laplacian()

# ============================================================
# GRAPH THEORY CODE ITEMS
# ============================================================
print("\n=== Graph Theory code thumbnails ===")

# Inverse eigenvalue solvers (graph-theory variant)
def gen_gt_iev_solver():
    fig, ax = setup_dark_fig()
    np.random.seed(10)
    # Petersen-like graph
    outer = [(np.cos(a), np.sin(a)) for a in np.linspace(0, 2*np.pi, 5, endpoint=False)]
    inner = [(0.5*np.cos(a + np.pi/5), 0.5*np.sin(a + np.pi/5)) for a in np.linspace(0, 2*np.pi, 5, endpoint=False)]
    nodes = outer + inner
    edges_outer = [(i, (i+1)%5) for i in range(5)]
    edges_inner = [(5+i, 5+(i+2)%5) for i in range(5)]
    edges_cross = [(i, 5+i) for i in range(5)]
    all_edges = edges_outer + edges_inner + edges_cross
    for i, j in all_edges:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]], color='#555555', linewidth=1.5)
    for i, (x, y) in enumerate(nodes):
        c = ACCENT_COLORS[0] if i < 5 else ACCENT_COLORS[1]
        ax.plot(x, y, 'o', color=c, markersize=10, zorder=5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Graph Spectrum', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-gt-iev')

gen_gt_iev_solver()

# Permanents and cycle analysis
def gen_permanents():
    fig, ax = setup_dark_fig()
    np.random.seed(6)
    # Directed graph with cycles
    n = 6
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / 2
    x = np.cos(angles) * 0.7
    y = np.sin(angles) * 0.7
    dir_edges = [(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,3)]
    for i, j in dir_edges:
        dx = x[j] - x[i]
        dy = y[j] - y[i]
        ax.annotate('', xy=(x[j], y[j]), xytext=(x[i], y[i]),
                   arrowprops=dict(arrowstyle='->', color=ACCENT_COLORS[2], lw=1.5))
    # Highlight cycles
    cycle1 = [0, 1, 2, 0]
    cycle2 = [3, 4, 5, 3]
    for cycle, color in [(cycle1, ACCENT_COLORS[3]), (cycle2, ACCENT_COLORS[4])]:
        cx_arr = [x[i] for i in cycle]
        cy_arr = [y[i] for i in cycle]
        ax.fill(cx_arr, cy_arr, color=color, alpha=0.15)
    for i in range(n):
        ax.plot(x[i], y[i], 'o', color=ACCENT_COLORS[0], markersize=12, zorder=5)
        ax.text(x[i], y[i], str(i+1), color='white', fontsize=7, ha='center', va='center', zorder=6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Directed Cycles', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-permanents')

gen_permanents()

# ============================================================
# SHELL/BASH
# ============================================================
print("\n=== Shell code thumbnail ===")

def gen_shell():
    fig, ax = setup_dark_fig()
    # Terminal-like appearance
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    # Terminal frame
    rect = plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=True, facecolor='#0a0a0a',
                         edgecolor='#333333', linewidth=2, zorder=1)
    ax.add_patch(rect)
    # Title bar
    rect2 = plt.Rectangle((0.05, 0.85), 0.9, 0.1, fill=True, facecolor='#1a1a1a',
                          edgecolor='#333333', linewidth=1, zorder=2)
    ax.add_patch(rect2)
    # Window buttons
    for i, c in enumerate(['#e57373', '#ffb74d', '#81c784']):
        ax.plot(0.1 + i * 0.04, 0.9, 'o', color=c, markersize=5, zorder=3)
    # Terminal text
    lines = [
        ('$ ', '#81c784', 'ls -la ~/projects'),
        ('', '#888888', 'drwxr-xr-x  scripts/'),
        ('', '#888888', '-rw-r--r--  deploy.sh'),
        ('$ ', '#81c784', 'git status'),
        ('', '#4fc3f7', 'On branch master'),
        ('', '#81c784', 'nothing to commit'),
        ('$ ', '#81c784', '▌'),
    ]
    for i, (prompt, color, text) in enumerate(lines):
        y = 0.78 - i * 0.09
        if prompt:
            ax.text(0.1, y, prompt, color='#81c784', fontsize=7, fontfamily='monospace', zorder=3)
        ax.text(0.15, y, text, color=color, fontsize=6, fontfamily='monospace', zorder=3)
    save_thumb(fig, 'code-shell')

gen_shell()

# ============================================================
# SIGNAL PROCESSING
# ============================================================
print("\n=== Signal Processing code thumbnail ===")

def gen_signal():
    fig, axes = plt.subplots(2, 1, figsize=(4, 4), facecolor=DARK_BG)
    for ax in axes:
        ax.set_facecolor(DARK_BG)
        ax.tick_params(colors='#888888', labelsize=6)
        for spine in ax.spines.values():
            spine.set_color('#333333')
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 25 * t) + 0.3 * np.sin(2 * np.pi * 50 * t)
    axes[0].plot(t, signal, color=ACCENT_COLORS[0], linewidth=0.8)
    axes[0].set_title('Time Domain', color='#cccccc', fontsize=8, pad=3)
    # FFT
    freqs = np.fft.fftfreq(len(t), t[1] - t[0])
    fft_vals = np.abs(np.fft.fft(signal))
    mask = freqs > 0
    axes[1].plot(freqs[mask][:100], fft_vals[mask][:100], color=ACCENT_COLORS[2], linewidth=1.5)
    axes[1].fill_between(freqs[mask][:100], fft_vals[mask][:100], alpha=0.2, color=ACCENT_COLORS[2])
    axes[1].set_title('Frequency Spectrum', color='#cccccc', fontsize=8, pad=3)
    fig.tight_layout(pad=1)
    save_thumb(fig, 'code-signal')

gen_signal()

# ============================================================
# TEACHING CODE ITEMS
# ============================================================
print("\n=== Teaching code thumbnails ===")

# Math visualizations
def gen_math_viz():
    fig, ax = setup_dark_fig()
    theta = np.linspace(0, 4 * np.pi, 1000)
    r = 1 + 0.5 * np.cos(5 * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color=ACCENT_COLORS[0], linewidth=2)
    ax.fill(x, y, color=ACCENT_COLORS[0], alpha=0.1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Rose Curve', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-math-viz')

gen_math_viz()

# Arts & recreation
def gen_arts():
    fig, ax = setup_dark_fig()
    np.random.seed(42)
    # Spirograph
    t = np.linspace(0, 20 * np.pi, 5000)
    R, r, d = 5, 3, 5
    x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
    y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)
    # Color by angle
    colors = plt.cm.cool(np.linspace(0, 1, len(t)))
    for i in range(0, len(t) - 1, 5):
        ax.plot(x[i:i+6], y[i:i+6], color=colors[i], linewidth=0.5, alpha=0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Spirograph', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-arts')

gen_arts()

# TeX goodies
def gen_tex():
    fig, ax = setup_dark_fig()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    # LaTeX-rendered formulas
    formulas = [
        r'$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}$',
        r'$\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}$',
        r'$e^{i\pi} + 1 = 0$',
        r'$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$',
    ]
    for i, f in enumerate(formulas):
        y = 0.8 - i * 0.2
        ax.text(0.5, y, f, color=ACCENT_COLORS[i % len(ACCENT_COLORS)],
               fontsize=14, ha='center', va='center')
    ax.set_title('LaTeX Formulas', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'code-tex')

gen_tex()

# ============================================================
# TEACHING SAGE CODE - use existing sage/ images
# ============================================================
print("\n=== Teaching Sage Code thumbnails (from existing images) ===")

sage_items = {
    'sage-newton': 'sage/newton.gif',  # need special handling for GIF
    'sage-level-curves': 'sage/level_curves.png',
    'sage-cross-sections': 'sage/cross_sections.png',
    'sage-linearize-jacobian': 'sage/linearize_jacobian.png',
    'sage-linear-appx': 'sage/linear_appx.png',
    'sage-taylor': 'sage/taylor.png',
    'sage-random-echelon': 'sage/random_echelon.png',
    'sage-random-invertible': 'sage/random_invertible.png',
    'sage-gaussian-elimination': 'sage/gaussian_elimination.png',
    'sage-inverting': 'sage/inverting.png',
    'sage-inverting2': 'sage/inverting2.png',
    'sage-gershgorin': 'sage/gershgorin.png',
    'sage-solve-linear': None,  # no image, generate
}

for name, path in sage_items.items():
    if path is None:
        continue
    full_path = os.path.join(BASE, path)
    if not os.path.exists(full_path):
        print(f"  SKIP {name}: not found")
        continue
    if path.endswith('.gif'):
        # For GIF, get first frame
        img = Image.open(full_path)
        img = img.convert('RGB')
        process_existing_image(full_path.replace('.gif', '.gif'), name)
        # Actually just use PIL
        img_pil = Image.open(full_path).convert('RGB')
        arr = np.array(img_pil)
        if arr.mean() > 140:
            arr = 255 - arr
        img_pil = Image.fromarray(arr)
        w, h = img_pil.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img_pil = img_pil.crop((left, top, left + side, top + side))
        img_pil = img_pil.resize((400, 400), Image.LANCZOS)
        img_pil.save(os.path.join(OUT_DIR, f"{name}.webp"), "WEBP", quality=85)
        print(f"  Saved: {name}.webp (from GIF)")
    else:
        process_existing_image(full_path, name)

# Generate solve-linear thumbnail
def gen_solve_linear():
    fig, ax = setup_dark_fig()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.text(0.5, 0.6, r'$Ax = b$', color=ACCENT_COLORS[0], fontsize=28, ha='center', va='center')
    ax.text(0.5, 0.35, r'$x = A^{-1}b$', color=ACCENT_COLORS[1], fontsize=22, ha='center', va='center')
    ax.set_title('Linear System', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'sage-solve-linear')

gen_solve_linear()

# ============================================================
# ANOMALY DETECTION (ML paper without PDF)
# ============================================================
print("\n=== ML paper thumbnail ===")

def gen_anomaly():
    fig, ax = setup_dark_fig()
    np.random.seed(20)
    t = np.linspace(0, 10, 2000)
    # EEG-like signal
    signal = np.sin(2*np.pi*t) + 0.5*np.sin(2*np.pi*3*t) + np.random.normal(0, 0.3, len(t))
    # Seizure burst
    mask = (t > 4) & (t < 6)
    signal[mask] += 3 * np.sin(2*np.pi*15*t[mask]) + np.random.normal(0, 1, mask.sum())
    ax.plot(t, signal, color=ACCENT_COLORS[0], linewidth=0.5)
    ax.axvspan(4, 6, color=ACCENT_COLORS[3], alpha=0.15)
    ax.text(5, ax.get_ylim()[1] * 0.9, 'Seizure', color=ACCENT_COLORS[3], fontsize=9, ha='center')
    ax.set_title('EEG Anomaly Detection', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'paper-anomaly')

gen_anomaly()

# ============================================================
# Neuroscience papers without PDFs
# ============================================================
print("\n=== Neuroscience paper thumbnails (no PDF) ===")

def gen_brain_kuramoto():
    fig, ax = setup_dark_fig()
    np.random.seed(3)
    # Brain network oscillators
    n = 12
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = 0.5 + 0.35 * np.cos(angles)
    y = 0.5 + 0.35 * np.sin(angles)
    # Phase coloring
    phases = np.random.uniform(0, 2 * np.pi, n)
    colors_arr = plt.cm.hsv(phases / (2 * np.pi))
    # Draw connections
    for i in range(n):
        for j in range(i+1, n):
            if np.random.random() > 0.6:
                ax.plot([x[i], x[j]], [y[i], y[j]], color='#333333', linewidth=0.5, alpha=0.5)
    for i in range(n):
        ax.scatter(x[i], y[i], s=100, color=colors_arr[i], zorder=5, edgecolors='white', linewidth=0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Kuramoto Brain Network', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'paper-brain-kuramoto')

gen_brain_kuramoto()

def gen_default_mode():
    fig, ax = setup_dark_fig()
    np.random.seed(7)
    # Brain-like outline with highlighted regions
    t = np.linspace(0, 2 * np.pi, 100)
    # Simple brain outline
    x_brain = 0.5 + 0.35 * np.cos(t) * (1 + 0.1 * np.cos(2 * t))
    y_brain = 0.5 + 0.3 * np.sin(t)
    ax.plot(x_brain, y_brain, color='#555555', linewidth=2)
    # DMN regions (approximate)
    regions = [(0.35, 0.6, 0.08), (0.65, 0.6, 0.08), (0.5, 0.45, 0.06), (0.5, 0.7, 0.07)]
    for x, y, r in regions:
        circle = plt.Circle((x, y), r, color=ACCENT_COLORS[2], alpha=0.4, zorder=3)
        ax.add_patch(circle)
    # Connections between regions
    for i in range(len(regions)):
        for j in range(i+1, len(regions)):
            ax.plot([regions[i][0], regions[j][0]], [regions[i][1], regions[j][1]],
                   color=ACCENT_COLORS[2], linewidth=1, alpha=0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 0.9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Default Mode Network', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'paper-default-mode')

gen_default_mode()

# Graph theory papers without PDFs
print("\n=== Graph Theory paper thumbnails (no PDF) ===")

def gen_reciprocal_matrix():
    fig, ax = setup_dark_fig()
    np.random.seed(4)
    M = np.array([[1, 2, 3], [0.5, 1, 4], [1/3, 0.25, 1]])
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('dark3', ['#111111', '#ba68c8'])
    ax.imshow(np.log(M + 0.1), cmap=cmap, interpolation='nearest')
    for i in range(3):
        for j in range(3):
            val = M[i, j]
            txt = f'{val:.2f}' if val != int(val) else str(int(val))
            ax.text(j, i, txt, ha='center', va='center', color='white', fontsize=10)
    ax.set_title('Reciprocal Matrix', color='#cccccc', fontsize=10, pad=5)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    save_thumb(fig, 'paper-reciprocal')

gen_reciprocal_matrix()

def gen_dissonance():
    fig, ax = setup_dark_fig()
    np.random.seed(11)
    n = 10
    pos = {i: (np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)) for i in range(n)}
    # Social network with positive/negative edges
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.random() > 0.6:
                sign = np.random.choice([-1, 1])
                color = ACCENT_COLORS[1] if sign > 0 else ACCENT_COLORS[3]
                style = '-' if sign > 0 else '--'
                ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]],
                       color=color, linewidth=1, linestyle=style, alpha=0.6)
    for i in range(n):
        ax.plot(pos[i][0], pos[i][1], 'o', color=ACCENT_COLORS[0], markersize=10, zorder=5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Dissonance Network', color='#cccccc', fontsize=10, pad=5)
    save_thumb(fig, 'paper-dissonance')

gen_dissonance()

print("\n=== ALL CODE THUMBNAILS GENERATED ===")
