from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired


class ImageUploadForm(FlaskForm):
    image = FileField('Image File', validators=[FileRequired(message="Please Select Image"),
                                                FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    submit = SubmitField("Upload Image File")
