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

#fungsi koneksi ke basis data
def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_perpus", user="root", passwd="",host="localhost",port=3306,autocommit=True)
    cursor = conn.cursor()	

#fungsi menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()


#fungsi view index() untuk menampilkan data dari basis data
users = {
    'user1': 'password1',
    'user2': 'password2'
}

books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling", "year": 1997, "stock":2},
    {"id": 2, "title": "Lord of the Rings", "author": "J.R.R. Tolkien", "year": 1954,"stock":2},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960,"stock":2}
]


def generate_id(cursor):
    while True:
        # Generate a random combination of letters and numbers with a length of 5 characters
        random_combination = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(5))
        cursor.execute('SELECT COUNT(*) FROM anggota WHERE id=%s', (random_combination,))
        count = cursor.fetchone()[0]
        if count == 0:
            return random_combination

@application.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        openDb()

        if email == "admin@gmail.com" and password == "admin123":
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


@application.route("/admin")
def admin():
    if "logged_in" in session and session["logged_in"]:
        return render_template("admin.html", email=session["email"], books=books)
    else:
        return redirect(url_for("index"))
    
@application.route("/user")
def user():
    if "logged_in" in session and session["logged_in"]:
        return render_template("user.html", email=session["email"], books=books)
    else:
        return redirect(url_for("login"))

@application.route("/buku")
def buku():
    return render_template("buku.html",books=books)


@application.route("/user/koleksi-saya")
def koleksi_saya():
    return render_template("/user/koleksi.html")

@application.route("/user/katalog-buku")
def katalog_buku():
    return render_template("/user/buku.html")

@application.route("/peminjaman")
def peminjaman():
    return render_template("data_peminjaman.html")

@application.route("/denda")
def denda():
    return render_template("data_denda.html")

@application.route('/tambah_buku', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        # Generate ID baru
        new_id = max([book['id'] for book in books]) + 1

        openDb()
        sql = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
        val = (title, author, year)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        # books.append({"id": new_id, "title": title, "author": author, "year": year})
        return redirect(url_for('buku'))
    return render_template('tambah_buku.html')

@application.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@application.route('/data_user')
def data_user():   
    openDb()
    container = []
    sql = "SELECT * FROM pegawai ORDER BY NIK DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('data_user.html', container=container,)

@application.route('/data_anggota')
def data_anggota():   
    openDb()
    container = []
    sql = "SELECT * FROM pegawai ORDER BY NIK DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('data_anggota.html', container=container,)



#fungsi membuat NIK otomatis
def generate_nik():
    # mendefinisikan fungsi openDb(), cursor, dan closeDb() 
    openDb()

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    
    # Mengambil empat digit terakhir dari tahun
    year_str = str(current_year).zfill(2)
    
    # Mengambil dua digit dari bulan
    current_month_str = str(current_month).zfill(2)

    # Membuat format NIK tanpa nomor urut terlebih dahulu
    base_nik_without_number = f"P-{year_str}{current_month_str}"

    # Mencari NIK terakhir dari database untuk mendapatkan nomor urut
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

#fungsi untuk menyimpan lokasi foto
UPLOAD_FOLDER = '/web_pegawai/crud/static/foto/'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#fungsi view tambah() untuk membuat form tambah data
@application.route('/tambah', methods=['GET','POST'])
def tambah():
    generated_nik = generate_nik()  # Memanggil fungsi untuk mendapatkan NIK otomatis

    if request.method == 'POST':
        fullname = request.form["fullname"]
        password = request.form["password"]
        email = request.form["email"]
        born = request.form["born"]
        phonenumber = request.form["phonenumber"]
        status = "Active"

        # # Pastikan direktori upload ada
        # if not os.path.exists(UPLOAD_FOLDER):
        #     os.makedirs(UPLOAD_FOLDER)

        # # Simpan foto dengan nama NIK
        # if 'foto' in request.files:
        #     foto = request.files['foto']
        #     if foto.filename != '':
        #         foto.save(os.path.join(application.config['UPLOAD_FOLDER'], f"{nik}.jpg"))

        openDb()
        id = generate_id(cursor)
        sql = "INSERT INTO anggota (fullname, password, email, born, phonenumber, status, id) VALUES (%s, %s,%s, %s, %s, %s,%s)"
        val = (fullname, password, email, born, phonenumber, status, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin'))      
    else:
        return render_template('tambah.html')  # Mengirimkan NIK otomatis ke template
    
#fungsi view edit() untuk form edit data
@application.route('/edit/<nik>', methods=['GET','POST'])
def edit(nik):
    openDb()
    cursor.execute('SELECT * FROM pegawai WHERE nik=%s', (nik))
    data = cursor.fetchone()
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        alamat = request.form['alamat']
        tgllahir = request.form['tgllahir']
        jeniskelamin = request.form['jeniskelamin']
        status = request.form['status']
        gaji = request.form['gaji']
        foto = request.form['nik']

        path_to_photo = os.path.join(application.root_path, '/web_pegawai/crud/static/foto', f'{nik}.jpg')
        if os.path.exists(path_to_photo):
            os.remove(path_to_photo)

        # Pastikan direktori upload ada
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Simpan foto dengan nama NIK
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.save(os.path.join(application.config['UPLOAD_FOLDER'], f"{nik}.jpg"))
        sql = "UPDATE pegawai SET nama=%s, alamat=%s, tgllahir=%s, jeniskelamin=%s, status=%s, gaji=%s, foto=%s WHERE nik=%s"
        val = (nama, alamat, tgllahir,jeniskelamin, status, gaji, foto, nik)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        closeDb()
        return render_template('edit.html', data=data)

#fungsi menghapus data
@application.route('/hapus/<nik>', methods=['GET','POST'])
def hapus(nik):
    openDb()
    cursor.execute('DELETE FROM pegawai WHERE nik=%s', (nik,))
    # Hapus foto berdasarkan NIK
    path_to_photo = os.path.join(application.root_path, '/web_pegawai/crud/static/foto', f'{nik}.jpg')
    if os.path.exists(path_to_photo):
        os.remove(path_to_photo)

    conn.commit()
    closeDb()
    return redirect(url_for('index'))

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
