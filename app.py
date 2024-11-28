from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'wayan',  
    'password': 'wayan20',  
    'host': 'localhost',
    'database': 'database_name' 
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM keuntungan')
    keuntungan = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', keuntungan=keuntungan)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO keuntungan (nama, jumlah) VALUES (%s, %s)', (nama, jumlah))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        cursor.execute('UPDATE keuntungan SET nama = %s, jumlah = %s WHERE id = %s', (nama, jumlah, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM keuntungan WHERE id = %s', (id,))
    keuntungan = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', keuntungan=keuntungan)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM keuntungan WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)