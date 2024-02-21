# %%
from flask import Flask, render_template, request, redirect, url_for
import csv

# %%
app = Flask(__name__)

# %%
# Caminho para o arquivo CSV
csv_volumes = 'volumes.csv'
csv_colecoes = 'colecoes.csv'

# Função para carregar os dados do CSV
def load_data_volumes():
    with open(csv_volumes, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return data

def load_data_colecao():
    with open(csv_colecoes, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return data

# %%
# Função para salvar os dados no CSV
def save_data(data):
    with open(csv_volumes, 'w', newline='') as csv_file:
        fieldnames = ['volume', 'titulo', 'author', 'status']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        csv_writer.writeheader()
        csv_writer.writerows(data)


# %%
# Rotas
@app.route('/')
def index(): 
    volumes_data = load_data_volumes()
    colecoes_data = load_data_colecao()
    return render_template('index.html', volumes_data=volumes_data, colecoes_data=colecoes_data)

@app.route('/add', methods=['POST'])
def add():
    data = load_data_volumes()
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
    data = load_data_volumes()
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
    data = load_data_volumes()
    del data[row_id]
    save_data(data)
    return redirect(url_for('index'))

# %%
if __name__ == '__main__':
    app.run(debug=True)


