import io

from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash, make_response
from app.models import Project
from ..forms import ProjectForm
from ..choices import country_list
from .. import db
from ..fnc import *
from .auth_views import login_required
from ..dashboardData import dashboardData
import pandas as pd

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/dashboard')
@login_required
def dashboard():
    # 본인 프로젝트만 현황 확인
    project_list = Project.query.filter_by(userid=g.user.id)
    df = pd.read_sql(project_list.statement, project_list.session.bind)
    df.set_index('id', inplace=True)

    dbd = dashboardData(df)

    return render_template('dashboard/view.html', dbd=dbd)


@bp.route('/download')
@login_required
def download():
    project_list = Project.query.filter_by(userid=g.user.id)
    df = pd.read_sql(project_list.statement, project_list.session.bind)
    df.set_index('id', inplace=True)

    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

    df.to_excel(excel_writer=writer, sheet_name="myproject")
    writer.save()
    writer.close()

    excel_file = make_response(out.getvalue())
    excel_file.headers["Content-Disposition"] = "attachment; filename=MyProject_{}.xlsx".format(datetime.now().strftime('%Y%m%d'))
    excel_file.headers["Content-type"] = "application/x-xls"

    return excel_file