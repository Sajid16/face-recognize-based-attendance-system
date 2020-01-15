from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/')
def index():
    return render_template('webcam_auto_test.html')


@app.route('/try', methods=['GET', 'POST'])
def ttry():
    if request.method == 'POST':
        x = request.form.get("latitude")
        y = request.form.get("longitude")
        z = request.form.get("altitude")
        print(x)
        print(y)
        print(z)
    return ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(host='10.11.201.69', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))

    # app.run(host='202.40.190.114', port=5000)
