from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import User
from . import db

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', user=current_user)
