# %%
from flask import Flask, render_template, request, redirect, url_for
import csv

# %%
app = Flask(__name__)

# %%
# Caminho para o arquivo CSV
csv_file_path = 'volumes.csv'

# Função para carregar os dados do CSV
def load_data():
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return data

# %%
# Função para salvar os dados no CSV
def save_data(data):
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['volume', 'titulo', 'author', 'status']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        csv_writer.writeheader()
        csv_writer.writerows(data)


# %%
# Rotas
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    data = load_data()
    new_entry = {
        'volume': request.form['volume'],
        'titulo': request.form['titulo'],
        'author': request.form['author'],
        'status': request.form['status'],
    }
    data.append(new_entry)
    save_data(data)
    return redirect(url_for('index'))

@app.route('/update/<int:row_id>', methods=['GET', 'POST'])
def update(row_id):
    data = load_data()
    if request.method == 'POST':
        updated_entry = {
            'volume': request.form['volume'],
            'titulo': request.form['titulo'],
            'author': request.form['author'],
            'status': request.form['status'],
        }
        data[row_id] = updated_entry
        save_data(data)
        return redirect(url_for('index'))
    else:
        entry = data[row_id]
        return render_template('update.html', row_id=row_id, entry=entry)

@app.route('/delete/<int:row_id>')
def delete(row_id):
    data = load_data()
    del data[row_id]
    save_data(data)
    return redirect(url_for('index'))

# %%
if __name__ == '__main__':
    app.run(debug=True)


