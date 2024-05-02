# pdfreader

This application is able to:
- Load a pdf
- Convert each page of the pdf to png file
- Extract text from each png file
- Request ChatGPT to extract the text pertaining to troubleshooting and provide the page number in which it's found
- Response is provided in json format:
  ({
        'troubleshoot_text':troubleshoot_text,
        'troubleshoot_page':troubleshoot_page
        })

To run:
- Add your OpenAI API key to the .env file
- In the root directory:
- docker build -t my-flask-app .
- docker run -p 5001:5001 my-flask-app
- python send_pdf.py

   
The pdf to be scanned needs to be in the root directory and the filename needs to be updated in send_pdf.py variable - file_path
