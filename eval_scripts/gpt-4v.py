import csv

from openai import OpenAI

# 1. Load dataset

rows = []

with open('data.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Load model

client = OpenAI()

# 3. Evaluate model

for i in range(len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\n\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}.\n"
    url = f"https://cavendishlabs.org/rebus/images/{filename}"

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=2000,
        )

        print(url)
        print(response.choices[0].message.content)

        # Write the output to a file
        with open("gpt4v_output.txt", "a") as f:
            f.write(url + "\n")
            f.write(response.choices[0].message.content + "\n")
            f.write("\n\n")
    except:
        print("Error")
