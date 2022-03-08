from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/rgstr')
def rgstr():
    return render_template('login/rgstr.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
