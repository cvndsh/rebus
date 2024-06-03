import base64
import csv
from io import BytesIO

import anthropic
import httpx
from PIL import Image

# 1. Load dataset

rows = []

with open('dataset.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

client = anthropic.Anthropic(
    api_key=API_KEY,
)

# 3. Evaluate model

for i in range(len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\n\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}.\n"
    url = f"https://cavendishlabs.org/rebus/images/{filename}"
    image_data = base64.b64encode(httpx.get(url).content).decode("utf-8")
    image_media_type = Image.MIME[Image.open(BytesIO(base64.b64decode(image_data))).format]

    # try:
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    print(url)
    print(message.content[0].text)
    print()
    print()

    # Write the output to a file
    with open("claude_sonnet_output.txt", "a") as f:
        f.write(url + "\n")
        f.write(message.content[0].text + "\n")
        f.write("\n\n")
    # except:
    #     print("Error")
