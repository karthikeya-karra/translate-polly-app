from flask import Flask, render_template, request, send_file
import boto3
import os

app = Flask(__name__)

translate = boto3.client('translate')
polly = boto3.client('polly')

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = None
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['language']

        # Translate text
        result = translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_lang)
        translated_text = result['TranslatedText']

        # Synthesize speech
        response = polly.synthesize_speech(Text=translated_text, OutputFormat='mp3', VoiceId='Joanna')

        # Save audio
        with open('static/audio.mp3', 'wb') as f:
            f.write(response['AudioStream'].read())

    return render_template('index.html', translated_text=translated_text)

@app.route('/audio')
def audio():
    return send_file('static/audio.mp3')

if __name__ == '__main__':
    app.run(debug=True)
