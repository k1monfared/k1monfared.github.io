#!/usr/bin/env python3
"""
Add proper workout type labels (Foundation, Tempo, Lactate, etc.) to the HTML
"""

# Read HTML
with open('blog/2025_11_12_16_week_olympic_triathlon_training_plan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define replacements based on week and workout characteristics
replacements = [
    # Week 1-2: Foundation workouts and Swim Base
    ('<span class="workout-icon">🏊</span> SWIM</div>\n            <span class="workout-duration">800m</span>\n        </div>\n        <ul class="workout-details">\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part"><span class="label">WU:</span></span>\n                    <span class="detail-part">200 @ easy</span>\n                </div>\n            </li>\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part">4 ×25 drills, RI (Rest Interval)=0:10</span>',
     '<span class="workout-icon">🏊</span> SWIM BASE</div>\n            <span class="workout-duration">800m</span>\n        </div>\n        <ul class="workout-details">\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part"><span class="label">WU:</span></span>\n                    <span class="detail-part">200 @ easy</span>\n                </div>\n            </li>\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part">4 ×25 drills, RI (Rest Interval)=0:10</span>'),

    # Swim Base 900m
    ('<span class="workout-icon">🏊</span> SWIM</div>\n            <span class="workout-duration">900m</span>\n        </div>\n        <ul class="workout-details">\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part"><span class="label">WU:</span></span>\n                    <span class="detail-part">200 @ easy</span>\n                </div>\n            </li>\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part">4 ×25 drills, RI (Rest Interval)=0:10</span>',
     '<span class="workout-icon">🏊</span> SWIM BASE</div>\n            <span class="workout-duration">900m</span>\n        </div>\n        <ul class="workout-details">\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part"><span class="label">WU:</span></span>\n                    <span class="detail-part">200 @ easy</span>\n                </div>\n            </li>\n            <li>\n                <span class="bullet">▸</span>\n                <div class="detail-content">\n                    <span class="detail-part">4 ×25 drills, RI (Rest Interval)=0:10</span>'),
]

# Apply replacements
for old, new in replacements:
    html = html.replace(old, new)

# Write back
with open('blog/2025_11_12_16_week_olympic_triathlon_training_plan.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Workout labels updated!")
