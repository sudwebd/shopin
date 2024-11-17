from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class WaitlistEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<WaitlistEntry {self.phone}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        phone = request.form.get('phone')
        
        # Basic phone number validation
        if not phone or len(phone) < 10:
            flash('Please enter a valid phone number', 'error')
            return redirect(url_for('home'))
        
        # Check if phone number already exists
        if WaitlistEntry.query.filter_by(phone=phone).first():
            flash('This phone number is already registered!', 'info')
            return redirect(url_for('home'))
        
        try:
            new_entry = WaitlistEntry(phone=phone)
            db.session.add(new_entry)
            db.session.commit()
            flash('Thanks for joining our waitlist!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            
        return redirect(url_for('home'))
    
    return render_template('index.html')

@app.route('/admin/waitlist')
def view_waitlist():
    entries = WaitlistEntry.query.order_by(WaitlistEntry.created_at.desc()).all()
    return render_template('admin/waitlist.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
