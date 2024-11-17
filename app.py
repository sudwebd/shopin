from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages

# Simple in-memory storage (will reset when server restarts)
waitlist_entries = []

@app.route('/success')
def success():
    return render_template('templates/success.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        phone = request.form.get('phone')
        
        # Basic phone number validation
        if not phone or len(phone) != 10:
            flash('Please enter a valid 10-digit phone number', 'error')
            return redirect(url_for('home'))
        
        # Check if phone number already exists
        if any(entry['phone'] == phone for entry in waitlist_entries):
            flash('This phone number is already registered!', 'info')
            return redirect(url_for('home'))
        
        try:
            waitlist_entries.append({
                'phone': phone,
                'created_at': datetime.utcnow()
            })
            flash('Thanks for joining our waitlist!', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('home'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)