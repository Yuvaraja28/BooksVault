from datetime import datetime
import bcrypt, json, sqlite3, os, random, string
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

ADMINS = ['yuv.the.dev@gmail.com']

app = Flask(__name__)
# generate a random secret key for session management
SECRET = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
app.secret_key = SECRET

reviews = [
    {
        'name': 'Devakumar',
        'review': 'The customer service here is outstanding! They have a great collection of books for Pondicherry University arts, and the prices are very reasonable. Highly recommended!',
        'stars': 5,
        'image': 'pic-1.png'
    },
    {
        'name': 'Bob',
        'review': 'This is the best bookstore I have come across. They have almost every book you need, whether for exams or general reading, and the prices are very affordable.',
        'stars': 5,
        'image': 'pic-2.png'
    },
    {
        'name': 'Yuvaraja',
        'review': 'The staff here are very helpful and polite. They make sure to provide the books you need quickly. A great place for all your book needs!',
        'stars': 5,
        'image': 'pic-3.png'
    },
    {
        'name': 'Pooja',
        'review': 'This bookstore has an extensive collection of books. They even have all the arts study materials for every semester. The atmosphere is peaceful and welcoming.',
        'stars': 5,
        'image': 'pic-4.png'
    },
    {
        'name': 'Abhinav',
        'review': 'I switched to their online platform because it’s so convenient. They have a great selection of books, and I no longer have to worry about library closing times.',
        'stars': 5,
        'image': 'pic-5.png'
    }
]

# SQLite connection details
DATABASE = 'books.db'

def get_db():
    db = getattr(Flask(__name__), '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        Flask(__name__)._database = db
    return db

# Function to fetch book data from SQLite
def get_books_from_db():
    try:
        mydb = get_db()
        cursor = mydb.cursor()

        cursor.execute("SELECT id, title, image, price, original_price, description, bookStatus, rentalPrice FROM books")
        result = cursor.fetchall()

        books_data = []
        for row in result:
            books_data.append({
                'id': row[0],
                'title': row[1],
                'image': row[2],
                'price': row[3],
                'original_price': row[4],
                'description': row[5],
                'bookStatus': row[6],
                'rentalPrice': row[7]
            })

        cursor.close()
        mydb.close()
        return books_data
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return []


@app.route('/')
def index():
    # Fetch book data from the database
    books_data = get_books_from_db()
    books = {book['id']: book for book in books_data}
    return render_template('index.html', books=list(books.values()), reviews=reviews)

@app.route('/books/<string:category_id>')
def books(category_id):
    # Fetch book data from the database
    books_data = get_books_from_db()
    books = [x for x in books_data if x.get('bookStatus', 'new') == category_id]
    if book:
        return render_template('categories.html', category=category_id.capitalize(), books=books)
    else:
        return "Book not found"
    
@app.route('/book/<int:book_id>')
def book(book_id):
    # Fetch book data from the database
    books_data = get_books_from_db()
    books = {book['id']: book for book in books_data}
    book = books.get(book_id)
    if book:
        return render_template('book.html', book=book, rentalPrice=book.get('rentalPrice', 0), bookCondition=100 if book.get('bookStatus') == 'new' else random.randint(60, 90))
    else:
        return "Book not found"

def calculate_late_charges(rental_end_date, return_date, rental_price):
    # Calculate the number of days late
    late_days = (return_date - rental_end_date).days
    if late_days > 0:
        # Calculate the late charges (e.g., 10% of the rental price per day)
        late_charges = (rental_price * 0.10) * late_days
        return late_charges
    else:
        return 0

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        show_login_popup = True
    else:
        show_login_popup = False

    cart = session.get('cart', [])
    total = 0
    for item in cart:
        total += item['price'] * item['quantity']

    book_status = request.args.get('book_status', 'new')
    rental_end_date_str = request.args.get('return_date')

    late_charges = 0
    if book_status == 'rental' and rental_end_date_str:
        try:
            rental_end_date = datetime.strptime(rental_end_date_str, '%Y-%m-%d')
            return_date = datetime.now()  # Use current date as return date for calculation
            rental_price = 10  # Example rental price
            late_charges = calculate_late_charges(rental_end_date, return_date, rental_price)
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')

    return render_template('checkout.html', total=total, late_charges=late_charges, book_status=book_status, show_login_popup=show_login_popup)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'message': 'Authentication required'}), 401

    try:
        mydb = get_db()
        cursor = mydb.cursor()

        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchaseOrders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName VARCHAR(255),
                lastName VARCHAR(255),
                username VARCHAR(255),
                email VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255),
                state VARCHAR(255),
                pinCode VARCHAR(255),
                paymentMethod VARCHAR(255),
                book_status VARCHAR(255),
                cartItems TEXT
            )
        """)
        mydb.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentalOrders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName VARCHAR(255),
                lastName VARCHAR(255),
                username VARCHAR(255),
                email VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255),
                state VARCHAR(255),
                pinCode VARCHAR(255),
                paymentMethod VARCHAR(255),
                book_status VARCHAR(255),
                rental_start_date VARCHAR(255),
                rental_end_date VARCHAR(255),
                cartItems TEXT
            )
        """)
        mydb.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        mydb.commit()

        data = request.get_json()
        firstName = data['firstName']
        lastName = data['lastName']
        username = data['username']
        email = data['email']
        address = data['address']
        city = data['city']
        state = data['state']
        pinCode = data['pinCode']
        paymentMethod = data['paymentMethod']
        cartItems = data['cartItems']

        # Parse cart items
        cart = json.loads(cartItems)

        for item in cart:
            book_status = item.get('book_status', 'new')

            if book_status == 'rental':
                # Insert order into rentalOrders table
                rental_start_date = item.get('rental_start_date', None)
                rental_end_date = item.get('rental_end_date', None)
                sql = "INSERT INTO rentalOrders (firstName, lastName, username, email, address, city, state, pinCode, paymentMethod, cartItems, book_status, rental_start_date, rental_end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val = (firstName, lastName, username, email, address, city, state, pinCode, paymentMethod, json.dumps(item), book_status, rental_start_date, rental_end_date)
            else:
                # Insert order into purchaseOrders table
                sql = "INSERT INTO purchaseOrders (firstName, lastName, username, email, address, city, state, pinCode, paymentMethod, cartItems, book_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val = (firstName, lastName, username, email, address, city, state, pinCode, paymentMethod, json.dumps(item), book_status)
            
            cursor.execute(sql, val)
            mydb.commit()

        return jsonify({'message': 'Order placed successfully!'}), 200

    except Exception as e:
        print(f"Error placing order: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/auth', methods=['POST'])
def auth():
    mydb = get_db()
    cursor = mydb.cursor()

    # Create the users table if it doesn't exist
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        mydb.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
        flash(f"Error creating table: {e}", 'error')
        return redirect(url_for('index'))
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

    if request.form.get('action') == 'register':
        # Registration logic
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            mydb = get_db()
            cursor = mydb.cursor()

            # Insert the user into the database
            sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
            val = (username, hashed_password, email)
            cursor.execute(sql, val)
            mydb.commit()

            cursor.close()
            mydb.close()

            session['username'] = username
            session['email'] = email
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Error registering user: {e}")
            flash(f"Error registering user: {e}", 'error')
            return redirect(url_for('index'))

    elif request.form.get('action') == 'login':
        # Login logic
        username = request.form['username']
        password = request.form['password']

        try:
            mydb = get_db()
            cursor = mydb.cursor()

            # Retrieve the user from the database
            sql = "SELECT id, username, password, email FROM users WHERE username = ? OR email = ?"
            val = (username, username)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            cursor.close()
            mydb.close()

            if result:
                user_id, username_db, hashed_password, user_email = result
                # Verify the password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['user_id'] = user_id
                    session['username'] = username_db
                    session['email'] = user_email
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    return jsonify({ "error": "Invalid Password" }), 400
            else:
                return redirect(url_for('index'))

        except Exception as e:
            print(f"Error logging in user: {e}")
            return redirect(url_for('index'))
    else:
        flash('Invalid request', 'error')
        return redirect(url_for('index'))

# Admin dashboard route
@app.route('/admin')
def admin():
    if 'user_id' not in session or session['email'] not in ADMINS:
        return redirect(url_for('index'))

    try:
        mydb = get_db()
        cursor = mydb.cursor()

        # Fetch data from rentalOrders table
        cursor.execute("SELECT * FROM rentalOrders")
        rental_orders_result = cursor.fetchall()

        rental_orders = []
        for row in rental_orders_result:
            rental_orders.append({
                'id': row[0],
                'firstName': row[1],
                'lastName': row[2],
                'username': row[3],
                'email': row[4],
                'address': row[5],
                'city': row[6],
                'state': row[7],
                'pinCode': row[8],
                'paymentMethod': row[9],
                'book_status': row[10],
                'rental_start_date': row[11],
                'rental_end_date': row[12],
                'cartItems': json.loads(row[13]) if row[13] else {}
            })

        # Fetch data from purchaseOrders table
        cursor.execute("SELECT * FROM purchaseOrders")
        purchase_orders_result = cursor.fetchall()

        purchase_orders = []
        for row in purchase_orders_result:
            purchase_orders.append({
                'id': row[0],
                'firstName': row[1],
                'lastName': row[2],
                'username': row[3],
                'email': row[4],
                'address': row[5],
                'city': row[6],
                'state': row[7],
                'pinCode': row[8],
                'paymentMethod': row[9],
                'book_status': row[10],
                'cartItems': json.loads(row[11]) if row[11] else {}
            })

        cursor.close()
        mydb.close()

        return render_template('admin.html', rental_orders=rental_orders, purchase_orders=purchase_orders)

    except Exception as e:
        print(f"Error fetching orders: {e}")
        return f"Error fetching orders: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT') or 5000, debug=True)
