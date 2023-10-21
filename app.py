import os
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

correct_phrases = {
    'எதுவும் ஒன்றாகும்': 'இதுவும் ஒன்றாகும்',
}
@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    text = request.form.get('text')
    for i, j in correct_phrases.items():
        text = text.replace(i, j)
    from spell import correct_spelling
    text = correct_spelling(text)
    # Do your grammar check logic here. For demonstration, let's just echo the text.
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'e.jpg', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
