#!/usr/bin/env python3
"""
Fix triathlon training plan distances - convert from converted meters back to original yard values
(but keep them labeled as meters, since we're using yards as meters 1:1)
"""

import re

# Read the HTML file
input_file = 'blog/2025_11_!2_16_week_olympic_triathlon_training_plan.html'
output_file = input_file  # Overwrite the same file

print("Reading file...")
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("Making replacements...")

# Total swim workout distances (these appear in workout-duration)
distance_replacements = {
    # Week-by-week total distances
    '1460m': '800m',   # Week 1 (200+100+100+100+100+200 = 800)
    '1640m': '900m',   # Week 2 (200+100+100+100+100+100+200 = 900)
    '1820m': '1000m',  # Week 3 (200+100+100+100+100+100+200 = 1000)
    '2000m': '1100m',  # Week 5 (200+100+100+100+100+100+100+200 = 1100)
    '2185m': '1200m',  # Week 6 (200+100+100+100+100+100+100+200 = 1200)
    '2320m': '1275m',  # Week 7 (200+100+75+75+75+75+75+75+200 = 1275)
    '1820m': '1000m',  # Week 8
    '2458m': '1350m',  # Week 9 (200+100+75+75+75+75+75+75+75+200 = 1350)
    '2549m': '1400m',  # Week 9 Friday, 10, 11 (200+100+200+200+200+200+100 = 1400)
    '2002m': '1100m',  # Week 12 (200+100+75+75+75+75+75+200 = 1100)
    '2185m': '1200m',  # Week 12 Friday
    '2732m': '1500m',  # Weeks 13-15 (200+100+100+100+100+100+100+100+100+200 = 1500)
    '1640m': '900m',   # Week 16 Friday
}

# Individual distance replacements within workouts
detail_replacements = {
    # Warmup/Cooldown
    '180m': '200m',
    '183m': '200m',

    # Drills and kicks
    '×23m': '×25m',
    '23m': '25m',

    # Main set intervals
    '×91m': '×100m',
    '91m': '100m',
    '×68m': '×75m',
    '68m': '75m',
    '×69m': '×75m',
    '69m': '75m',
    '×183m': '×200m',
    '183m': '200m',
    '×274m': '×300m',
    '274m': '300m',
}

# Apply total distance replacements first
for old, new in distance_replacements.items():
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f"  Replaced {old} → {new} ({count} times)")

# Apply detail replacements
for old, new in detail_replacements.items():
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f"  Replaced {old} → {new} ({count} times)")

# Additional specific patterns that might need fixing
# Fix any remaining converted distances in specific contexts
specific_patterns = [
    # Match patterns like "span>180m</span>" and replace with "span>200m</span>"
    (r'(\d+)m(?=</span>)', lambda m: str({
        '180': '200', '183': '200',
        '23': '25',
        '91': '100',
        '68': '75', '69': '75',
        '274': '300',
        '1460': '800', '1640': '900', '1820': '1000',
        '2000': '1100', '2185': '1200', '2320': '1275',
        '2458': '1350', '2549': '1400', '2732': '1500',
        '2002': '1100',
    }.get(m.group(1), m.group(1))) + 'm'),
]

for pattern, replacement in specific_patterns:
    content = re.sub(pattern, replacement, content)

# Also fix race day distances if they're wrong
# Sprint Triathlon in Week 12: Swim 800, Bike 12 miles, Run 3 miles
# Olympic Triathlon in Week 16: 1500m swim, 40km bike, 10km run

print("\nWriting updated file...")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Done! Updated {output_file}")
print("\nPlease review the changes and test the page.")
