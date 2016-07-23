from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('LoGiN.html')


@app.route("/")
def login():
    return render_template('hOmEpAge.html')


if __name__ == '__main__':
    app.run()
