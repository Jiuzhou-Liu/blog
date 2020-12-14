
from flask import render_template, flash, redirect, url_for, Blueprint
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('auth/login.html')


