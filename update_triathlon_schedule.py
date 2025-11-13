#!/usr/bin/env python3
"""
Update triathlon training plan HTML with correct schedule from tri.txt
Preserves all HTML structure, CSS, and JavaScript functionality
"""

import re
from typing import Dict, List, Tuple

def parse_tri_txt(filename: str) -> Dict[int, Dict[str, List[str]]]:
    """Parse tri.txt and return structured workout data by week and day"""

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    weeks = {}
    current_week = None
    current_day = None
    current_workout = []

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check for week header
        week_match = re.match(r'Week (\d+)', line)
        if week_match:
            week_num = int(week_match.group(1))
            if current_week is not None and current_day is not None:
                # Save previous workout
                if current_day not in weeks[current_week]:
                    weeks[current_week][current_day] = []
                weeks[current_week][current_day] = current_workout

            current_week = week_num
            if current_week not in weeks:
                weeks[current_week] = {}
            current_day = None
            current_workout = []
            i += 1
            continue

        # Skip week notes/descriptions
        if line.startswith('Week') and '\t' in line:
            i += 1
            continue

        # Check for day of week
        day_match = re.match(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\t(.+)', line)
        if day_match and current_week is not None:
            # Save previous workout if exists
            if current_day is not None and current_workout:
                if current_day not in weeks[current_week]:
                    weeks[current_week][current_day] = []
                weeks[current_week][current_day] = current_workout

            current_day = day_match.group(1)
            workout_line = day_match.group(2)
            current_workout = [workout_line]

            # Read continuation lines (lines that don't start with a day or week)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                # Check if it's a continuation line (starts with WU, MS, CD, or other workout details)
                if next_line and not next_line.startswith(('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Week', 'The ', 'This ')):
                    current_workout.append(next_line)
                    i += 1
                else:
                    break
            continue

        i += 1

    # Save last workout
    if current_week is not None and current_day is not None and current_workout:
        if current_day not in weeks[current_week]:
            weeks[current_week][current_day] = []
        weeks[current_week][current_day] = current_workout

    return weeks

def determine_workout_type(workout_text: str) -> Tuple[str, str, str]:
    """Determine workout type, icon, and card class from workout text"""
    text_lower = workout_text.lower()

    if 'rest day' in text_lower:
        return 'rest', '', ''
    elif 'brick' in text_lower:
        return 'BRICK', '🏋️', 'brick-card'
    elif 'race day' in text_lower or 'triathlon' in text_lower:
        return 'RACE', '🏁', 'race-card'
    elif 'swim' in text_lower:
        return 'SWIM', '🏊', 'swim-card'
    elif 'bike' in text_lower or 'cycle' in text_lower:
        return 'BIKE', '🚴', 'bike-card'
    elif 'run' in text_lower:
        return 'RUN', '🏃', 'run-card'
    else:
        return 'WORKOUT', '💪', 'brick-card'

def extract_duration(workout_lines: List[str]) -> str:
    """Extract workout duration/distance from workout lines"""
    first_line = workout_lines[0] if workout_lines else ''

    # Try to extract distance/duration from first line
    # Examples: "Swim: 800 Yards", "Foundation Bike: 30 Minutes", etc.
    if ':' in first_line:
        parts = first_line.split(':', 1)
        if len(parts) > 1:
            duration_part = parts[1].strip()

            # If the line contains WU:/MS:/CD:, extract only the duration before those markers
            wu_match = re.search(r'\s+(WU:|MS:|CD:)', duration_part)
            if wu_match:
                duration_part = duration_part[:wu_match.start()].strip()

            # Convert "800 Yards" to "800m"
            duration_part = re.sub(r'(\d+)\s*Yards?', r'\1m', duration_part)
            # Convert "30 Minutes" to "30 min", "1 Hour" to "1:00", etc.
            duration_part = re.sub(r'(\d+)\s*Minutes?', r'\1 min', duration_part)
            duration_part = re.sub(r'(\d+)\s*Hour', r'\1:00', duration_part)
            duration_part = re.sub(r'1:(\d+)', r'1:\1', duration_part)

            return duration_part

    return ''

def parse_workout_details(workout_lines: List[str]) -> List[Dict[str, str]]:
    """Parse workout detail lines into structured format"""
    details = []

    # Check if first line contains WU:/MS:/CD: all on one line
    first_line = workout_lines[0] if workout_lines else ''
    if 'WU:' in first_line and 'MS:' in first_line:
        # Split the first line into separate WU/MS/CD entries
        # Extract the part after the duration
        match = re.search(r':\s*[\d\.:]+\s*(?:Minutes?|min|Hour|Yards?)?\s+(WU:.+)', first_line)
        if match:
            combined_details = match.group(1)
            # Split by WU:, MS:, CD:
            parts = re.split(r'\s+(WU:|MS:|CD:)\s+', combined_details)

            # Reconstruct as label: content pairs
            i = 1  # Start at 1 to skip empty first element
            while i < len(parts) - 1:
                label = parts[i].replace(':', '').strip()
                content = parts[i + 1].strip()

                # Remove next label from content if present
                for next_label in ['WU:', 'MS:', 'CD:']:
                    if next_label in content:
                        content = content[:content.index(next_label)].strip()
                        break

                # Convert units
                content = re.sub(r'(\d+)\s*Yards?', r'\1m', content)
                content = re.sub(r'(\d+)\s*@', r'\1 @', content)
                content = re.sub(r'low aerobic intensity', 'easy', content)
                content = re.sub(r'moderate aerobic intensity', 'moderate', content)
                content = re.sub(r'threshold intensity', 'threshold', content)
                content = re.sub(r'recovery intensity', 'recovery', content)
                content = re.sub(r'VO2max intensity', 'VO2max', content)
                content = re.sub(r'speed intensity', 'speed', content)
                content = re.sub(r'Minutes', 'min', content)
                content = re.sub(r'minutes', 'min', content)
                content = re.sub(r'x\s*', '×', content)

                details.append({
                    'label': label,
                    'content': content
                })
                i += 2

            return details

    # Skip first line (workout title)
    for line in workout_lines[1:]:
        line = line.strip()
        if not line:
            continue

        # Check for WU, MS, CD, Transition Run, etc.
        detail = {}

        # Match patterns like "WU: ...", "MS: ...", "CD: ..."
        if line.startswith(('WU:', 'MS:', 'CD:', 'Transition Run:')):
            # Parse the line
            if ':' in line:
                label_part, content_part = line.split(':', 1)
                label = label_part.strip()
                content = content_part.strip()

                # Convert units
                content = re.sub(r'(\d+)\s*Yards?', r'\1m', content)
                content = re.sub(r'(\d+)\s*@', r'\1 @', content)
                content = re.sub(r'low aerobic intensity', 'easy', content)
                content = re.sub(r'moderate aerobic intensity', 'moderate', content)
                content = re.sub(r'threshold intensity', 'threshold', content)
                content = re.sub(r'recovery intensity', 'recovery', content)
                content = re.sub(r'VO2max intensity', 'VO2max', content)
                content = re.sub(r'speed intensity', 'speed', content)
                content = re.sub(r'Minutes', 'min', content)
                content = re.sub(r'minutes', 'min', content)
                content = re.sub(r'x\s*', '×', content)

                details.append({
                    'label': label,
                    'content': content
                })
        else:
            # It's a continuation or standalone line
            content = line
            content = re.sub(r'(\d+)\s*Yards?', r'\1m', content)
            content = re.sub(r'low aerobic intensity', 'easy', content)
            content = re.sub(r'moderate aerobic intensity', 'moderate', content)
            content = re.sub(r'threshold intensity', 'threshold', content)
            content = re.sub(r'recovery intensity', 'recovery', content)
            content = re.sub(r'VO2max intensity', 'VO2max', content)
            content = re.sub(r'speed intensity', 'speed', content)
            content = re.sub(r'x\s*', '×', content)
            content = re.sub(r'Minutes', 'min', content)
            content = re.sub(r'minutes', 'min', content)

            details.append({
                'label': '',
                'content': content
            })

    return details

def generate_workout_html(workout_lines: List[str]) -> str:
    """Generate HTML for a workout"""
    if not workout_lines:
        return '<td class="rest-day">REST</td>'

    # Check if it's a rest day
    if 'Rest day' in workout_lines[0] or 'REST' in workout_lines[0].upper():
        return '<td class="rest-day">REST</td>'

    workout_type, icon, card_class = determine_workout_type(workout_lines[0])
    duration = extract_duration(workout_lines)

    # Special case for race day
    if workout_type == 'RACE':
        race_details = '<br>'.join(workout_lines[1:])
        return f'''<td><div class="workout-card race-card">
        <div style="font-weight: bold; text-align: center;">
            {icon} RACE DAY!
        </div>
        <div style="margin-top: 8px; font-size: 0.85em; text-align: center;">
            {race_details}
        </div>
    </div></td>'''

    # Check if it's a brick workout (bike + transition run)
    if 'Transition Run' in '\n'.join(workout_lines):
        # Split into bike and run parts
        bike_lines = []
        run_lines = []
        in_run = False

        for line in workout_lines:
            if 'Transition Run' in line:
                in_run = True
                run_lines.append(line)
            elif in_run:
                run_lines.append(line)
            else:
                bike_lines.append(line)

        # Generate brick workout HTML
        bike_type, bike_icon, _ = determine_workout_type(bike_lines[0])
        run_type, run_icon, _ = determine_workout_type('Run')
        bike_duration = extract_duration(bike_lines)
        run_duration = extract_duration(run_lines)

        bike_details = parse_workout_details(bike_lines)
        run_details = parse_workout_details(run_lines)

        html = '<td>'

        # Bike workout
        html += f'''<div class="workout-card bike-card">
        <div class="workout-header">
            <div class="workout-type"><span class="workout-icon">{bike_icon}</span> {bike_type}</div>
            <span class="workout-duration">{bike_duration}</span>
        </div>
        <ul class="workout-details">'''

        for detail in bike_details:
            if detail['label']:
                html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part"><span class="label">{detail['label']}:</span></span>
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''
            else:
                html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''

        html += '</ul></div>'

        # Transition run
        html += f'''<div class="workout-card run-card">
        <div class="workout-header">
            <div class="workout-type"><span class="workout-icon">{run_icon}</span> {run_type}</div>
            <span class="workout-duration">{run_duration}</span>
        </div>
        <ul class="workout-details">'''

        for detail in run_details:
            if detail['label']:
                html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part"><span class="label">{detail['label']}:</span></span>
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''
            else:
                html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''

        html += '</ul></div></td>'
        return html

    # Regular workout
    details = parse_workout_details(workout_lines)

    html = f'''<td><div class="workout-card {card_class}">
        <div class="workout-header">
            <div class="workout-type"><span class="workout-icon">{icon}</span> {workout_type}</div>
            <span class="workout-duration">{duration}</span>
        </div>
        <ul class="workout-details">'''

    for detail in details:
        if detail['label']:
            html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part"><span class="label">{detail['label']}:</span></span>
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''
        else:
            html += f'''
            <li>
                <span class="bullet">▸</span>
                <div class="detail-content">
                    <span class="detail-part">{detail['content']}</span>
                </div>
            </li>'''

    html += '</ul></div></td>'
    return html

def generate_week_html(week_num: int, week_data: Dict[str, List[str]]) -> str:
    """Generate HTML for a complete week"""

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Generate table rows
    html = f'''<div class="week-wrapper">
<div class="table-wrapper">
<div class="week-label">WEEK {week_num}</div>
<table>
<thead><tr>
<th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th><th>Sunday</th>
</tr></thead>
<tbody><tr>
'''

    for day in days_order:
        if day in week_data:
            html += generate_workout_html(week_data[day])
        else:
            html += '<td class="rest-day">REST</td>'

    html += '''
</tr></tbody>
</table>
</div>
</div>

'''
    return html

# Main execution
print("Parsing tri.txt...")
weeks = parse_tri_txt('blog/tri.txt')

print(f"Found {len(weeks)} weeks of training data")

# Read the current HTML file
print("Reading HTML file...")
with open('blog/2025_11_!2_16_week_olympic_triathlon_training_plan.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Generate new schedule HTML
print("Generating new schedule...")
new_schedule = ''

# Base phase (weeks 1-6)
new_schedule += '<div class="phase-header">BASE PHASE (Weeks 1-6) - Build Aerobic Capacity & Endurance</div>\n'
for week_num in range(1, 7):
    if week_num in weeks:
        new_schedule += generate_week_html(week_num, weeks[week_num])

# Build phase (weeks 7-11)
new_schedule += '<div class="phase-header">BUILD PHASE (Weeks 7-11) - High-Intensity & Endurance Development</div>\n'
for week_num in range(7, 12):
    if week_num in weeks:
        new_schedule += generate_week_html(week_num, weeks[week_num])

# Peak phase (weeks 12-16)
new_schedule += '<div class="phase-header">PEAK PHASE (Weeks 12-16) - Race-Specific Training & Taper</div>\n'
for week_num in range(12, 17):
    if week_num in weeks:
        new_schedule += generate_week_html(week_num, weeks[week_num])

# Add source link
new_schedule += '''<div class="source-link">
    <p><strong>Source:</strong> This training plan is adapted from
    <a href="https://www.triathlete.com/training/olympic-triathlon-16-week-training-plan/" target="_blank">
    Triathlete Magazine's 16-Week Olympic Triathlon Training Plan</a></p>
</div>
'''

# Replace the schedule section in the HTML
# Find the start of the schedule (after control panel)
start_marker = '</div>\n\n<div class="phase-header">'
end_marker = '<script'

start_idx = html_content.find(start_marker)
if start_idx == -1:
    print("Error: Could not find schedule start marker")
    exit(1)

start_idx += len('</div>\n\n')  # Move past the control panel closing div

end_idx = html_content.find(end_marker, start_idx)
if end_idx == -1:
    print("Error: Could not find schedule end marker")
    exit(1)

# Replace the schedule
updated_html = html_content[:start_idx] + new_schedule + html_content[end_idx:]

# Write the updated HTML
print("Writing updated HTML...")
with open('blog/2025_11_!2_16_week_olympic_triathlon_training_plan.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("\n✅ Done! Schedule has been updated with correct workout data.")
print("All HTML structure, CSS, and JavaScript functionality preserved.")
