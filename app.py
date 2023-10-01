from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder='static')

# Initialize a placeholder for status (you can set it to False initially)
status = False  # Assuming no motion initially

@app.route('/')
def index():
    return render_template('index.html', boolean_data=status)

@app.route('/get_status')
def get_status():
    # Return the current status (boolean_data) to the client
    global status  # Access the status variable defined in this script
    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(debug=True)
    
