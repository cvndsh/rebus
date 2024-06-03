import sys

from transformers import FuyuProcessor, FuyuForCausalLM
from PIL import Image
import requests
import csv


# 1. Load datasaet

rows = []

with open('dataset.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

model_id = "adept/fuyu-8b"
processor = FuyuProcessor.from_pretrained(model_id)
model = FuyuForCausalLM.from_pretrained(model_id)

# 3. Evaluate model

for i in range(4, 7):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    text_prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\n\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}.\n"
    url = f"https://cavendishlabs.org/rebus/images/{filename}"

    print(text_prompt)
    print(url)

    image = Image.open(requests.get(url, stream=True).raw)

    inputs = processor(text=text_prompt, images=image, return_tensors="pt")#.to("mps")

    # autoregressively generate text
    generation_output = model.generate(**inputs, max_new_tokens=2000)
    generation_text = processor.batch_decode(generation_output[:, -2000:], skip_special_tokens=True)
    print(generation_text)
I