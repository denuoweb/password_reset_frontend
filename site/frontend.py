from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change 'your_secret_key' to an actual secret key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        if email.endswith('.edu'):
            flash('Email received: {}'.format(email))
            # You can add the logic for processing the .edu email here
            return redirect(url_for('success'))
        else:
            flash('Please enter a valid .edu email address')
            return redirect(url_for('error'))

@app.route('/home_token')
def home_token():
    return render_template('home_token.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/success_token')
def success_token():
    return render_template('success_token.html')

@app.route('/error_token')
def error_token():
    return render_template('error_token.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
