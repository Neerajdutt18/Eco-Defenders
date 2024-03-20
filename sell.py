from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

sell = Flask(__name__, template_folder='template')
sell.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:9596@localhost/mydatabase'
sell.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER/'
sell.config['STATIC_FOLDER'] = 'static/'
sell.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
sell.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management
db = SQLAlchemy(sell)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in sell.config['ALLOWED_EXTENSIONS']

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

@sell.route('/')
def index():
    products = Product.query.all()
    for product in products:
        if product.photo_url:
            product.image_url = url_for('uploaded_file', filename=os.path.basename(product.photo_url))
        else:
            product.image_url = url_for('static', filename='default_product.jpg')
    return render_template('index.html', products=products)

@sell.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        seller_name = request.form['seller_name']
        contact_number = request.form['contact_number']
        address = request.form['address']
        photo = request.files['photo']

        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(sell.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            product = Product(name=name, description=description, price=price, photo_url=photo_path, seller_name=seller_name, contact_number=contact_number, address=address)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('add_product.html')

@sell.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(sell.config['UPLOAD_FOLDER'], filename)

@sell.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    sell.run(debug=True, port=5001)
