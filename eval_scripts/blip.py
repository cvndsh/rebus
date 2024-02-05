import os
import csv

import torch
import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration


# 1. Load dataset

rows = []

with open('data.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xxl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xxl", torch_dtype=torch.float16, device_map="auto")

# 3. Evaluate model

for i in range(len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\n\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}. Make sure to think for at least a few paragraphs before outputting a final answer.\n"
    url = f"https://cavendishlabs.org/rebus/images/{filename}"

    # print(prompt)
    print(url)

    image = Image.open(requests.get(url, stream=True).raw).convert('RGB')

    inputs = processor(image, prompt, return_tensors="pt").to("cuda", torch.float16)

    out = model.generate(**inputs, max_new_tokens=3000)

    print(processor.decode(out[0], skip_special_tokens=True))

    with open("blip2-flan-t5-xxl_output.txt", "a") as f:
        f.write(url + "\n")
        f.write(processor.decode(out[0], skip_special_tokens=True) + "\n")
        f.write("\n\n")
