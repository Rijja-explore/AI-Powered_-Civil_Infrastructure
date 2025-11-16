#!/usr/bin/env python3
"""Remove 5 static demo data blocks from Analytics.jsx"""
import re

# Read the file
filepath = 'frontend/src/pages/Analytics.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original_length = len(content)

# Define the 5 blocks to remove as regex patterns
# Each pattern matches from the comment through the closing </div>
patterns = [
    # Correlation Matrix Analysis - from comment to closing </div>
    r'\n\s+{/\* Correlation Matrix Analysis \*/}\s+<div className="chart-panel">.*?</div>\s+{/\* Regression Analysis \*/}',
    # Distribution Analysis - from comment to Comprehensive Suite comment
    r'\n\s+{/\* Distribution Analysis \*/}\s+<div className="chart-panel">.*?</div>\s+{/\* Comprehensive Statistical Analysis Suite \*/}',
    # Frequency Distribution Analysis - from comment to Z-Score comment
    r'\n\s+{/\* Frequency Distribution Analysis \*/}\s+<div className="chart-panel large">.*?</div>\s+{/\* Z-Score Analysis & Standard Normal Distribution \*/}',
    # Z-Score Analysis - from comment to Environmental Impact comment
    r'\n\s+{/\* Z-Score Analysis & Standard Normal Distribution \*/}\s+<div className="chart-panel">.*?<Zap size={22} /}\s+Environmental Impact',
    # Hypothesis Testing Suite - from comment to end before closing grid
    r'\n\s+{/\* Hypothesis Testing Suite \*/}\s+<div className="chart-panel large">.*?console\.error\(\'Error rendering Hypothesis Testing Suite:\',\s*error\);\s+return <div className="chart-error">Chart temporarily unavailable</div>;\s+}\s+}\)\(\)}\s+</div>\s+</div>',
]

# These are too complex - let's use a simpler line-based approach
# Read line by line and identify block boundaries

lines = content.split('\n')
result_lines = []
skip_until = None
skip_patterns = [
    'Correlation Matrix Analysis',
    'Distribution Analysis', 
    'Frequency Distribution Analysis',
    'Z-Score Analysis & Standard Normal Distribution',
    'Hypothesis Testing Suite'
]

in_block = False
block_depth = 0
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this line starts one of the blocks to remove
    is_block_start = any(pattern in line for pattern in skip_patterns)
    
    if is_block_start and '{/*' in line:
        # Found start of a block to remove
        result_lines.append(line)  # Keep the comment line for now
        i += 1
        
        # Skip until we find the matching closing </div>
        # Count opening and closing divs
        div_count = 1
        while i < len(lines) and div_count > 0:
            l = lines[i]
            # Count div tags
            div_count += l.count('<div')
            div_count -= l.count('</div>')
            
            if div_count > 0:
                result_lines.pop()  # Remove the comment line we added
                i += 1
                continue
            else:
                # Found the closing div
                i += 1
                break
    else:
        result_lines.append(line)
        i += 1

new_content = '\n'.join(result_lines)
new_length = len(new_content)

print(f"Original: {original_length} chars, {len(lines)} lines")
print(f"New: {new_length} chars, {len(result_lines)} lines")
print(f"Removed: {original_length - new_length} chars, {len(lines) - len(result_lines)} lines")

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done!")
