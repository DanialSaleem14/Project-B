import os
import re

# Directories
input_dir = "content/ielts"
output_dir = "content/ielts" # We will overwrite/add here. 

# Reading existing Book files to extract data table
# Filename pattern: ielts-cambridge-book-{number}-reading-answers.md

def parse_markdown_tables(content):
    """
    Parses the Book markdown content and extracts tables for Test 1, 2, 3, 4.
    Returns a dict: {1: [(q, a)...], 2: ..., 3: ..., 4: ...}
    """
    tests_data = {}
    current_test = None
    
    lines = content.split('\n')
    for line in lines:
        # Detect Test Header
        test_match = re.search(r'### Test (\d+)', line)
        if test_match:
            current_test = int(test_match.group(1))
            tests_data[current_test] = []
            continue
            
        # Parse Table Row
        if current_test is not None:
             if line.strip().startswith('|') and 'Question' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2:
                    q = parts[0]
                    a = parts[1]
                    tests_data[current_test].append((q, a))
    return tests_data

# Process specific books (7-20)
for book_num in range(7, 21):
    input_filename = f"ielts-cambridge-book-{book_num}-reading-answers.md"
    input_path = os.path.join(input_dir, input_filename)
    
    if not os.path.exists(input_path):
        print(f"Skipping {input_filename}, not found.")
        continue
        
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    extracted_data = parse_markdown_tables(content)
    
    # Generate 4 individual test files
    for test_num in range(1, 5):
        # Data for this test
        rows = extracted_data.get(test_num, [])
        
        # New Filename
        new_filename = f"cambridge-{book_num}-test-{test_num}.md"
        new_file_path = os.path.join(output_dir, new_filename)
        
        # SEO Keywords string
        keywords_str = '"IELTS, IELTS Reading, Cambridge IELTS, IELTS Answer Key, IELTS Exam Preparation, IELTS Test {}, Cambridge Reading Answers, Free IELTS Material, British Council IELTS, IDP IELTS, Academic Reading, General Training Reading"'.format(book_num)
        
        # Table MD
        table_md = "| Question | Answer |\n| :---: | :---: |\n"
        if rows:
            for q, a in rows:
                table_md += f"| {q} | {a} |\n"
        else:
            table_md += "| - | - |\n\n_Answers coming soon._"
            
        # Content Template
        file_content = f"""---
title: "Cambridge IELTS Book {book_num} Test {test_num} Reading Answers"
url: "/answers/cambridge-{book_num}-test-{test_num}/"
date: 2024-01-01
layout: "single"
type: "page"
description: "Get the complete and verified IELTS Reading Answers for Cambridge Book {book_num} Test {test_num}. Prepare for your exam with accurate keys."
keywords: [{keywords_str}]
---

<div class="max-w-3xl mx-auto">

<div class="mb-8">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Reading Answer Key</h2>
    <p class="text-slate-600 leading-relaxed mb-6">
        Looking for the **verified IELTS reading answers** for **Cambridge Book {book_num} Test {test_num}**? You have come to the right place. 
        Our database provides accurate **Cambridge IELTS data** and exam keys to help you achieve a **high band score**. 
        Whether you are beginning your **IELTS exam preparation** or reviewing a **recent IELTS test**, these answer keys are essential for your success. 
        Get the edge with our free **British Council IELTS** and **IDP IELTS** compatible material.
    </p>
</div>

<div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
    <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex justify-between items-center">
        <span class="font-bold text-slate-700">Test {test_num} Answers</span>
        <span class="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded border border-slate-200">Verified</span>
    </div>
    <div class="overflow-x-auto">
        <!-- Rendered Table -->
        {table_md}
    </div>
</div>

<div class="mt-12 p-6 bg-slate-50 rounded-xl border border-dashed border-slate-300">
    <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">SEO Context</h3>
    <p class="text-sm text-slate-400">
        Mastering **IELTS Reading** requires consistent practice with **Cambridge IELTS** materials. 
        This page provides the **IELTS Answer Key** for **IELTS Test {book_num}**, specifically targeting **Academic Reading** and **General Training Reading** modules. 
        Use this **Free IELTS Material** to score 8.0+ in your exam.
    </p>
</div>

</div>
"""
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
    print(f"Processed Book {book_num} -> 4 Test files created.")
    
    # Remove old file
    os.remove(input_path)
    print(f"Removed old file: {input_filename}")

print("Migration Complete.")
