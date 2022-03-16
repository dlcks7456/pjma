from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Project, User
from ..forms import ProjectForm
from ..choices import country_list
from .. import db
from ..fnc import *
from .auth_views import login_required

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    return redirect(url_for("project._list"))
