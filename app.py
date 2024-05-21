from flask import Flask, render_template, request, redirect, session, url_for
import pymysql.cursors, os
import datetime
from flask import jsonify
import uuid
import secrets
import string

application = Flask(__name__)

conn = cursor = None

application.secret_key = "your_secret_key_here"

def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perpus", user="root", passwd="",host="localhost",port=3306,autocommit=True)
    cursor = conn.cursor()	

def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# books = [
#     {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling", "year": 1997, "stock":2},
#     {"id": 2, "title": "Lord of the Rings", "author": "J.R.R. Tolkien", "year": 1954,"stock":2},
#     {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960,"stock":2}
# ]

def generate_random_id(length):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

@application.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        openDb()

        if email == "admin@gmail.com" and password == "admin":
            session["logged_in"] = True
            session["email"] = email
            return redirect(url_for("admin"))
        
        cursor.execute('SELECT * FROM anggota WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = user[0] 
            session['email'] = user[1]    
            return redirect(url_for('user'))
        else:
            closeDb() 
            return render_template("index.html", message="Invalid username or password.")
    return render_template("index.html")

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        password = request.form["password"]
        email = request.form["email"]
        born = request.form["born"]
        phonenumber = request.form["phonenumber"]
        status = "Active"

        openDb()
        id = generate_id(cursor)
        sql = "INSERT INTO anggota (fullname, password, email, born, phonenumber, status, id) VALUES (%s, %s,%s, %s, %s, %s,%s)"
        val = (fullname, password, email, born, phonenumber, status, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('user'))
    return render_template("register.html")

def fetch_anggota():
    openDb()
    container = []
    sql = "SELECT * FROM anggota;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return container

def fetch_buku():
    openDb()
    books = []
    sql = "SELECT * FROM buku;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        books.append(data)
    closeDb()
    return books

def fetch_transaksi():
    openDb()
    all_transaksi = []
    sql = "SELECT * FROM transaksi;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        all_transaksi.append(data)
    closeDb()
    return all_transaksi

@application.route("/admin")
def admin():
    container = fetch_anggota()
    books = fetch_buku()
    transaksi =fetch_transaksi()
    if "logged_in" in session and session["logged_in"]:
        return render_template("admin.html", email=session["email"], container=container, books=books, transaksi=transaksi)
    else:
        return redirect(url_for("index"))
    
@application.route("/user")
def user():
    if "logged_in" in session and session["logged_in"]:
        return render_template("user.html", email=session["email"], books=books)
    else:
        return redirect(url_for("login"))

@application.route("/denda")
def denda():
    return render_template("data_denda.html")

@application.route('/tambah_buku', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        stok = request.form['stok']

        status = "Tersedia"  
        new_id = generate_random_id

        openDb()
        sql = "INSERT INTO buku (id, judul, penulis, tahun, status, stok) VALUES (%s,%s, %s, %s, %s, %s)"
        val = (new_id,title, author, year, status, stok)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin'))
    return render_template('tambah_buku.html')

@application.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))

#fungsi membuat NIK otomatis
def generate_nik():
    # mendefinisikan fungsi openDb(), cursor, dan closeDb() 
    openDb()

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    
    year_str = str(current_year).zfill(2)
    
    current_month_str = str(current_month).zfill(2)

    base_nik_without_number = f"P-{year_str}{current_month_str}"

    cursor.execute("SELECT nik FROM pegawai WHERE nik LIKE %s ORDER BY nik DESC LIMIT 1", (f"{base_nik_without_number}%",))
    last_nik = cursor.fetchone()

    if last_nik:
        last_number = int(last_nik[0].split("-")[-1])  # Mengambil nomor urut terakhir
        next_number = last_number + 1
        # Membuat NIK lengkap dengan nomor urut
        next_nik = f"P-{str(next_number).zfill(3)}"
    else:
        next_number = 1  # Jika belum ada data, mulai dari 1
        # Membuat NIK lengkap dengan nomor urut
        next_nik = f"{base_nik_without_number}{str(next_number).zfill(3)}"
    
    closeDb()  # untuk menutup koneksi database 
    
    return next_nik


@application.route('/edit_buku/<int:id>', methods=['GET', 'POST'])
def edit_buku(id):
    if request.method == 'POST':
        # Retrieve form data
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        status = request.form['status']
        stok = request.form['stok']
        
        openDb()
    
        sql = "UPDATE buku SET judul = %s, penulis = %s, tahun = %s, status = %s, stok = %s WHERE id = %s"
        val = (judul, penulis, tahun, status, stok, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin'))
    openDb()
    sql = "SELECT * FROM buku WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    closeDb()
    return render_template('edit_buku.html', book=book)

@application.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        # Retrieve form data
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        born = request.form['born']
        phonenumber = request.form['phonenumber']
        status = request.form['status']
        
        openDb()
        
        # Update the user record in the database
        sql = "UPDATE anggota SET fullname = %s, email = %s, password = %s, born = %s, phonenumber = %s, status = %s WHERE id = %s"
        val = (fullname, email, password, born, phonenumber, status, id)
        cursor.execute(sql, val)
        conn.commit()
        
        closeDb()
        
        # Redirect to the admin page after updating
        return redirect(url_for('admin'))
    
    # If it's a GET request, retrieve the user details based on the provided ID
    openDb()
    sql = "SELECT * FROM anggota WHERE id = %s"
    cursor.execute(sql, (id,))
    user = cursor.fetchone()
    closeDb()
    
    # Render the edit user form with the user details
    return render_template('edit.html', user=user)


@application.route('/delete_buku/<int:id>', methods=['GET','POST'])
def delete_buku(id):
    openDb()
    sql = "DELETE FROM buku WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('admin'))

@application.route('/hapus/<int:id>', methods=['GET','POST'])
def hapus(id):
    openDb()
    sql = "DELETE FROM anggota WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('admin'))

#fungsi cetak ke PDF
@application.route('/get_employee_data/<nik>', methods=['GET'])
def get_employee_data(nik):
    # Koneksi ke database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',  # Password Anda (jika ada)
                                 db='db_perpus',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Query untuk mengambil data pegawai berdasarkan NIK
            sql = "SELECT * FROM pegawai WHERE nik = %s"
            cursor.execute(sql, (nik,))
            employee_data = cursor.fetchone()  # Mengambil satu baris data pegawai

            # Log untuk melihat apakah permintaan diterima dengan benar
            print("Menerima permintaan untuk NIK:", nik)

            # Log untuk melihat data yang dikirim ke klien
            print("Data yang dikirim:", employee_data)

            return jsonify(employee_data)  # Mengembalikan data sebagai JSON

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Terjadi kesalahan saat mengambil data'}), 500

    finally:
        connection.close()  # Menutup koneksi database setelah selesai

#Program utama      
if __name__ == '__main__':
    application.run(debug=True)
