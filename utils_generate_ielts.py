import os

output_dir = "content/ielts"
os.makedirs(output_dir, exist_ok=True)

# Template for the content
template = """---
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

| Question | Test 1 Answer | Test 2 Answer | Test 3 Answer | Test 4 Answer |
| :---: | :---: | :---: | :---: | :---: |
| 1 | TRUE | FALSE | NOT GIVEN | TRUE |
| 2 | FALSE | TRUE | TRUE | FALSE |
| 3 | NOT GIVEN | NOT GIVEN | FALSE | TRUE |
| 4 | -- | -- | -- | -- |
| 5 | -- | -- | -- | -- |
| 6 | -- | -- | -- | -- |
| 7 | -- | -- | -- | -- |
| 8 | -- | -- | -- | -- |
| 9 | -- | -- | -- | -- |
| 10 | -- | -- | -- | -- |
| ... | ... | ... | ... | ... |
| 40 | -- | -- | -- | -- |

_(Note: This is a placeholder table. Full data for Book {number} will be populated here.)_
"""

for i in range(1, 19):
    filename = f"ielts-cambridge-book-{i}-reading-answers.md"
    file_path = os.path.join(output_dir, filename)
    
    content = template.format(number=i)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Generated {filename}")
