import base64
import csv
import json

import requests
import google.generativeai as genai
import httpx

# 1. Load dataset

rows = []

with open('dataset.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

genai.configure(api_key="xxx")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
# 3. Evaluate model

for i in range(179, len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\\n\\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}.\\n"
    im_url = f"https://cavendishlabs.org/rebus/images/{filename}"

    while True:
        try:
            # Save https://cavendishlabs.org/rebus/images/0001.jpg to 0001.jpg
            with httpx.Client() as client:
                response = client.get(f"https://cavendishlabs.org/rebus/images/{filename}")
                with open(filename, "wb") as file:
                    file.write(response.content)

            convo = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [genai.upload_file(filename)],
                },
            ])

            convo.send_message(
                f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\\\\n\\\\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}. Don't forget to think aloud before giving a final answer!\\\\n")
            answer = convo.last.text

            print(im_url)
            print(answer)

            # Write the output to a file
            with open("gemini_1.5_output.txt", "a") as f:
                f.write(im_url + "\n")
                f.write(answer + "\n")
                f.write("\n\n")

            break
        except Exception as e:
            print("Error")
            print(e)
