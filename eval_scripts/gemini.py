import base64
import csv
import json

import requests

# 1. Load dataset

rows = []

with open('dataset.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    headers = next(csv_reader)

    for row in csv_reader:
        rows.append(row)

# 2. Evaluate model

for i in range(len(rows)):
    current_row = rows[i]
    filename = current_row[0]
    correct_answer = current_row[1]
    also_correct_answer = current_row[2]
    category = current_row[3]

    prompt = f"This rebus puzzle is a play on words based on images, and may contain text, logical operators, addition/subtraction of letters, and other forms of creative thinking to solve. Can you figure out what it is? The category for this puzzle is {category}; that is, your answer should match the category in order to be correct.\\n\\nTake a deep breath, and let's begin. You can think for as long as you want, until you get a correct answer in the category {category}. When you're done reasoning and thinking, output your final answer in three braces, like {{{{{{this}}}}}}.\\n"
    im_url = f"https://cavendishlabs.org/rebus/images/{filename}"

    image = base64.b64encode(requests.get(im_url).content).decode("utf-8")

    request = f"""{{"contents":[{{"parts":[{{"text": "{prompt}"}},{{"inline_data": {{"mime_type":"image/jpeg","data": "{image}"}}}}]}}]}}"""

    # The URL for the API request
    api_key = "your-key-here"
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}'

    # Set the headers
    headers = {'Content-Type': 'application/json'}

    # print(request)
    jsonified_request = json.loads(request)

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=jsonified_request)

        # Check if the request was successful
        if response.status_code == 200:
                # Extract and print the text from the response
                response_data = response.json()

                output = response_data['candidates'][0]['content']['parts'][0]['text']

                print(im_url)
                print(output)

                # Write the output to a file
                with open("gemini_output.txt", "a") as f:
                    f.write(im_url + "\n")
                    f.write(output + "\n")
                    f.write("\n\n")
        else:
            print(f"Error: {response.status_code}")
    except:
        print("Error")
