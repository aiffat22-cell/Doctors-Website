from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/makeanappointment'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    payment_code = db.Column(db.String(100))
    location = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('shop.html', customers=customers)

@app.route('/all_customers')
def all():
    customers = Customer.query.all()
    return render_template('sub.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        product = request.form['product']
        payment_code = request.form.get('payment_code')
        location = request.form.get('location')

        new_customer = Customer(name=name, last_name=last_name, phone=phone, product=product, payment_code=payment_code, location=location)

        try:
            db.session.add(new_customer)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an issue adding the customer: {e}"

@app.route('/cust/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.last_name = request.form['last_name']
        customer.phone = request.form['phone']
        customer.product = request.form['product']
        customer.payment_code = request.form['payment_code']
        customer.location = request.form['location']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the customer"

    return render_template('edit.html', customer=customer)

@app.route('/cust/delete/<int:id>')
def delete(id):
    customer = Customer.query.get_or_404(id)

    try:
        db.session.delete(customer)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the customer"

if __name__ == "__main__":
    app.run(debug=True)