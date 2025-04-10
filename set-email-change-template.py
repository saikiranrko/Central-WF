#!/usr/bin/env python3
import os
import sys

# Check if we have enough arguments
if len(sys.argv) < 8:
    print("Usage: python set-email-change-template.py <to> <change> <change_window> <impact> <summary> <action> <note>")
    sys.exit(1)

to_input = sys.argv[1]
change = sys.argv[2]
change_window = sys.argv[3]
impact = sys.argv[4]
summary = sys.argv[5]
action = sys.argv[6]
note = sys.argv[7]

# The multiline inputs are already formatted with <br> tags by the workflow

# Determine the template file path
template_file = 'email_change_template.html'

# Check if the template file exists with different naming
if not os.path.exists(template_file):
    possible_names = [
        'email_change_template (3).html',
        'email_change_template.html',
        'template.html'
    ]
    
    for name in possible_names:
        if os.path.exists(name):
            template_file = name
            break
    else:
        print(f"Error: Template file not found. Looked for: {', '.join(possible_names)}")
        sys.exit(1)

# Read the HTML template from the file
try:
    with open(template_file, 'r', encoding='utf-8') as file:
        html_template = file.read()
except Exception as e:
    print(f"Error reading template file: {e}")
    sys.exit(1)

# Generate the final HTML content by replacing placeholders
html_content = html_template \
    .replace('{{to_placeholder}}', to_input) \
    .replace('{{change_placeholder}}', change) \
    .replace('{{change_window_placeholder}}', change_window) \
    .replace('{{impact_placeholder}}', impact) \
    .replace('{{change_summary_placeholder}}', summary) \
    .replace('{{action_needed_placeholder}}', action) \
    .replace('{{note_placeholder}}', note)

# Write HTML content to a file
file_path = 'email.html'
try:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"HTML content written to {file_path}")
except Exception as e:
    print(f"Error writing output file: {e}")
    sys.exit(1)
