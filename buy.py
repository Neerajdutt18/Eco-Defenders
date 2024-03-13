from flask import Flask, render_template, send_from_directory, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:9596@localhost/mydatabase'
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER/'
app.config['STATIC_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management
db = SQLAlchemy(app)

# Define your Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)
    photo_url = db.Column(db.String(255))
    image_url = db.Column(db.String(255), default='default_product.jpg')
    seller_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)


# Route to display products
@app.route('/')
def index():
    products = Product.query.all()
    for product in products:
        if product.photo_url:
            product.image_url = url_for('uploaded_file', filename=os.path.basename(product.photo_url))
        else:
            product.image_url = url_for('static', filename='default_product.jpg')
    return render_template('buyindex.html', products=products)

# Route to display product details
# Route to display product details
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if product:
        if product.photo_url:
            product.image_url = url_for('uploaded_file', filename=os.path.basename(product.photo_url))
        else:
            product.image_url = url_for('static', filename='default_product.jpg')
        
        # Pass the product and an empty item to the template
        return render_template('product_details.html', product=product, item={})
    else:
        return "Product not found"


# Route to handle adding product to cart and redirect to address and payment section
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Initialize cart in session if not already present
    session.setdefault('cart', {})
    # Add product to cart or increment quantity if already present
    session['cart'][product_id] = session['cart'].get(product_id, 0) + 1
    # Redirect to the address and payment section
    return redirect(url_for('address_and_payment'))

# Route to display address and payment section
@app.route('/address_and_payment')
def address_and_payment():
    # Render the template for address and payment section
    return render_template('address_and_payment.html', cart=session.get('cart', {}))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
