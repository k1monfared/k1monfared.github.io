#!/usr/bin/env python3
"""
Update all HTML pages to use the new dark theme structure.
Applies changes to research.html, teaching.html, computation.html, learning.html, blog.html, and contact.html
"""

import re

# List of HTML files to update
files_to_update = [
    'research.html',
    'teaching.html',
    'computation.html',
    'learning.html',
    'blog.html',
    'contact.html'
]

def update_html_file(filename):
    """Update a single HTML file with the new structure."""
    print(f"Updating {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update DOCTYPE and html tag
    content = re.sub(
        r'<!DOCTYPE html PUBLIC.*?>\s*<html xmlns.*?>',
        '<!DOCTYPE html>\n<html lang="en">',
        content,
        flags=re.DOTALL
    )

    # Update head section - meta charset and viewport
    content = re.sub(
        r'<head>\s*<meta http-equiv="Content-Type".*?>',
        '<head>\n\t<meta charset="UTF-8">\n\t<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        content
    )

    # Update title
    content = re.sub(
        r'<title>\s*Keivan Monfared\'s Home Page\s*</title>',
        f'<title>Keivan Monfared - {filename.replace(".html", "").title()}</title>',
        content
    )

    # Update body structure - add bg-gradient, header section, and move nav outside container
    body_pattern = r'<body>\s*<div class="container">\s*<div id="stick-here"></div>\s*<div class="myTitle">\s*KEIVAN MONFARED\s*</div>\s*<div class="myTitleFooter">\s*Mathematics and Data Science\s*</div>\s*<!-- Navigation loaded from nav\.html -->\s*<div id="nav-container"></div>'

    body_replacement = '''<body>
\t<div class="bg-gradient"></div>

\t<header class="site-header">
\t\t<div class="header-content">
\t\t\t<h1 class="myTitle">KEIVAN MONFARED</h1>
\t\t\t<p class="myTitleFooter">Mathematics and Data Science</p>
\t\t</div>
\t</header>

\t<div id="stick-here"></div>

\t<!-- Navigation loaded from nav.html -->
\t<div id="nav-container"></div>

\t<div class="container">'''

    content = re.sub(body_pattern, body_replacement, content, flags=re.DOTALL)

    # Update small_menu innerHTML to remove span tags
    content = re.sub(
        r"'<span class=\"menuItem\"><a href=\"(#[^\"]+)\">([^<]+)</a></span>'",
        r"'<a href=\"\1\">\2</a>'",
        content
    )

    # Update pageContent and mainContent to main-content
    content = re.sub(
        r'<div id="pageContent">\s*<div id="mainContent">',
        '\t\t<main class="main-content">',
        content
    )

    # Update closing divs for pageContent and mainContent
    content = re.sub(
        r'</div>\s*</div>\s*<!-- Footer and social media loaded from footer\.html -->',
        '\t\t</main>\n\n\t\t<!-- Footer and social media loaded from footer.html -->',
        content
    )

    # Update footer structure
    content = re.sub(
        r'<!-- Footer and social media loaded from footer\.html -->\s*<div id="footer-container"></div>\s*</div>\s*</body>',
        '''<!-- Footer and social media loaded from footer.html -->
\t\t<footer class="site-footer">
\t\t\t<div id="footer-container"></div>
\t\t</footer>
\t</div>

\t<!-- Scroll to top button (mobile only) -->
\t<button class="scroll-to-top" aria-label="Scroll to top"></button>

\t<script>
\t\t// Scroll to top button functionality
\t\tconst scrollToTopBtn = document.querySelector('.scroll-to-top');

\t\tif (scrollToTopBtn) {
\t\t\tscrollToTopBtn.addEventListener('click', () => {
\t\t\t\twindow.scrollTo({
\t\t\t\t\ttop: 0,
\t\t\t\t\tbehavior: 'smooth'
\t\t\t\t});
\t\t\t});

\t\t\t// Show/hide scroll to top button based on scroll position
\t\t\twindow.addEventListener('scroll', () => {
\t\t\t\tif (window.pageYOffset > 300) {
\t\t\t\t\tscrollToTopBtn.style.opacity = '1';
\t\t\t\t\tscrollToTopBtn.style.pointerEvents = 'auto';
\t\t\t\t} else {
\t\t\t\t\tscrollToTopBtn.style.opacity = '0';
\t\t\t\t\tscrollToTopBtn.style.pointerEvents = 'none';
\t\t\t\t}
\t\t\t});

\t\t\t// Initialize button state
\t\t\tscrollToTopBtn.style.opacity = '0';
\t\t\tscrollToTopBtn.style.pointerEvents = 'none';
\t\t}
\t</script>
</body>''',
        content
    )

    # Write updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {filename}")

def main():
    """Update all HTML files."""
    for filename in files_to_update:
        try:
            update_html_file(filename)
        except Exception as e:
            print(f"✗ Error updating {filename}: {e}")

    print("\nAll files updated successfully!")

if __name__ == '__main__':
    main()
