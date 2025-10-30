from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, Email, Optional
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Bharatig%401980@localhost/healthcare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------- MODELS --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient_appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, foreign_keys='Appointment.doctor_id')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    problem_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------- FORMS --------------------
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
    specialization = StringField('Specialization', validators=[Optional()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int)
    doctor_id = SelectField('Doctor', coerce=int)
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    problem_description = TextAreaField('Problem Description', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# -------------------- LOGIN MANAGER --------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    # Count totals for cards
    total_patients = User.query.filter_by(role='patient').count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()

    return render_template(
        'index.html',
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data[:120], password_hash=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()

        # Add Doctor record if role is doctor
        if form.role.data == 'doctor':
            new_doctor = Doctor(
                name=form.username.data,
                specialization=form.specialization.data or "General"
            )
            db.session.add(new_doctor)
            db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('login_register.html', form=form, action='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login_register.html', form=form, action='login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if current_user.role != 'doctor':
        flash('Only doctors can add new doctors.')
        return redirect(url_for('index'))

    class AddDoctorForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired()])
        specialization = StringField('Specialization', validators=[DataRequired()])
        phone = StringField('Phone', validators=[Optional()])
        submit = SubmitField('Add Doctor')

    form = AddDoctorForm()
    if form.validate_on_submit():
        new_doc = Doctor(name=form.name.data, specialization=form.specialization.data, phone=form.phone.data)
        db.session.add(new_doc)
        db.session.commit()
        flash('Doctor added successfully!')
        return redirect(url_for('doctors'))

    return render_template('add_doctor.html', form=form)

# -------------------- BOOK APPOINTMENT --------------------
@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if current_user.role != 'patient':
        flash('Only patients can book appointments.')
        return redirect(url_for('index'))

    form = AppointmentForm()
    form.patient_id.choices = [(current_user.id, current_user.username)]
    doctors = Doctor.query.order_by(Doctor.name).all()
    form.doctor_id.choices = [(d.id, d.name) for d in doctors]

    if not doctors:
        flash('No doctors are available. Please register a doctor first.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        existing = Appointment.query.filter_by(
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data
        ).first()
        if existing:
            flash('Doctor already has an appointment at this time.')
            return redirect(url_for('book'))

        new_appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data,
            problem_description=form.problem_description.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully!')
        return redirect(url_for('index'))

    return render_template('book.html', form=form)

# -------------------- CONTACT --------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_msg = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_msg)
        db.session.commit()
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# -------------------- DELETE / UPDATE --------------------
@app.route('/delete_patient/<int:id>')
@login_required
def delete_patient(id):
    if current_user.role != 'doctor':
        flash('Only doctors can delete patients.')
        return redirect(url_for('index'))
    patient = User.query.get_or_404(id)
    Appointment.query.filter_by(patient_id=patient.id).delete()
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!')
    return redirect(url_for('index'))

@app.route('/delete_doctor/<int:id>')
@login_required
def delete_doctor(id):
    if current_user.role != 'doctor':
        flash('Only doctors can delete doctors.')
        return redirect(url_for('index'))
    doctor = Doctor.query.get_or_404(id)
    Appointment.query.filter_by(doctor_id=doctor.id).delete()
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!')
    return redirect(url_for('index'))

@app.route('/delete_appointment/<int:id>')
@login_required
def delete_appointment(id):
    if current_user.role != 'doctor':
        flash('Only doctors can delete appointments.')
        return redirect(url_for('index'))
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!')
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>/<status>')
@login_required
def update_status(id, status):
    if current_user.role != 'doctor':
        flash('Only doctors can update appointment status.')
        return redirect(url_for('index'))
    appointment = Appointment.query.get_or_404(id)
    appointment.status = status
    db.session.commit() 
    flash('Appointment status updated!')
    return redirect(url_for('index'))

# View Patients
@app.route('/view_patients')
# @login_required
def view_patients():
    patients = User.query.filter_by(role='patient').order_by(User.username).all()
    return render_template('patient_list.html', patients=patients)

# View Doctors
@app.route('/view_doctors')
# @login_required
def view_doctors():
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('doctor_list.html', doctors=doctors)

# View Appointments
@app.route('/view_appointments')
def view_appointments():
    if current_user.is_authenticated:
        if current_user.role == 'patient':
            appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
        elif current_user.role == 'doctor':
            doctor = Doctor.query.filter_by(name=current_user.username).first()
            if doctor:
                appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
            else:
                appointments = []
        else:
            appointments = Appointment.query.all()
    else:
        # Guest view — show all appointments safely
        appointments = Appointment.query.all()
        
    return render_template('appointment_list.html', appointments=appointments)



# -------------------- RUN --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)