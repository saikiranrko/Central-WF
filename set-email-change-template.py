import os
import sys

to_input = sys.argv[1]
change = sys.argv[2]
change_window = sys.argv[3]
impact = sys.argv[4]
summary = sys.argv[5]
action = sys.argv[6]
note = sys.argv[7]



# Read the HTML template from the file
with open('email_change_template.html', 'r') as file:
    html_template = file.read()

# Generate the final HTML content by replacing placeholders
html_content = html_template.replace('{{to_placeholder}}', to_input).replace('{{change_placeholder}}', change).replace('{{change_window_placeholder}}', change_window).replace('{{impact_placeholder}}', impact).replace('{{change_summary_placeholder}}', summary).replace('{{action_needed_placeholder}}', action).replace('{{note_placeholder}}', note)

print(html_content)

# Write HTML content to a file
file_path = 'email.html'
with open(file_path, 'w') as file:
    file.write(html_content)

print(f"HTML content written to {file_path}")
