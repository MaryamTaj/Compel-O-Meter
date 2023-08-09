from flask import Flask, render_template, request
import analysis
import spacy
import nltkmodules

spacy.load('en_core_web_sm')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/launch')
def launch():
    return render_template('launch.html')


@app.route('/load', methods=['POST'])
def load():
    return render_template ('load.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    text = request.form['text']
    result = analysis.get_compellingness_ai(text)
    descriptions = analysis.get_compellingness_description(result)
    warnings = analysis.ethics_warning(text)
    pathos = analysis.get_pathos_description(result)
    logos = analysis.get_logos_description(result)
    return render_template('results.html', text=text, result=result, descriptions=descriptions, warnings=warnings, pathos=pathos, logos=logos)


if __name__ == '__main__':
    app.run()
