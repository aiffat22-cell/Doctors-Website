from flask import Flask, render_template, jsonify,request, send_from_directory, flash, redirect, url_for , session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from datetime import datetime
import smtplib
import random
import string
from flask_cors import CORS
from sqlalchemy.orm.exc import NoResultFound

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from sqlalchemy.exc import IntegrityError
import base64
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/makeanappointment'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
login_manager = LoginManager(app)




#-----------------------------------------------------------------------------------------------------

# Define User model
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    phone_number = db.Column(db.String(500), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50), nullable=True, default='user')
    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth.isoformat(),
            'address': self.address,
            'role': self.role
        }


    #to chek if user is admin 
def is_admin(self):
        return self.role == 'admin'

# Define Patients model
class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    visitday = db.Column(db.Date)
    status = db.Column(db.String(10))

def send_email(sender_email, receiver_email, subject, message):
    email = MIMEMultipart()
    email.attach(MIMEText(message, 'plain'))
    email["Subject"] = subject
    email["From"] = sender_email
    email["To"] = receiver_email
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    app_password = "fggx tcka vcyd wcee" 
    server.login(sender_email, app_password)
    server.send_message(email)
    server.quit()

@app.route('/')
def index1():
    return render_template('index.html')
@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('image', filename) 

@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    name = request.form['doctor']
    email = request.form['email']
    phone = request.form['phone']
    status = request.form['patient_status']
    visit_date = request.form['visit_date']
    visit_date = datetime.strptime(visit_date, '%Y-%m-%d').date()
    

    new_patient = Patients(name=name, email=email, phone=phone, visitday=visit_date, status=status)
    db.session.add(new_patient)
    db.session.commit()
    sender_email = "haydariifatimaa@gmail.com"  
    receiver_email = email
    subject = "Appointment Confirmation"
    message = f"Dear patient,\n\nYour appointment has been scheduled for {visit_date}. We look forward to seeing you.\n\nBest regards,\nYour Clinic"
    send_email(sender_email, receiver_email, subject, message)
    
    appointments = Patients.query.filter_by(email=email).all()
    
    return render_template('datatablemake.html', Patients=appointments)


# Other routes follow the same pattern
@app.route('/submissions.html')
def sub():
    return render_template('submissions.html')
@app.route('/index.html')
def index():
    return render_template('index.html')
@app.route('/About.html')
def About():
    return render_template('About.html')
@app.route('/servicing.html')
def service():
    return render_template('servicing.html')
@app.route('/pricing.html')
def price():
    return render_template('pricing.html')

@app.route('/ourteam.html')
def ourteam():
    return render_template('ourteam.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

    
@app.route('/finddoctor.html')
def find():
    return render_template('finddoctor.html')


@app.route('/take_appointement.html')
def gototakeapp():
    return render_template('take_appointement.html')


@app.route('/shop.html')
def shop():
    return render_template('shop.html')


@app.route('/forgetPassword.html')
def forget():
    return render_template('forgetPassword.html')
#---------------to load users from database----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Authentication successful
            if user.role == 'admin':
                login_user(user)
                return redirect(url_for('show_users'))

            else:
                return redirect(url_for('display_image',  email=email))
        else:
            # Authentication failed
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
       
        hashed_password = generate_password_hash(password)
       
        new_user = User(full_name=full_name, email=email, password=hashed_password, phone_number=phone_number,
                        date_of_birth=date_of_birth, address=address)
        
        db.session.add(new_user)
        db.session.commit()
       
        return redirect(url_for('login'))
    return render_template('signup.html')





#show users----------------------------------------------------------------- 
@app.route('/user')
def show_users():
    users = User.query.all()
    return render_template('user.html', users=users)

#-----------------rest api route and function
@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])
@app.route('/usersrest')
def display_list_users():
    return render_template('usersrest.html')



#edit user---------------------------------------------------- 

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        if current_user.role != 'admin':
            flash("Access Denied", "error")
            
            return redirect(url_for('index'))
        
        user.full_name = request.form.get('full_name', user.full_name)
        user.email = request.form.get('email', user.email)
        user.phone_number = request.form.get('phone_number', user.phone_number)
        user.date_of_birth = request.form.get('date_of_birth', user.date_of_birth)
        user.address = request.form.get('address', user.address)
        
        password = request.form.get('password')
        if password:
            user.password = generate_password_hash(password)
        
        db.session.commit()
        
        flash("User updated successfully", "success")
        return redirect(url_for('show_users'))
    
    return render_template('edit_user.html', user=user)


#---------------------------delete user-----------------------------------------------
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    if current_user.role != 'admin':
        return 'Access Denied'

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))







#--------------------------------------appointment filter----------------------------------------------
@app.route('/appointments', methods=['GET'])
def appointments():
    user_email = request.args.get('user_email')
    if user_email:
        appointments = Patients.query.filter_by(email=user_email).all()
    else:
        
        appointments = Patients.query.all()

    return render_template('datatablemake.html', Patients=appointments)

#-----------------show id appointment------------------------------
@app.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    appointment = Patients.query.get(id)
    if appointment:
        return render_template('datatablemake.html', appointment=appointment)
    else:
        return 'Appointment not found', 404
    

    #-----------------------------delete patients----------------------------------------------
    
@app.route('/appointments/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Patients.query.get(id)
    if appointment:
        user_email = appointment.email
        db.session.delete(appointment)
        db.session.commit()
        appointments = Patients.query.filter_by(email=user_email).all()
        return render_template('datatablemake.html', Patients=appointments)
    else:
        return 'Appointment not found', 404

#----------------------------------updaaaate appointment -----------------------------------------------------------


   

@app.route('/appointments/update/<int:id>', methods=['GET', 'POST'])
def update_appointment(id):
    patient = Patients.query.get(id)
    
    if not patient:
        return render_template('error.html', message="Patient not found.")
    
    if request.method == 'POST':
      
            patient.name = request.form['doctor']
            patient.email = request.form['email']
            patient.phone = request.form['phone_number']
            patient.visitday = request.form['visitday']
            patient.status = request.form['status']
            user_email = patient.email
            
            db.session.commit()
            flash('Patient Updated Successfully!', 'success')
            
         
            appointments = Patients.query.filter_by(email=user_email).all()
            return render_template('datatablemake.html', Patients=appointments)
        

    return render_template('edit_patient.html', patient=patient )









#------------------------------------------------------------------------------------------

@app.route('/appointments/<string:email>')
def appointmentsby(email):
    appointments = Patients.query.filter_by(email=email).all()
    return render_template('appointments_by_email.html', appointments=appointments, email=email)

@app.route('/patient/<int:user_id>', methods=['GET'])
def show_patients():
    user_email = request.args.get('user_email')
    if user_email:
        appointments = Patients.query.filter_by(email=user_email).all()
    else:
        
        appointments = Patients.query.all()

    return render_template('datatablemake.html', Patients=appointments)


#----------------------------------------forget pass------------------------------------------------------


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        session['reset_email'] = email
        
     
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
       
        session['reset_code'] = code
        
        sender_email = "haydariifatimaa@gmail.com"  
        subject = "Password Reset Code"
        message = f"Your password reset code is: {code}"
        send_email(sender_email, email, subject, message)
        
        return render_template('verifycode.html')  
    else:
        return render_template('forgetPassword.html')
    

    #-------------------------------------------------------------------------------------

 
@app.route('/verify-code', methods=['POST'])
def verify_code():
    if 'reset_code' in session:
        submitted_code = request.form['code']
        stored_code = session['reset_code']
        
        if submitted_code == stored_code:
        
            return redirect(url_for('password_reset', email=session.get('reset_email')))
        else:
         
            return render_template('submissions.html') 
    else:
       
        return render_template('submissions.html') 

@app.route('/password-reset')
def password_reset():
    # Retrieve email from URL parameters
    email = request.args.get('email')
    return redirect(url_for('display_image', email=email))


#------------------------------------------------------------------------------------------------


class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.String(10), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)


@app.route('/medical')
def medicalrecord():
    return render_template('medicalrecord.html')

#----------------------------------------------------------------------------------------------------

@app.route('/upload', methods=['POST'])
def upload():
    patient_name = request.form['patient_name']
    email = request.form['email']
    date_of_birth = request.form['date_of_birth']
    image = request.files['photo_path']

    print("Received file:", image.filename) 

    if image:
        image_data = image.read()
        print("Encoded image data:", image_data[:50])  
    else:
        image_data = None

    print("Attempting to save record...")

    
    try:
        existing_record = MedicalRecord.query.filter_by(email=email).one()
        print("Record already exists. Updating...")

        existing_record.patient_name = patient_name
        existing_record.date_of_birth = date_of_birth
        existing_record.image = image_data if image_data else None

        db.session.commit()

        print("Record updated successfully.")  
        return redirect(url_for('medicalrecord'))

    except NoResultFound:
        print("No existing record found. Creating new record...")
        new_record = MedicalRecord(
            patient_name=patient_name,
            email=email,
            date_of_birth=date_of_birth,
            image=image_data if image_data else None  
        )

        db.session.add(new_record)
        db.session.commit()

        print("New record saved successfully.")  
        return redirect(url_for('medicalrecord'))

    except Exception as e:
        print("An error occurred:", str(e))
        db.session.rollback()
        return jsonify({"error": "An error occurred"}), 500








@app.route('/display/<email>')
def display_image(email):
    record = MedicalRecord.query.filter_by(email=email).first()
    if record and record.image:
        return render_template('display_image.html', image_data=base64.b64encode(record.image).decode('utf-8'), name=record.patient_name, email=record.email,)
    else:
        return "No medical record found for the specified email or no image available."
    





@app.route('/api/records', methods=['GET'])
def get_all_records():
    records = MedicalRecord.query.all()
    all_records = []

    for record in records:
        record_data = {
            "patient_name": record.patient_name,
            "email": record.email,
            "date_of_birth": record.date_of_birth,
            "image_data": base64.b64encode(record.image).decode('utf-8') if record.image else None
        }
        all_records.append(record_data)

    return jsonify(all_records), 200


@app.route('/api/records/<email>', methods=['GET'])
def get_record(email):
    record = MedicalRecord.query.filter_by(email=email).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    response = {
        "patient_name": record.patient_name,
        "email": record.email,
        "date_of_birth": record.date_of_birth,
        "image_data": base64.b64encode(record.image).decode('utf-8') if record.image else None
    }
    return jsonify(response)


if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
        db.create_all()

    app.run(debug=True)
