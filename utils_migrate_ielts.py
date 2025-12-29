import os
import re

# We will read from the restored content/ielts/reading directory
input_dir = "content/ielts/reading"
output_dir = "content/ielts"
os.makedirs(output_dir, exist_ok=True)

# Regex to parse the markdown table in the old format
def parse_table_content(content):
    # Find lines starting with | number |
    rows = []
    # Structure in old file: | Q | Ans | Q | Ans | Q | Ans |
    # We want to flatten this to just dict of {q_num: ans}
    
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('|') and 'Ans' not in line and '---' not in line:
            # Clean and split
            parts = [p.strip() for p in line.split('|') if p.strip()]
            
            # parts should look like [1, FALSE, 14, v, 27, D]
            # iterate in pairs
            for i in range(0, len(parts), 2):
                if i+1 < len(parts):
                    q = parts[i]
                    a = parts[i+1]
                    if q and a:
                        rows.append((q, a))
    
    # Sort by question num
    def try_int(x):
        try:
            return int(x)
        except:
            return 999
    
    rows.sort(key=lambda x: try_int(x[0]))
    return rows

# Store data: book_num -> test_num -> list of (q, ans)
book_data = {}

# Scan input 1-20
files = os.listdir(input_dir)
for f in files:
    # Pattern: cambridge-7-test-1.md
    match = re.match(r"cambridge-(\d+)-test-(\d+)\.md", f)
    if match:
        book_num = int(match.group(1))
        test_num = int(match.group(2))
        
        if book_num < 7 or book_num > 20: 
            # Skip book 1-6 as per user request
            # (Though user said they "added 7 to 20")
            continue 

        with open(os.path.join(input_dir, f), 'r', encoding='utf-8') as file:
            content = file.read()
            data = parse_table_content(content)
            
            if book_num not in book_data:
                book_data[book_num] = {}
            book_data[book_num][test_num] = data

# Now generate the new files for Books 7-20
template_header = """---
title: "Cambridge IELTS Book {number} Reading Answers (Test 1, 2, 3, 4)"
slug: "ielts-cambridge-book-{number}-reading-answers"
date: 2024-01-01
layout: "single"
type: "page"
description: "Get the complete and verified IELTS Reading Answers for Cambridge Book {number}. Improve your band score with our daily exam keys."
keywords: ["IELTS", "IELTS Reading Answers", "Cambridge IELTS Answers", "IELTS Exam Keys", "IELTS Prediction"]
---

Looking for the verified **IELTS reading answers** for Cambridge Book {number}? You have come to the right place. Our database provides accurate **Cambridge IELTS data** and exam keys to help you achieve a **high band score**. Whether you are beginning your **IELTS exam preparation** or reviewing a **recent IELTS test**, these answer keys are essential for your success.

## Cambridge IELTS Book {number} Reading Answers

Here are the complete answers for all four tests in Book {number}.

"""

for book_num in range(7, 21):
    # User requested Books 7 to 20
    filename = f"ielts-cambridge-book-{book_num}-reading-answers.md"
    file_path = os.path.join(output_dir, filename)
    
    final_content = template_header.format(number=book_num)
    
    # Append 4 tables
    for test_num in range(1, 5):
        final_content += f"\n### Test {test_num}\n\n"
        
        # Check if we have data
        if book_num in book_data and test_num in book_data[book_num]:
            rows = book_data[book_num][test_num]
            if rows:
                final_content += "| Question | Answer |\n| :---: | :---: |\n"
                for q, a in rows:
                    final_content += f"| {q} | {a} |\n"
            else:
                final_content += "_Answers not available yet._\n"
        else:
             final_content += "_Answers not available yet._\n"
        
        final_content += "\n<br>\n" # Spacer

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"Generated {filename} with restored data")

# Cleanup
# We will NOT delete the input_dir here within python, better to do it in shell
