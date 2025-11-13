#!/usr/bin/env python3
"""
Update workout type labels in the existing HTML without changing any other content
"""
import re

print("Reading HTML file...")
with open('blog/2025_11_12_16_week_olympic_triathlon_training_plan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Strategy: Find workout headers and update them based on surrounding context
# We'll use workout duration and details to identify the correct workout type

def update_workout_label(html, old_label, new_label, duration_pattern, detail_pattern=None):
    """Update a workout label based on duration and optional detail patterns"""
    # Build regex pattern to match the specific workout
    if detail_pattern:
        pattern = f'(<div class="workout-type"><span class="workout-icon">[^<]+</span> ){old_label}(</div>\\s+<span class="workout-duration">{re.escape(duration_pattern)}</span>.*?<ul class="workout-details">.*?{detail_pattern})'
    else:
        pattern = f'(<div class="workout-type"><span class="workout-icon">[^<]+</span> ){old_label}(</div>\\s+<span class="workout-duration">{re.escape(duration_pattern)}</span>)'

    replacement = f'\\1{new_label}\\2'
    html_new = re.sub(pattern, replacement, html, flags=re.DOTALL)
    count = len(re.findall(pattern, html, flags=re.DOTALL))
    if count > 0:
        print(f"  Updated {count} instances: {old_label} -> {new_label} (duration: {duration_pattern})")
    return html_new

# Update SWIM workouts
print("\\nUpdating SWIM workouts...")

# Swim Base (simple ones with 2x100, 3x100, 4x100, 5x100 in main set)
html = update_workout_label(html, 'SWIM', 'SWIM BASE', '800m', '2 ×100 @ moderate')
html = update_workout_label(html, 'SWIM', 'SWIM BASE', '900m', '3 ×100 @ moderate')
html = update_workout_label(html, 'SWIM', 'SWIM BASE', '1000m', '4 ×100 @ moderate')
html = update_workout_label(html, 'SWIM', 'SWIM BASE', '1100m', '5 ×100 @ moderate')
html = update_workout_label(html, 'SWIM', 'SWIM BASE', '1200m', '6 ×100 @ moderate')

# Swim Base + Lactate (has VO2max intervals)
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1275m', 'VO2max')
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1000m', 'VO2max')
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1350m', 'VO2max')
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1400m', 'VO2max')
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1100m', 'VO2max')
html = update_workout_label(html, 'SWIM', 'SWIM BASE + LACTATE', '1500m', 'VO2max')

# Swim Threshold + Sprint (has threshold @ 200m or 300m intervals)
html = update_workout_label(html, 'SWIM', 'SWIM THRESHOLD + SPRINT', '1200m', '3 ×200 @ threshold')
html = update_workout_label(html, 'SWIM', 'SWIM THRESHOLD + SPRINT', '900m', '2 ×200 @ threshold')
html = update_workout_label(html, 'SWIM', 'SWIM THRESHOLD + SPRINT', '1400m', '4 ×200 @ threshold')
html = update_workout_label(html, 'SWIM', 'SWIM THRESHOLD + SPRINT', '1500m', '3 ×300 @ threshold')

# Update BIKE workouts
print("\\nUpdating BIKE workouts...")

# Foundation Bike (simple steady pace)
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '30 min', '10 min @ moderate')
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '45 min', '10 min @ moderate')
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '1:00', '40 min @ moderate')
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '1:15', '55 min @ moderate')
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '1:30', '1 hour and 10 min @ moderate')
html = update_workout_label(html, 'BIKE', 'FOUNDATION BIKE', '1:45', '1 hour and 25 min @ moderate')

# Bike Hill Climbs
html = update_workout_label(html, 'BIKE', 'BIKE SHORT HILL CLIMBS', '45 min', '4 ×1-minute hill climbs')
html = update_workout_label(html, 'BIKE', 'BIKE SHORT HILL CLIMBS', '50 min', '5 ×1-minute hill climbs')
html = update_workout_label(html, 'BIKE', 'BIKE SHORT HILL CLIMBS', '55 min', '6 ×1-minute hill climbs')

html = update_workout_label(html, 'BIKE', 'BIKE LONG HILL CLIMBS', '1:00', '2 ×5-minute hill climbs')
html = update_workout_label(html, 'BIKE', 'BIKE LONG HILL CLIMBS', '1:05', '3 ×5-minute hill climbs')
html = update_workout_label(html, 'BIKE', 'BIKE LONG HILL CLIMBS', '1:10', '4 ×5-minute hill climbs')

# Bike Lactate Intervals
html = update_workout_label(html, 'BIKE', 'BIKE LACTATE INTERVALS', '1:00', '2 ×3-minute intervals @ VO2max')
html = update_workout_label(html, 'BIKE', 'BIKE LACTATE INTERVALS', '1:15', '4 ×3-minute intervals @ VO2max')

# Tempo Bike
html = update_workout_label(html, 'BIKE', 'TEMPO BIKE', '45 min', '2 ×10 min @ threshold')
html = update_workout_label(html, 'BIKE', 'TEMPO BIKE', '55 min', '22 min @ threshold')
html = update_workout_label(html, 'BIKE', 'TEMPO BIKE', '1:05', '24 min @ threshold')

# Long Bike
html = update_workout_label(html, 'BIKE', 'LONG BIKE', '2:00', '1 hour and 40 min @ moderate')

# Recovery Bike
html = update_workout_label(html, 'BIKE', 'RECOVERY BIKE', '20 min', '10 min @ recovery')

# Update RUN workouts
print("\\nUpdating RUN workouts...")

# Foundation Run
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '25 min', 'Run 5 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '30 min', 'Run 10 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '35 min', 'Run 15 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '40 min', 'Run 20 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '45 min', 'Run 25 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '50 min', 'Run 30 min @ moderate')
html = update_workout_label(html, 'RUN', 'FOUNDATION RUN', '55 min', 'Run 35 min @ moderate')

# Run Lactate Intervals
html = update_workout_label(html, 'RUN', 'RUN LACTATE INTERVALS', '32 min', '12 ×30 seconds @ VO2max')
html = update_workout_label(html, 'RUN', 'RUN LACTATE INTERVALS', '34 min', '14 ×30 seconds @ VO2max')
html = update_workout_label(html, 'RUN', 'RUN LACTATE INTERVALS', '36 min', '8 ×1 minute @ VO2max')
html = update_workout_label(html, 'RUN', 'RUN LACTATE INTERVALS', '40 min', '10 ×1 minute @ VO2max')

# Tempo Run
html = update_workout_label(html, 'RUN', 'TEMPO RUN', '30 min', 'Run 10 min @ threshold')
html = update_workout_label(html, 'RUN', 'TEMPO RUN', '32 min', 'Run 12 min @ threshold')
html = update_workout_label(html, 'RUN', 'TEMPO RUN', '36 min', 'Run 16 min @ threshold')

# Long Run
html = update_workout_label(html, 'RUN', 'LONG RUN', '1:05', 'Run 45 min @ moderate')

print("\\nWriting updated HTML...")
with open('blog/2025_11_12_16_week_olympic_triathlon_training_plan.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\\n✅ Done! All workout labels have been updated.")
