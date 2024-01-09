import os
import csv

import requests
from PIL import Image
import torch
from transformers import pipeline

# 1. Load datasaet

rows = []

with open('dataset.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

model_id = "llava-hf/llava-1.5-13b-hf"
pipe = pipeline("image-to-text", model=model_id)

# 3. Evaluate model

for i in range(len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"USER: <image>\nThis rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\n\nTake a deep breath, and let's begin. Spend at least two paragraphs thinking through the puzzle, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer.\nASSISTANT: Ok, here goes:"
    url = f"https://cavendishlabs.org/rebus/images/{filename}"

    # print(prompt)
    print(url)

    image = Image.open(requests.get(url, stream=True).raw)

    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 2000})

    print(outputs[0]['generated_text'])

    with open("llava_13b_output.txt", "a") as f:
        f.write(url + "\n")
        f.write(str(outputs[0]['generated_text']) + "\n")
        f.write("\n\n")
