# Brew install tesseract, poppler

from flask import Flask, request, jsonify
from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv
import requests
import json
import ast 
import io
from pdf2image import convert_from_bytes

app = Flask(__name__)

@app.route('/upload_manual', methods=['POST'])
def upload_manual():
    print('started')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_stream = uploaded_file.read()
    try:
        images = convert_from_bytes(file_stream)
    except Exception as e:
        return jsonify({'error': 'Failed to convert PDF', 'message': str(e)})


    pdf_string = ''
    # Extract text from the image
    for page_number, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        pdf_string += f'Page number: {page_number+1}'
        pdf_string += text

    # Extract the text from the troubleshooting section from the string using ChatGPT


    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You will be provided with a string that represents the contents of a user manual. Your job is to return two elements in a list, 1)the exact text which contains the information about troubleshooting and 2) the page where this string is found. The page number is indicated in the page with 'Page number: '. Reply only with a list containing these two elements and nothing else. Your output should look like ['extracted text', 1], where extracted text is the troubleshooting text and 1 is the page number."
            },
            {
                "role": "user",
                "content": pdf_string
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Response from OpenAI:", response.json())
        # print('\n')
        openai_response = (response.json()['choices'][0]['message']['content'])
    else:
        print("Error:", response.status_code, response.text)
    print(f'Open AI response: {openai_response}')
    openai_response = ast.literal_eval(openai_response)

    troubleshoot_text, troubleshoot_page = openai_response[0], openai_response[1]
    print(troubleshoot_text, troubleshoot_page)
    return jsonify({
        'troubleshoot_text':troubleshoot_text,
        'troubleshoot_page':troubleshoot_page
        })

if __name__ == '__main__':
    app.run(debug=True)
