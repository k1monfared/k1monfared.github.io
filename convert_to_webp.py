#!/usr/bin/env python3
"""
Convert all JPEG images to WebP format and update HTML references.
WebP typically reduces file size by 25-35% while maintaining quality.
"""

import os
import sys
from pathlib import Path
import re

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library not found.")
    print("Please install it with: pip install Pillow")
    sys.exit(1)


def convert_image_to_webp(jpeg_path, quality=90):
    """Convert a JPEG image to WebP format."""
    try:
        webp_path = jpeg_path.with_suffix('.webp')

        # Skip if WebP already exists and is newer
        if webp_path.exists() and webp_path.stat().st_mtime > jpeg_path.stat().st_mtime:
            return webp_path, 0, 0

        # Open and convert image
        with Image.open(jpeg_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background

            # Save as WebP
            img.save(webp_path, 'WebP', quality=quality, method=6)

        # Get file sizes
        jpeg_size = jpeg_path.stat().st_size
        webp_size = webp_path.stat().st_size

        return webp_path, jpeg_size, webp_size

    except Exception as e:
        print(f"Error converting {jpeg_path}: {e}")
        return None, 0, 0


def find_jpeg_files(root_dir):
    """Find all JPEG files in the directory."""
    root = Path(root_dir)
    jpeg_files = []

    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
        jpeg_files.extend(root.rglob(ext))

    return sorted(jpeg_files)


def find_html_files(root_dir):
    """Find all HTML files in the directory."""
    root = Path(root_dir)
    return sorted(root.rglob('*.html'))


def replace_references_in_file(html_path, replacements):
    """Replace JPEG references with WebP in an HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        changes_made = []

        for jpeg_rel, webp_rel in replacements.items():
            # Try different path variations
            patterns = [
                jpeg_rel,
                jpeg_rel.replace('\\', '/'),
                './' + jpeg_rel,
                '../' + jpeg_rel,
            ]

            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, webp_rel)
                    if pattern not in changes_made:
                        changes_made.append(pattern)

        # Only write if changes were made
        if content != original_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return len(changes_made)

        return 0

    except Exception as e:
        print(f"Error processing {html_path}: {e}")
        return 0


def main():
    root_dir = Path.cwd()

    print("=" * 70)
    print("JPEG to WebP Converter")
    print("=" * 70)
    print()

    # Find all JPEG files
    print("Scanning for JPEG files...")
    jpeg_files = find_jpeg_files(root_dir)
    print(f"Found {len(jpeg_files)} JPEG files")
    print()

    if not jpeg_files:
        print("No JPEG files found!")
        return

    # Convert images
    print("Converting images to WebP...")
    print("-" * 70)

    conversions = {}
    total_jpeg_size = 0
    total_webp_size = 0
    successful_conversions = 0

    for i, jpeg_path in enumerate(jpeg_files, 1):
        rel_path = jpeg_path.relative_to(root_dir)
        print(f"[{i}/{len(jpeg_files)}] {rel_path}", end=" ... ")

        webp_path, jpeg_size, webp_size = convert_image_to_webp(jpeg_path)

        if webp_path:
            conversions[str(rel_path)] = str(webp_path.relative_to(root_dir))
            total_jpeg_size += jpeg_size
            total_webp_size += webp_size

            if jpeg_size > 0:
                reduction = ((jpeg_size - webp_size) / jpeg_size) * 100
                print(f"OK ({jpeg_size/1024:.1f}KB → {webp_size/1024:.1f}KB, {reduction:.1f}% smaller)")
                successful_conversions += 1
            else:
                print("SKIPPED (already exists)")
        else:
            print("FAILED")

    print()
    print("=" * 70)
    print("Conversion Summary:")
    print(f"  Total JPEG size: {total_jpeg_size/1024/1024:.2f} MB")
    print(f"  Total WebP size: {total_webp_size/1024/1024:.2f} MB")
    if total_jpeg_size > 0:
        total_reduction = ((total_jpeg_size - total_webp_size) / total_jpeg_size) * 100
        print(f"  Space saved: {(total_jpeg_size - total_webp_size)/1024/1024:.2f} MB ({total_reduction:.1f}%)")
    print(f"  Successful conversions: {successful_conversions}/{len(jpeg_files)}")
    print("=" * 70)
    print()

    # Update HTML files
    print("Updating HTML file references...")
    print("-" * 70)

    html_files = find_html_files(root_dir)
    print(f"Found {len(html_files)} HTML files")
    print()

    # Build replacement dictionary
    replacements = {}
    for jpeg_path, webp_path in conversions.items():
        # Add various formats
        replacements[jpeg_path] = webp_path
        replacements[jpeg_path.replace('\\', '/')] = webp_path.replace('\\', '/')

    total_replacements = 0
    files_modified = 0

    for html_path in html_files:
        rel_path = html_path.relative_to(root_dir)
        changes = replace_references_in_file(html_path, replacements)
        if changes > 0:
            print(f"  {rel_path}: {changes} reference(s) updated")
            total_replacements += changes
            files_modified += 1

    print()
    print("=" * 70)
    print("HTML Update Summary:")
    print(f"  Files scanned: {len(html_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print("=" * 70)
    print()
    print("Conversion complete!")
    print()
    print("Note: Original JPEG files are kept. After verifying the site works,")
    print("      you can remove them with: find . -type f \\( -iname '*.jpg' -o -iname '*.jpeg' \\) -delete")


if __name__ == '__main__':
    main()
