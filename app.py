from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
import os

app = Flask(__name__)
CORS(app)

translate_client = translate.Client()

@app.route('/translate', methods=['POST'])
def translate_email():
    try:
        data = request.json
        html_content = data.get('html_content', '')
        target_lang = data.get('target_lang', 'es')

        soup = BeautifulSoup(html_content, 'html.parser')

        text_elements = [element for element in soup.find_all(string=True) if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', 'link']]

        for element in text_elements:
            stripped_text = element.strip()
            if stripped_text:
                translation = translate_client.translate(stripped_text, target_language=target_lang)
                element.replace_with(translation['translatedText'])

        translated_html = str(soup)
        
        return jsonify({
            'status': 'success',
            'translated_html': translated_html
        })
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
