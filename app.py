from flask import Flask, render_template

# Starter Flask-serveren
app = Flask(__name__)

# Fortæller serveren, at når man går ind på forsiden ("/"), skal den vise vores HTML-fil
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Starter programmet på port 5000
    app.run(debug=True, port=5000)