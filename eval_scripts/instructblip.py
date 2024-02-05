import os
import csv

from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
import requests


# 1. Load dataset

rows = []

with open('data.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-flan-t5-xxl", torch_dtype=torch.float16, device_map="auto")
processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-flan-t5-xxl")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

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

    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device, torch.float16)

    outputs = model.generate(
        **inputs,
        do_sample=False,
        num_beams=5,
        max_length=3000,
        min_length=1,
        top_p=0.9,
        repetition_penalty=1.5,
        length_penalty=1.0,
        temperature=1,
    )

    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    print(generated_text)

    with open("instructblip_output.txt", "a") as f:
        f.write(url + "\n")
        f.write(generated_text + "\n")
        f.write("\n\n")
