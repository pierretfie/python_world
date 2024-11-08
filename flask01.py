from flask import Flask, render_template

#initialize flask app
app = Flask(__name__)

#route definition to home page
@app.route('/')
def home():
    return "Hello World!"


#run the app

if __name__ == '__main__':
    app.run(debug=True)
