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

# BUAT REGISTER
@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]

        openDb()
        sql = "INSERT INTO customers (name, password, email) VALUES (%s, %s,%s)"
        val = (name, password, email)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('user'))
    return render_template("register.html")

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
        
        cursor.execute('SELECT * FROM customers WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = user[0] 
            session['email'] = user[1]    
            return redirect(url_for('user'))
        else:
            closeDb() 
            return render_template("login.html", message="Invalid username or password.")
    return render_template("login.html")
##

# LOGOUT
@application.route("/signout")
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

def fetch_orders_user(id):
    openDb()
    arr_orders = []
    sql = "SELECT * FROM orders WHERE customerid = '%s';"
    cursor.execute(sql,(id,))
    results = cursor.fetchall()
    for data in results:
        arr_orders.append(data)
    closeDb()
    return arr_orders

def fetch_orders_recent():
    openDb()
    arr_orders = []
    sql = "SELECT * FROM orders ORDER BY OrderDate DESC LIMIT 5;"
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

def count_order_amount(orderid):
    openDb()
    sql= "SELECT SUM(orderitems.Quantity * orderitems.Price) AS total_order FROM orderitems WHERE orderitems.OrderID = %s"
    cursor.execute(sql,(orderid,))
    count = cursor.fetchone()[0]      
    closeDb()
    return count

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

def count_menu():
    openDb()
    sql = "SELECT COUNT(*) FROM menuitems;"
    cursor.execute(sql)
    count = cursor.fetchone()[0]      
    closeDb()
    return count

def count_orders():
    openDb()
    sql = "SELECT COUNT(*) FROM orders;"
    cursor.execute(sql)
    count = cursor.fetchone()[0]      
    closeDb()
    return count

def count_active_orders():
    openDb()
    sql = "SELECT COUNT(*) FROM `orders` WHERE Status = 'Accept'"
    cursor.execute(sql)
    count = cursor.fetchone()[0]      
    closeDb()
    return count

def count_total_income():
    openDb()
    sql = "SELECT SUM(Amount) FROM `orders` WHERE Status = 'Accept'"
    cursor.execute(sql)
    count = cursor.fetchone()[0]      
    closeDb()
    if count is not None:
        count = int(count)
    else:
        count = 0
    return count
    
##


# TAMPILIN HALAMAN ADMIN & USER    
    
@application.route("/homepage")
def homepage():
    menu = fetch_menu()
    return render_template("homepage.html",data_menu=menu)

@application.route("/user")
def user():
    menu = fetch_menu()
    id = session["logged_in"]
    order=fetch_orders_user(id)
    if "logged_in" in session and session["logged_in"]:
        return render_template("user.html", email=session["email"], data_menu=menu, idcustomer=id,
                               data_order=order)
    else:
        return redirect(url_for("login"))

@application.route("/admin")
def admin():
    orders = fetch_orders()
    menu = fetch_menu()
    recent = fetch_orders_recent()
    all_menu = count_menu()
    all_orders = count_orders()
    all_active = count_active_orders()
    all_income = count_total_income()
    if "logged_in" in session and session["logged_in"]:
       return render_template("admin.html", data_orders=orders, data_menu=menu, count_menu=all_menu, count_orders = all_orders,
    count_active=all_active, count_income=all_income, email=session["email"])
    else:
        return redirect(url_for("login"))
        

@application.route("/detail_order/<int:id>")
def detail_order(id):
    detail = fetch_orders_detail(id)  
    total = count_order_amount(id)
    email = session['email']
    return render_template("detail_order.html", data_detail=detail, id=id,  total_order=total, role=email)

##

# ADD
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
        return redirect(url_for('admin')+ '#menu')
   return render_template('add_menu.html')

@application.route('/create_order/<int:id>', methods=['GET','POST'])
def add_item(id):
   if request.method == 'POST':
        customerName = request.form['customerName']
        Location = request.form['location']
        status = ""
        Amount = 0
        customerid = id
        current_date = datetime.now().strftime("%Y-%m-%d")

        openDb()
        sql = "INSERT INTO orders (orderDate, customerName,Location,status,Amount,customerid) VALUES (%s,%s,%s,%s, %s,%s)"
        val = (current_date,customerName,Location,status,Amount,customerid)
        cursor.execute(sql, val)
        conn.commit()
        closeDb() 
        return redirect(url_for('select_menu',id=id))
   return render_template('create_order.html',name=session['email'] )

@application.route('/select_menu/<int:id>', methods=['GET','POST'])
def select_menu(id):
   return render_template('select_menu.html',data_menu=fetch_menu(), name=session['email'])

@application.route('/submit_cart', methods=['POST'])
def submit_cart():
    data = request.json
    cart = data['cart']
    customer = data['customer']
    
    customer_name = customer['name']
    location = customer['location']
    status = "Pending"
    amount = sum(item['price'] * item['quantity'] for item in cart)
    customer_id = session['logged_in']

    try:
        openDb()
    
        order_sql = """
            INSERT INTO orders (OrderDate, CustomerName, Location, Status, Amount, CustomerID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_values = (order_date, customer_name, location, status, amount, customer_id)
        cursor.execute(order_sql, order_values)
        
        orderID = cursor.lastrowid
        
        for item in cart:
            item_sql = """
                INSERT INTO orderitems (OrderID, ItemName, Price, Quantity, Total)
                VALUES (%s, %s, %s, %s, %s)
            """
            item_values = (orderID, item['name'], item['price'], item['quantity'], item['quantity'] * item['price'])
            cursor.execute(item_sql, item_values)
        
        conn.commit()
        closeDb()
        return jsonify({'success': True, 'redirect': url_for('user') + '#orders'})
    except Exception as e:
        print(f"Error placing order: {e}")
        closeDb()
        return jsonify({'success': False, 'error': str(e)})

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
        status = request.form['status']
        
        openDb()
    
        sql = "UPDATE menuitems SET img_url = %s,name = %s, description = %s, price = %s, category = %s , status = %s WHERE MenuItemID = %s"
        val = (img_url, name, description, price, category,status, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('admin')+ '#menu')
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
    return redirect(url_for('admin') + "#orders")

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
    return redirect(url_for('admin') + "#orders")

##

# DELETE
@application.route('/delete_menu/<int:id>', methods=['GET','POST'])
def delete_menu(id):
    openDb()
    sql = "DELETE FROM menuitems WHERE MenuItemID = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('admin'))

@application.route('/cancel/<int:id>', methods=['GET','POST'])
def cancel(id):
    openDb()
    sql = "DELETE FROM orderitems WHERE OrderID = %s"
    cursor.execute(sql, (id,))

    sql = "DELETE FROM orders WHERE OrderID = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('user'))
##

# PRINT 
@application.route('/print_order/<int:id>', methods=['GET'])
def print_order(id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='', 
                                 db='db_restoran',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)                  

    try:
        with connection.cursor() as cursor:
            sql_detail_order = """
            SELECT 
                ItemName, 
                Quantity, 
                Price, 
                (Quantity * Price) AS total_item
            FROM 
                orderitems 
                JOIN orders ON orderitems.OrderID = orders.OrderID 
            WHERE 
                orderitems.OrderID = %s
            """

            sql_total_order = """
            SELECT 
                SUM(Quantity * Price) AS total_order
            FROM 
                orderitems 
            WHERE 
                OrderID = %s
            """

            cursor.execute(sql_detail_order, (id,))
            detail_order = cursor.fetchall()

            cursor.execute(sql_total_order, (id,))
            total_order = cursor.fetchone()['total_order']

            print("Menerima permintaan untuk NIK:", id)
            print("Detail Order:", detail_order)
            print("Total Order:", total_order)

            # Combine detail_order and total_order into a single dictionary
            combined_result = {
                "detail_order": detail_order,
                "total_order": total_order
            }

            return jsonify(combined_result)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Terjadi kesalahan saat mengambil data'}), 500

    finally:
        connection.close() 

##

# MAIN PROGRAM      
if __name__ == '__main__':
    application.run(debug=True)
