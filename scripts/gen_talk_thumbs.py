#!/usr/bin/env python3
"""Generate unique thumbnails for talks that don't have slide PDFs."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os, io

BASE = "/home/k1/public/k1monfared.github.io"
OUT_DIR = os.path.join(BASE, "images/thumbs")
DARK_BG = '#111111'
ACCENT = ['#4fc3f7', '#81c784', '#ffb74d', '#e57373', '#ba68c8', '#4dd0e1', '#fff176']

def setup_dark_fig(figsize=(4, 4)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
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
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUT_DIR, f"{name}.webp"), "WEBP", quality=85)
    print(f"  Saved: {name}.webp")

# Generic talk-topic generator with unique visuals per topic
def gen_topic_thumb(name, title, visual_fn):
    fig, ax = setup_dark_fig()
    visual_fn(ax)
    ax.set_title(title, color='#aaaaaa', fontsize=8, pad=5, style='italic')
    save_thumb(fig, name)

# ============================================================
# MATRIX THEORY TALKS (without slide PDFs)
# ============================================================
print("=== Matrix Theory talks ===")

def draw_ilas_2019(ax):
    # Polynomial with graph
    np.random.seed(19)
    x = np.linspace(-2, 3, 200)
    p = (x + 1) * (x - 0.5) * (x - 2)
    ax.plot(x, p, color=ACCENT[0], linewidth=2)
    ax.axhline(0, color='#333', linewidth=0.5)
    roots = [-1, 0.5, 2]
    ax.scatter(roots, [0]*3, color=ACCENT[3], s=60, zorder=5)
    ax.axis('off')
gen_topic_thumb('talk-ilas-2019', 'Inverse Polynomial Spectral Problems', draw_ilas_2019)

def draw_wclam(ax):
    np.random.seed(16)
    n = 7
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = np.cos(a)*0.6, np.sin(a)*0.6
    for i in range(n):
        for j in range(i+1, n):
            if abs(i-j) <= 2 or abs(i-j) >= n-2:
                ax.plot([x[i],x[j]], [y[i],y[j]], color='#444', lw=1)
    ax.scatter(x, y, s=80, color=ACCENT[1], zorder=5, edgecolors='w', linewidth=0.5)
    # Eigenvalue markers
    evals = np.sort(np.random.uniform(-2, 3, n))
    for i, e in enumerate(evals):
        ax.plot(-0.8 + i*0.23, -0.85, '|', color=ACCENT[2], markersize=10, mew=2)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-wclam-2016', 'Inverse Eigenvalue Problems', draw_wclam)

def draw_ilas_2016(ax):
    np.random.seed(2016)
    # Jacobian visualization - contour plot
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2 + 0.5*np.sin(3*X*Y)
    ax.contour(X, Y, Z, levels=15, colors=[ACCENT[0]], linewidths=0.8, alpha=0.6)
    ax.contourf(X, Y, Z, levels=15, cmap='cool', alpha=0.2)
    ax.scatter([0], [0], color=ACCENT[3], s=80, zorder=5)
    ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-ilas-2016', 'Jacobian Method for SIEPs', draw_ilas_2016)

def draw_jmm_2016(ax):
    np.random.seed(2016)
    # Multiple graph examples
    graphs = [
        [(0,0.7), (0.3,0.9), (0.3,0.5)],
        [(0.6,0.7), (0.9,0.9), (0.9,0.5), (0.6,0.5)],
    ]
    for pts in graphs:
        for i in range(len(pts)):
            for j in range(i+1, len(pts)):
                ax.plot([pts[i][0],pts[j][0]], [pts[i][1],pts[j][1]], color='#444', lw=1.5)
        for p in pts:
            ax.plot(p[0], p[1], 'o', color=ACCENT[4], ms=10, zorder=5)
    ax.text(0.5, 0.25, r'$\det(J_f) \neq 0$', color=ACCENT[0], fontsize=14, ha='center')
    ax.set_xlim(-0.1, 1.1); ax.set_ylim(0, 1); ax.axis('off')
gen_topic_thumb('talk-jmm-2016', 'Jacobian Method Examples', draw_jmm_2016)

def draw_canadam_2015(ax):
    np.random.seed(15)
    # Tree with highlighted path
    nodes = {0:(0.5,0.9), 1:(0.25,0.6), 2:(0.75,0.6), 3:(0.1,0.3), 4:(0.4,0.3), 5:(0.6,0.3), 6:(0.9,0.3)}
    edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
    for i,j in edges:
        c = ACCENT[2] if (i==0 and j==1) or (i==1 and j==3) else '#444'
        ax.plot([nodes[i][0],nodes[j][0]], [nodes[i][1],nodes[j][1]], color=c, lw=2)
    for k, (x,y) in nodes.items():
        ax.plot(x, y, 'o', color=ACCENT[1], ms=12, zorder=5)
    ax.text(0.5, 0.05, 'Nowhere-zero eigenbasis', color='#888', fontsize=8, ha='center')
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05); ax.axis('off')
gen_topic_thumb('talk-jmm-2015', 'Nowhere-Zero Eigenbasis', draw_canadam_2015)

def draw_grwc(ax):
    np.random.seed(14)
    M = np.random.choice([0,1], (5,5), p=[0.4,0.6])
    np.fill_diagonal(M, 1)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('d', ['#111', '#ba68c8'])
    ax.imshow(M, cmap=cmap, interpolation='nearest')
    for i in range(5):
        for j in range(5):
            ax.text(j, i, str(M[i,j]), ha='center', va='center', color='white', fontsize=9)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
gen_topic_thumb('talk-grwc-2014', 'Principal Perrank Sequences', draw_grwc)

def draw_vibrating(ax):
    np.random.seed(14)
    # Spring-mass system
    y = 0.5
    for i in range(5):
        x = 0.1 + i * 0.2
        # Spring (zigzag)
        if i > 0:
            xs = np.linspace(x - 0.2, x, 20)
            ys = y + 0.03 * np.sin(np.linspace(0, 6*np.pi, 20))
            ax.plot(xs, ys, color='#666', lw=1)
        # Mass
        rect = plt.Rectangle((x-0.04, y-0.06), 0.08, 0.12, color=ACCENT[i%len(ACCENT)], zorder=5)
        ax.add_patch(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0.2, 0.8); ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-wiu-colloquium', 'Vibrating Systems', draw_vibrating)

def draw_wiu_seminar(ax):
    np.random.seed(14)
    # Structured IEP diagram
    n = 6
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = 0.5+0.3*np.cos(a), 0.6+0.3*np.sin(a)
    for i in range(n):
        ax.plot([x[i],x[(i+1)%n]], [y[i],y[(i+1)%n]], color='#555', lw=1.5)
    ax.scatter(x, y, s=80, color=ACCENT[0], zorder=5)
    ax.text(0.5, 0.1, r'$\sigma(A) = \{\lambda_1,\ldots,\lambda_n\}$', color=ACCENT[2], fontsize=11, ha='center')
    ax.set_xlim(0,1); ax.set_ylim(-0.05,1.05); ax.axis('off')
gen_topic_thumb('talk-wiu-seminar', 'Structured IEP', draw_wiu_seminar)

def draw_acnt(ax):
    np.random.seed(14)
    # Skew-symmetric matrix visualization
    M = np.array([[0,2,-1,3],[- 2,0,4,-1],[1,-4,0,2],[-3,1,-2,0]])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('ss', ['#e57373', '#111', '#4fc3f7'])
    ax.imshow(M, cmap=cmap, interpolation='nearest', vmin=-4, vmax=4)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(M[i,j]), ha='center', va='center', color='white', fontsize=10)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
gen_topic_thumb('talk-acnt', 'Skew-Symmetric SIEP', draw_acnt)

def draw_ucd(ax):
    np.random.seed(13)
    x = np.linspace(-2, 2, 100)
    for i in range(3):
        y = np.exp(-((x - (i-1)*0.5)**2) / (0.3 + 0.2*i))
        ax.fill_between(x, y * (i+1), alpha=0.3, color=ACCENT[i])
        ax.plot(x, y * (i+1), color=ACCENT[i], lw=1.5)
    ax.axis('off')
gen_topic_thumb('talk-ucd-2013', 'Jacobian Method in SIEPs', draw_ucd)

def draw_mathfest(ax):
    np.random.seed(13)
    # Path graph with eigenvalues
    for i in range(6):
        x = 0.1 + i * 0.16
        if i < 5:
            ax.plot([x, x+0.16], [0.7, 0.7], color='#555', lw=2)
        ax.plot(x, 0.7, 'o', color=ACCENT[0], ms=10, zorder=5)
    # Spectrum
    evals = [-2, -1.2, -0.3, 0.3, 1.2, 2]
    for i, e in enumerate(evals):
        ax.plot(0.1 + i*0.16, 0.3, '|', color=ACCENT[2], ms=15, mew=2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
gen_topic_thumb('talk-mathfest-2013', 'Structured IEP', draw_mathfest)

def draw_rmdmd_2012(ax):
    np.random.seed(12)
    n = 5
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = 0.5+0.3*np.cos(a), 0.5+0.3*np.sin(a)
    for i in range(n):
        for j in range(i+1, n):
            if np.random.random() > 0.3:
                ax.plot([x[i],x[j]], [y[i],y[j]], color='#444', lw=1)
    ax.scatter(x, y, s=80, color=ACCENT[3], zorder=5, edgecolors='w', linewidth=0.5)
    ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-rmdmd-2012', 'λ-μ Problem', draw_rmdmd_2012)

def draw_mighty(ax):
    np.random.seed(12)
    # Interlacing bars
    n = 6
    lambdas = np.sort(np.random.uniform(-2, 3, n))
    mus = np.sort(np.random.uniform(-1.5, 2.5, n-1))
    for i, l in enumerate(lambdas):
        ax.barh(0.6, 0.02, left=l, height=0.15, color=ACCENT[0])
        ax.text(l, 0.75, f'λ{i+1}', color=ACCENT[0], fontsize=6, ha='center')
    for i, m in enumerate(mus):
        ax.barh(0.3, 0.02, left=m, height=0.15, color=ACCENT[2])
        ax.text(m, 0.2, f'μ{i+1}', color=ACCENT[2], fontsize=6, ha='center')
    ax.set_ylim(0, 1); ax.axis('off')
gen_topic_thumb('talk-mighty-2012', 'Interlacing Construction', draw_mighty)

# ============================================================
# NEUROSCIENCE TALKS
# ============================================================
print("\n=== Neuroscience talks ===")

def draw_pdmw(ax):
    np.random.seed(18)
    n = 16
    # EEG channels arranged vertically
    for i in range(n):
        t = np.linspace(0, 2, 200)
        signal = np.sin(2*np.pi*(2+i*0.3)*t) + np.random.normal(0, 0.2, 200)
        ax.plot(t, signal * 0.3 + i, color=ACCENT[i % len(ACCENT)], lw=0.5, alpha=0.7)
    ax.set_xlim(0, 2); ax.axis('off')
gen_topic_thumb('talk-pdmw-2018', 'Graph Partitioning in Neuroscience', draw_pdmw)

# ============================================================
# GRAPH THEORY TALKS
# ============================================================
print("\n=== Graph Theory talks ===")

def draw_gt_jmm_2016(ax):
    np.random.seed(2016)
    # Bipartite graph
    left = [(0.2, 0.2 + i*0.2) for i in range(4)]
    right = [(0.8, 0.3 + i*0.2) for i in range(3)]
    for l in left:
        for r in right:
            if np.random.random() > 0.4:
                ax.plot([l[0],r[0]], [l[1],r[1]], color='#444', lw=1)
    for p in left:
        ax.plot(p[0], p[1], 'o', color=ACCENT[0], ms=10, zorder=5)
    for p in right:
        ax.plot(p[0], p[1], 's', color=ACCENT[2], ms=10, zorder=5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
gen_topic_thumb('talk-gt-jmm-2016', 'Permanent Rank Sequences', draw_gt_jmm_2016)

def draw_gt_calgary(ax):
    np.random.seed(2015)
    n = 8
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = 0.5+0.35*np.cos(a), 0.5+0.35*np.sin(a)
    # Draw all edges, highlight matching
    for i in range(n):
        for j in range(i+1, n):
            if np.random.random() > 0.5:
                ax.plot([x[i],x[j]], [y[i],y[j]], color='#333', lw=1)
    # Highlight some edges as matching
    for i in range(0, n, 2):
        j = (i+1) % n
        ax.plot([x[i],x[j]], [y[i],y[j]], color=ACCENT[2], lw=3)
    ax.scatter(x, y, s=80, color=ACCENT[0], zorder=5)
    ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-gt-calgary', 'Generalized Cycles', draw_gt_calgary)

def draw_gt_jmm_2012(ax):
    np.random.seed(2012)
    # Permanent rank diagram
    M = np.random.choice([0,1], (4,4), p=[0.3,0.7])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('d', ['#111', '#4dd0e1'])
    ax.imshow(M, cmap=cmap, interpolation='nearest')
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(M[i,j]), ha='center', va='center', color='white', fontsize=11)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
gen_topic_thumb('talk-gt-jmm-2012', 'Permanent Rank', draw_gt_jmm_2012)

def draw_gt_gscc(ax):
    np.random.seed(2012)
    n = 6
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = 0.5+0.3*np.cos(a), 0.5+0.3*np.sin(a)
    for i in range(n):
        ax.plot([x[i],x[(i+1)%n]], [y[i],y[(i+1)%n]], color=ACCENT[4], lw=2)
    ax.scatter(x, y, s=80, color=ACCENT[0], zorder=5)
    ax.text(0.5, 0.05, 'perrank ↔ rank', color='#888', fontsize=9, ha='center')
    ax.set_xlim(0,1); ax.set_ylim(-0.05,1.05); ax.axis('off')
gen_topic_thumb('talk-gt-gscc', 'Perrank vs Rank', draw_gt_gscc)

def draw_gt_rmdmd(ax):
    np.random.seed(2011)
    # Cycle counting
    n = 5
    a = np.linspace(0, 2*np.pi, n, endpoint=False) + np.pi/2
    x, y = 0.5+0.3*np.cos(a), 0.55+0.3*np.sin(a)
    for i in range(n):
        ax.plot([x[i],x[(i+1)%n]], [y[i],y[(i+1)%n]], color=ACCENT[1], lw=2)
    ax.scatter(x, y, s=80, color=ACCENT[5], zorder=5)
    ax.text(0.5, 0.08, r'$\mathrm{perrank}(A)$', color=ACCENT[2], fontsize=12, ha='center')
    ax.set_xlim(0,1); ax.set_ylim(-0.05,1.05); ax.axis('off')
gen_topic_thumb('talk-gt-rmdmd', 'Perrank', draw_gt_rmdmd)

# ============================================================
# TEACHING TALKS
# ============================================================
print("\n=== Teaching talks ===")

def draw_infinity(ax):
    t = np.linspace(0, 2*np.pi, 1000)
    # Infinity symbol (lemniscate)
    a = 0.6
    x = a * np.cos(t) / (1 + np.sin(t)**2)
    y = a * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)
    colors = plt.cm.cool(np.linspace(0, 1, len(t)))
    for i in range(len(t)-1):
        ax.plot(x[i:i+2], y[i:i+2], color=colors[i], lw=3)
    # Numbers
    for i, n in enumerate([1, 2, 3, '...', '∞']):
        ax.text(0.15 + i*0.18, -0.4, str(n), color=ACCENT[i%len(ACCENT)], fontsize=14, ha='center')
    ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-counting-infinity', 'Counting to Infinity', draw_infinity)

def draw_calculus_apps(ax):
    x = np.linspace(0, 4*np.pi, 500)
    y1 = np.sin(x)
    y2 = np.cos(x)
    ax.fill_between(x, y1, y2, where=y1>y2, alpha=0.3, color=ACCENT[0])
    ax.fill_between(x, y1, y2, where=y1<=y2, alpha=0.3, color=ACCENT[3])
    ax.plot(x, y1, color=ACCENT[0], lw=2)
    ax.plot(x, y2, color=ACCENT[3], lw=2)
    ax.axis('off')
gen_topic_thumb('talk-calculus-apps', 'Calculus & Linear Algebra', draw_calculus_apps)

def draw_touching_infinity(ax):
    # Cantor set visualization
    def cantor(ax, x0, x1, y, depth=0, max_depth=6):
        if depth > max_depth:
            return
        third = (x1 - x0) / 3
        c = ACCENT[depth % len(ACCENT)]
        ax.plot([x0, x0 + third], [y, y], color=c, lw=max(1, 6-depth), solid_capstyle='butt')
        ax.plot([x0 + 2*third, x1], [y, y], color=c, lw=max(1, 6-depth), solid_capstyle='butt')
        cantor(ax, x0, x0+third, y-0.12, depth+1, max_depth)
        cantor(ax, x0+2*third, x1, y-0.12, depth+1, max_depth)
    cantor(ax, 0.05, 0.95, 0.9)
    ax.set_ylim(-0.05, 1); ax.axis('off')
gen_topic_thumb('talk-touching-infinity', 'Touching Infinity', draw_touching_infinity)

def draw_math_education(ax):
    # Abstract representation of education - interconnected nodes
    np.random.seed(2008)
    n = 12
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = 0.5 + 0.35 * np.cos(a)
    y = 0.5 + 0.35 * np.sin(a)
    for i in range(n):
        for j in range(i+1, n):
            if (j-i) % 3 == 0 or (j-i) % 4 == 0:
                ax.plot([x[i],x[j]], [y[i],y[j]], color=ACCENT[2], alpha=0.3, lw=0.8)
    ax.scatter(x, y, s=60, c=[ACCENT[i%len(ACCENT)] for i in range(n)], zorder=5)
    ax.set_aspect('equal'); ax.axis('off')
gen_topic_thumb('talk-math-education', 'Mathematics Education', draw_math_education)

def draw_problem_solving(ax):
    np.random.seed(2006)
    # Problem solving steps
    x = np.linspace(0, 10, 200)
    y = np.cumsum(np.random.choice([-1, 0, 0, 1, 1, 1], 200))
    ax.plot(x, y, color=ACCENT[0], lw=2)
    # Breakthrough moments
    peaks = [40, 90, 150]
    for p in peaks:
        ax.scatter(x[p], y[p], s=100, color=ACCENT[2], zorder=5, marker='*')
    ax.axis('off')
gen_topic_thumb('talk-problem-solving', 'Math Problem Solving', draw_problem_solving)

print("\nDone generating talk thumbnails!")
