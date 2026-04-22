from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return '''
        <html>
            <head><title>My Flask App</title></head>
            <body>
                <h1>Welcome to My Flask Interface!</h1>
                <p>This is a simple Flask web interface.</p>
            </body>
        </html>
    '''

# Route with user input
@app.route('/greet/<name>')
def greet(name):
    return f'<h1>Hello, {name}!</h1>'

# Route with form handling
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = request.form.get('data')
        return f'<h2>You submitted: {data}</h2>'
    return '''
        <form method="POST">
            <input type="text" name="data" placeholder="Enter something">
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
