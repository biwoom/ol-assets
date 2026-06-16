#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def extract_korean(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if yaml_match:
        yaml_block = f"---\n{yaml_match.group(1).strip()}\n---\n\n"
        body_content = yaml_match.group(2)
    else:
        yaml_block = ""
        body_content = content
        
    # Split main body and footnotes section
    # Use case-insensitive search for '## 각주'
    parts = re.split(r'^##\s*각주\s*$', body_content, flags=re.MULTILINE | re.IGNORECASE)
    main_body = parts[0]
    footnotes_body = parts[1] if len(parts) > 1 else ""
    
    # Helper to extract elements from a section
    def parse_section(text, is_footnotes=False):
        elements = []
        lines = text.split('\n')
        in_ko = False
        current_ko_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped == '[KO]':
                in_ko = True
                current_ko_lines = []
                continue
            elif stripped == '[/KO]':
                in_ko = False
                if current_ko_lines:
                    # Clean empty lines at start/end of current block
                    while current_ko_lines and not current_ko_lines[0].strip():
                        current_ko_lines.pop(0)
                    while current_ko_lines and not current_ko_lines[-1].strip():
                        current_ko_lines.pop()
                    if current_ko_lines:
                        elements.append('\n'.join(current_ko_lines))
                current_ko_lines = []
                continue
                
            if in_ko:
                current_ko_lines.append(line)
            else:
                # If we are not in KO block, we only keep structural headers (like '## 본문') in the main body.
                # All other English headings (h1-h5) are ignored because they are translated in [KO] blocks.
                if not is_footnotes and line.startswith('#'):
                    if re.match(r'^##\s*본문\s*$', line.strip(), re.IGNORECASE):
                        elements.append(line)
                    
        if in_ko:
            print(f"Warning: Unclosed [KO] block detected in {input_path.name}")
            # Append whatever was left
            if current_ko_lines:
                elements.append('\n'.join(current_ko_lines))
                
        return elements

    # Parse main body elements
    body_elements = parse_section(main_body, is_footnotes=False)
    
    # Parse footnotes elements
    footnote_elements = parse_section(footnotes_body, is_footnotes=True)
    
    # Reconstruct final content
    output_parts = []
    
    # 1. YAML Frontmatter
    if yaml_block:
        output_parts.append(yaml_block.strip())
        
    # 2. Main Body (joined by double newlines)
    cleaned_body_elements = [elem.strip() for elem in body_elements if elem.strip()]
    if cleaned_body_elements:
        output_parts.append('\n\n'.join(cleaned_body_elements))
        
    # 3. Footnotes Section (if any footnotes exist)
    cleaned_footnote_elements = [elem.strip() for elem in footnote_elements if elem.strip()]
    if cleaned_footnote_elements:
        output_parts.append("## 각주")
        output_parts.append('\n\n'.join(cleaned_footnote_elements))
        
    # Join everything with double newlines
    final_output = '\n\n'.join(output_parts) + '\n'
    
    # Ensure directory exists and write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_output)
        
    print(f"Successfully extracted Korean-only manuscript to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 extract_korean.py <input_path> <output_path>")
        sys.exit(1)
        
    extract_korean(sys.argv[1], sys.argv[2])
