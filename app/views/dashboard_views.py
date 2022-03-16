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
from datetime import datetime

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/dashboard/')
@login_required
def dashboard():
    # 본인 프로젝트만 현황 확인
    project_list = Project.query.filter_by(userid=g.user.id)
    df = pd.read_sql(project_list.statement, project_list.session.bind)
    df.set_index('id', inplace=True)


    year = request.args.get('year', type=int, default=datetime.now().year)

    data_df = df[df['startday'].dt.year == year]
    data_df.fillna('', inplace=True)

    dbd = dashboardData(data_df)

    year_df = df.set_index('startday')
    yearList = list(set([n.year for n, g in year_df.groupby(pd.Grouper(freq='Y'))]))

    return render_template('dashboard/view.html', dbd=dbd, year=year, yearList=yearList)


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