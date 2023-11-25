from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def panoramic_tour():
    image_folder = 'static/images'
    images = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    return render_template('index.html', images=images)


if __name__ == '__main__':
    app.run(debug=True)
