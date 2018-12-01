from flask import Flask, render_template, request
import csv
import json

app = Flask(__name__)
filename = 'results.csv'

@app.route('/')
def main_page():
    age = resuest.form['age']
    if age = 'nope':
        return render_template('thanks.html')
    return render_template('index.html')

@app.route('/questions')
def questionnaire():
    return render_template('questions.html')

@app.route('/thanks', methods=['POST'])
def save_to_csv():
    if request.method == 'POST':
        hren = request.form['hren']
        her = request.form['her']
        hui = request.form['hui']
        bly = request.form['bly']
        suka = request.form['suka']
        gender = request.form['gender']
        fieldnames = ['hren', 'her', 'hui', 'bly', 'suka', 'gender']
        with open(filename, 'a+', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'hren': hren, 'her': her, 'hui': hui,
                             'bly': bly, 'suka': suka, 'gender': gender})
        return render_template('thanks.html', fin_form=fin_form)

@app.route('/stats')
def show_stats():
    with open(filename, 'r', encoding='utf-8') as content:
        content = csv.reader(content)
        return render_template('stats.html', content=content)

@app.route('/json')
def json_maker():
    dict_csv = {}
    fieldnames = ['hren', 'her', 'hui', 'bly', 'suka', 'gender']
    with open(filename, 'r+', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            gender = row['gender']
            dict_csv[gender] = json.loads(json.dumps(row))
    return render_template('json.html', json=dict_csv)


if __name__ == '__main__':
    app.run(debug=True)
    
    
