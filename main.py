import base64
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, url_for
from form import ImageUploadForm
import os
from PIL import Image


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEYS')
Bootstrap(app)

processed_image = None
top_colors = None


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def get_top_colors(image, num_colors=10):
    image = image.convert('RGB')
    colors = image.getcolors(maxcolors=256*256*256)
    if not colors:
        raise ValueError("Too many colors in the image")

    sorted_color = sorted(colors, key=lambda x: x[0], reverse=True)
    top_colors_hex = [(count, rgb_to_hex(color)) for count, color in sorted_color[:num_colors]]
    return top_colors_hex[:num_colors]


@app.route('/',  methods=["GET", "POST"])
def home():
    global processed_image, top_colors
    image_upload_form = ImageUploadForm()
    if image_upload_form.validate_on_submit():
        image_file = image_upload_form.image.data.read()
        processed_image = base64.b64encode(image_file).decode('utf-8')

        image_upload_form.image.data.seek(0)
        open_image = Image.open(image_upload_form.image.data)

        top_colors = get_top_colors(open_image, num_colors=10)

        return redirect(url_for('home'))
    return render_template('index.html', image_upload_form=image_upload_form, image_file=processed_image, top_colors=top_colors)


if __name__ == '__main__':
    app.run(debug=True)
