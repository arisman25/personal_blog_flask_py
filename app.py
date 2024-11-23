from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Konfigurasi MySQL
app.secret_key = 'x_personal_blog_flash_python'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'x_personal_blog_flash_python'
mysql = MySQL(app)

# Contoh Konten
# konten = [
#     {
#         'judul' : "Posting pertama",
#         'sinopsis': "Ini adalah posting pertama",
#         'isi': "Ini adalah isi posting pertama",
#         'penulis': "Adi Arisman",
#         'tanggal': "Selasa, 28 November 2024",
#         'jam': "10:00 AM",
#         'selengkapnya': 'detail/1'
#     },
#     {
#         'judul' : "Posting kedua",
#         'sinopsis': "Ini adalah posting kedua",
#         'isi': "Ini adalah isi posting kedua",
#         'penulis': "Adi Arisman",
#         'tanggal': "Rabu, 29 November 2024",
#         'jam': "10:00 AM",
#         'selengkapnya': 'detail/2'
#     }
# ]
@app.route("/")
def home():
    #Creating a connection cursor
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM konten')
    konten = cursor.fetchall()
    return render_template("home.html", konten=konten)


@app.route("/tentang/")
def tentang():
    return render_template("tentang.html", title="Tentang")

@app.route("/login/", methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Buat koneksi ke database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s and is_aktif = 1', (username, password,))
        user = cursor.fetchone()
        if user:
            session['name'] = user['nama']
            session['username'] = user['username']
            session['email'] = user['email']
            message = "Berhasil Login"
            return redirect(url_for('home'))
        else:
            message = 'Username atau password salah'

    return render_template("login.html", title="Login", message=message)

@app.route("/daftar/", methods=['GET', 'POST'])
def daftar():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'nama' in request.form and 'email' in request.form and 'password' in request.form and 'konfirm_password' in request.form:
        nama = request.form['nama']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        konfirm_password = request.form['konfirm_password']
        if password == konfirm_password:
            # Buat koneksi ke database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('insert into users (nama, username, email, password, is_aktif) values (% s, % s, % s, % s, % s)', (nama, username, email, password,1))
            mysql.connection.commit()
            message = "Berhasil Daftar"
            return redirect(url_for('login'))  
        else:
            message = 'Password dan Konfirmasi Password tidak cocok'

    return render_template("daftar.html", title="Daftar", message=message)

@app.route("/logout/")
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)