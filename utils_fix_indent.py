import os

content_dir = "content/ielts"

files = os.listdir(content_dir)
count = 0

for f in files:
    if f.endswith(".md") and f.startswith("cambridge-"):
        path = os.path.join(content_dir, f)
        
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        new_lines = []
        is_frontmatter = False
        fm_dashes = 0
        
        for line in lines:
            stripped = line.lstrip()
            
            # Preserve Frontmatter structure exactly, though usually it's fine.
            # But crucial logic: if it's NOT frontmatter, we want to remove leading indent.
            # Markdown code blocks are triggered by 4 spaces indent.
            
            # Simple heuristic: Just strip ALL leading whitespace for HTML lines.
            # HTML doesn't care about indentation.
            
            if line.strip() == "---":
                fm_dashes += 1
                new_lines.append(line)
                continue
                
            if fm_dashes < 2:
                # We are in frontmatter, keep as is (indentation matters for YAML lists)
                new_lines.append(line)
            else:
                # We are in content body.
                # If it's an empty line, keep it.
                if not line.strip():
                    new_lines.append(line)
                else:
                    # Remove all leading spaces/tabs
                    new_lines.append(stripped)
        
        with open(path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
            
        count += 1

print(f"Fixed indentation for {count} files.")
