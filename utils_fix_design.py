import os
import re

# Directories
content_dir = "content/ielts"

# HTML Template for the Table
table_template = """
<div class="overflow-hidden rounded-xl border border-slate-200 shadow-sm mt-8">
    <table class="w-full text-sm text-left text-slate-600">
        <thead class="text-xs text-slate-700 uppercase bg-slate-50 border-b border-slate-200">
            <tr>
                <th scope="col" class="px-6 py-4 font-bold">Question Number</th>
                <th scope="col" class="px-6 py-4 font-bold text-center">Correct Answer</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-slate-100">
            {rows}
        </tbody>
    </table>
</div>
"""

row_template = """
            <tr class="hover:bg-blue-50/50 transition-colors">
                <td class="px-6 py-4 font-medium text-slate-900 border-r border-slate-50">{q}</td>
                <td class="px-6 py-4 font-bold text-primary text-center tracking-wide">{a}</td>
            </tr>
"""

# New SEO/Info Section Template
seo_section_template = """
<div class="mt-16 bg-slate-50 rounded-2xl p-8 border border-slate-100">
    <h3 class="text-xl font-display font-bold text-slate-900 mb-4">About the IELTS Reading Test</h3>
    <div class="prose prose-slate text-sm text-slate-600 max-w-none">
        <p>
            Success in the **IELTS exam preparation** journey requires understanding the test format. The 
            **Academic Reading** module consists of 40 questions designed to test a wide range of reading skills. 
            Candidates have exactly **60 minutes** to read three long texts and verify their **IELTS reading answers**.
        </p>
        <p class="mt-4">
            Using authentic **Cambridge IELTS data** from past papers is the most reliable way to predict your performance. 
            Whether you are taking the **British Council IELTS** or **IDP IELTS** version, the marking criteria remain the same. 
            Consistently scoring 30+ out of 40 with our **IELTS Answer Key** indicates you are on track for a **high band score** (Band 7.0+). 
        </p>
        <p class="mt-4">
            Unlike the General Training Reading module, the Academic texts are taken from books, journals, magazines, and newspapers. 
            Regular practice with these **Cambridge Reading Answers** will help you improve your speed and accuracy for the actual test. 
            Our **Free IELTS Material** is updated regularly to reflect the difficulty of the **recent IELTS test** standards.
        </p>
    </div>
</div>
"""

def parse_broken_table(content):
    data = []
    # Find the block where the table is. relying on '|' char
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('|') and 'Question' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                data.append((parts[0], parts[1]))
    return data

# Process files
files = os.listdir(content_dir)
for f in files:
    if not f.endswith('.md') or f == '_index.md':
        continue
    
    file_path = os.path.join(content_dir, f)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract Book and Test Info from content or filename
    # cambridge-10-test-1.md
    match = re.match(r"cambridge-(\d+)-test-(\d+)\.md", f)
    if not match:
        continue
    
    book_num = match.group(1)
    test_num = match.group(2)
    
    # Extract Data
    rows_data = parse_broken_table(content)
    
    # Build HTML Table
    rows_html = ""
    for q, a in rows_data:
        rows_html += row_template.format(q=q, a=a)
    
    if not rows_html:
        rows_html = '<tr><td colspan="2" class="px-6 py-4 text-center italic text-slate-400">Answers verification pending for this test.</td></tr>'
        
    final_table = table_template.format(rows=rows_html)
    
    # New File Content
    # We keep the frontmatter but update description/keywords slightly? No, stick to what worked, just update BODY.
    
    # Extract existing frontmatter
    fm_end_idx = content.find('---', 3)
    if fm_end_idx == -1: continue
    
    frontmatter = content[:fm_end_idx+3]
    
    new_body = f"""

<div class="max-w-4xl mx-auto">

    <div class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-display font-extrabold text-slate-900 mb-4">Cambridge Book {book_num} Test {test_num}</h1>
        <p class="text-xl text-primary font-medium">Reading Answer Key</p>
    </div>

    <div class="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden p-6 md:p-8">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                <svg class="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Verified Answers
            </h2>
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-600 border border-blue-100">
                Academic Module
            </span>
        </div>

        {final_table}
    </div>

    {seo_section_template}

</div>
"""
    
    final_content = frontmatter + new_body
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(final_content)
        
    print(f"Fixed design for {f}")
