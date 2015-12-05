from flask_security.forms import ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import Required

class ExtendedRegisterForm(ConfirmRegisterForm):
    username = StringField('Username')
