from flask import Flask, render_template, request, redirect, session, url_for
import pymysql.cursors, os
import datetime
from flask import jsonify
from datetime import datetime


application = Flask(__name__)

conn = cursor = None

application.secret_key = "your_secret_key_here"

def openDb():
    global conn, cursor
    conn = pymysql.connect(db="db_restoran", user="root", passwd="",host="localhost",port=3306,autocommit=True)
    cursor = conn.cursor()	

def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# BUAT LOGIN 
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
##

# LOGOUT
@application.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))
##

# GET DATA
def fetch_orders():
    openDb()
    arr_orders = []
    sql = "SELECT * FROM orders;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        arr_orders.append(data)
    closeDb()
    return arr_orders


def fetch_orders_detail(orderid):
    openDb()
    detail=[]
    sql = "SELECT orderitems.ItemName, orderitems.Quantity, orderitems.Price, (orderitems.Quantity * orderitems.Price) AS total_item FROM orderitems JOIN orders ON orderitems.OrderID = orders.OrderID WHERE orderitems.OrderID = %s"
    cursor.execute(sql,(orderid,))
    results = cursor.fetchall()
    for data in results:
        detail.append(data)
    closeDb()
    return detail

def fetch_menu():
    openDb()
    arr_menu = []
    sql = "SELECT * FROM menuitems;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        arr_menu.append(data)
    closeDb()
    return arr_menu



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
##

# TAMPILIN HALAMAN ADMIN & USER
@application.route("/admin")
def admin():
    current_date = datetime.now().strftime('%Y-%m-%d')
    # container = fetch_anggota()
    books = fetch_buku()
    transaksi =fetch_transaksi()
    if "logged_in" in session and session["logged_in"]:
        return render_template("admin.html", email=session["email"], container=container, books=books, transaksi=transaksi, current_date=current_date)
    else:
        return redirect(url_for("login"))
    
@application.route("/user")
def user():
    if "logged_in" in session and session["logged_in"]:
        return render_template("user.html", email=session["email"], books=books)
    else:
        return redirect(url_for("login"))
##

# HALAMAN LAIN-LAIN
@application.route("/admin-new")
def admin_new():
    orders = fetch_orders()
    menu = fetch_menu()
    return render_template("admin-new.html", data_orders=orders, data_menu=menu)

@application.route("/detail_order/<int:id>")
def detail_order(id):
    detail = fetch_orders_detail(id)  
    return render_template("detail_order.html", data_detail=detail, id=id)


@application.route("/menulist")
def menulist():
    return render_template("menulist.html")

@application.route("/orderlist")
def orderlist():
    return render_template("orderlist.html")
##

# ADD
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

@application.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
   if request.method == 'POST':
        img_url = request.form['img_url']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        status = "Available"

        openDb()
        sql = "INSERT INTO menuitems (img_url, name, description, price, category, status) VALUES (%s,%s,%s, %s, %s,%s)"
        val = (img_url, name,description,price,category, status)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin_new')+ '#menu')
   return render_template('add_menu.html')

##
##


# EDIT 
@application.route('/edit_menu/<int:id>', methods=['GET', 'POST'])
def edit_menu(id):
    if request.method == 'POST':
        img_url = request.form['img_url']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        
        openDb()
    
        sql = "UPDATE menuitems SET img_url = %s,name = %s, description = %s, price = %s, category = %s WHERE MenuItemID = %s"
        val = (img_url, name, description, price, category, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin_new')+ '#menu')
    openDb()
    sql = "SELECT * FROM menuitems WHERE MenuItemID = %s"
    cursor.execute(sql, (id,))
    menu = cursor.fetchone()
    closeDb()
    return render_template('edit_menu.html', menu=menu)

@application.route('/accept/<int:id>', methods=['POST'])
def accept(id):
    if request.method == 'POST':
        status = 'Accept'
        
        openDb()
        sql = "UPDATE orders SET status = %s WHERE OrderID = %s"
        val = (status, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
    return redirect(url_for('admin_new') + "#orders")

@application.route('/reject/<int:id>', methods=['POST'])
def reject(id):
    if request.method == 'POST':
        status = 'Reject'
        
        openDb()
        sql = "UPDATE orders SET status = %s WHERE OrderID = %s"
        val = (status, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
    return redirect(url_for('admin_new') + "#orders")
  

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
##

# DELETE
@application.route('/delete_menu/<int:id>', methods=['GET','POST'])
def delete_menu(id):
    openDb()
    sql = "DELETE FROM menuitems WHERE MenuItemID = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('admin_new'))

##

# PRINT 
@application.route('/get_employee_data/<int:id>', methods=['GET'])
def get_employee_data(id):
    # Koneksi ke database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',  # Password Anda (jika ada)
                                 db='db_restoran',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Query untuk mengambil data pegawai berdasarkan NIK
            sql = "SELECT * FROM anggota WHERE id = %s"
            cursor.execute(sql, (id,))
            employee_data = cursor.fetchone()  # Mengambil satu baris data pegawai

            # Log untuk melihat apakah permintaan diterima dengan benar
            print("Menerima permintaan untuk NIK:", id)

            # Log untuk melihat data yang dikirim ke klien
            print("Data yang dikirim:", employee_data)

            return jsonify(employee_data)  # Mengembalikan data sebagai JSON

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Terjadi kesalahan saat mengambil data'}), 500

    finally:
        connection.close()  # Menutup koneksi database setelah selesai
##

# MAIN PROGRAM      
if __name__ == '__main__':
    application.run(debug=True)
