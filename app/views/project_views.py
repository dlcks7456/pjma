from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from app.models import Project, User
from ..forms import ProjectForm
from ..choices import country_list
from .. import db
from ..fnc import *
from .auth_views import login_required


bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/list')
@login_required
def _list():
    # 프로젝트 전체 리스트
    project_list = Project.query.filter_by(userid=g.user.id).order_by(Project.id.desc())
    #project_list = Project.query.order_by(Project.id.desc())

    # page 나누기
    page = request.args.get('page', type=int, default=1)  # 페이지
    project_list = project_list.paginate(page, per_page=30)

    return render_template('project/project_list.html', project_list=project_list)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProjectForm()

    if request.method == 'POST' and form.validate_on_submit() :
        project = Project(name=form.name.data,
                          type=form.type.data,
                          tool=form.tool.data,
                          status=form.status.data,
                          country=",".join(form.country.data),
                          testqc=form.testqc.data,
                          liveqc=form.liveqc.data,

                          # Date Format
                          startday=valueDateTimeFormat(form.startday.data),
                          testlinkday=valueDateTimeFormat(form.testlinkday.data),
                          livelinkday=valueDateTimeFormat(form.livelinkday.data),
                          endday=valueDateTimeFormat(form.endday.data),
                          comment=form.comment.data,
                          tracking=form.tracking.data,
                          sample = form.sample.data,
                          userid=g.user.id,
                          username=g.user.username
                          )

        if not project.livelinkday is None and project.testlinkday is None:
            flash("테스트 링크 전달 날짜 응답 필요")
            return render_template('project/project_create.html', form=form)
        else :
            if not project.livelinkday is None and not project.testlinkday is None :
                diff = project.testlinkday - project.startday
                project.start_test = diff.days

        if not project.endday is None and project.livelinkday is None:
            flash("라이브 링크 전달 날짜 응답 필요")
            return render_template('project/project_create.html', form=form, project_id=project_id)
        else:
            if not project.endday is None and not project.livelinkday is None:
                diff_live_test = project.livelinkday - project.testlinkday
                diff_end_live = project.endday - project.livelinkday
                diff_end_start = project.endday - project.startday

                project.test_live = diff_live_test.days
                project.live_end = diff_end_live.days
                project.start_end = diff_end_start.days

        if dateValueCheck(valueDateTimeFormat(form.startday.data), valueDateTimeFormat(form.testlinkday.data)):
            flash("테스트 링크 전달 날짜 확인 필요")
            return render_template('project/project_create.html', form=form)

        elif dateValueCheck(valueDateTimeFormat(form.testlinkday.data), valueDateTimeFormat(form.livelinkday.data)):
            flash("라이브 링크 전달 날짜 확인 필요")
            return render_template('project/project_create.html', form=form)

        elif dateValueCheck(valueDateTimeFormat(form.livelinkday.data), valueDateTimeFormat(form.endday.data)):
            flash("종료 날짜 확인 필요")
            return render_template('project/project_create.html', form=form)




        db.session.add(project)
        db.session.commit()

        return redirect(url_for('project._list'))


    return render_template('project/project_create.html', form=form)


@bp.route('/views/<int:project_id>/', methods=['GET', 'POST'])
@login_required
def views(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project/project_view.html', project=project)

@bp.route('/update/<int:project_id>/', methods=['GET', 'POST'])
@login_required
def _update(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST" :
        form = ProjectForm()
        if form.validate_on_submit():
            form.populate_obj(project)

            project.country = ",".join(form.country.data)

            # Date Format
            project.startday = valueDateTimeFormat(form.startday.data)
            project.testlinkday = valueDateTimeFormat(form.testlinkday.data)
            project.livelinkday = valueDateTimeFormat(form.livelinkday.data)
            project.endday = valueDateTimeFormat(form.endday.data)

            project.tracking = 0 if form.tracking.data==None else form.tracking.data

            if not project.livelinkday is None and project.testlinkday is None:
                flash("테스트 링크 전달 날짜 응답 필요")
                return render_template('project/project_create.html', form=form)
            else :
                if not project.livelinkday is None and not project.testlinkday is None :
                    diff = project.testlinkday - project.startday
                    project.start_test = diff.days

            if not project.endday is None and project.livelinkday is None:
                flash("라이브 링크 전달 날짜 응답 필요")
                return render_template('project/project_create.html', form=form, project_id=project_id)
            else:
                if not project.endday is None and not project.livelinkday is None:
                    diff_live_test = project.livelinkday - project.testlinkday
                    diff_end_live = project.endday - project.livelinkday
                    diff_end_start = project.endday - project.startday

                    project.test_live = diff_live_test.days
                    project.live_end = diff_end_live.days
                    project.start_end = diff_end_start.days

            if dateValueCheck(project.startday, project.testlinkday) :
                flash("테스트 링크 전달 날짜 확인 필요")
                return render_template('project/project_create.html', form=form, project_id=project_id)

            elif dateValueCheck(project.testlinkday, project.livelinkday) :
                flash("라이브 링크 전달 날짜 확인 필요")
                return render_template('project/project_create.html', form=form, project_id=project_id)

            elif dateValueCheck(project.livelinkday, project.endday) :
                flash("종료 날짜 확인 필요")
                return render_template('project/project_create.html', form=form, project_id=project_id)

            else :
                db.session.commit()

            return redirect(url_for('project.views', project_id=project_id))
    else :
        form = ProjectForm(obj=project)
        form.country.data = ''.join(form.country.data)

    return render_template('project/project_create.html', form=form, project_id=project_id)


@bp.route('/delete/<int:project_id>/', methods=['GET', 'POST'])
@login_required
def _delete(project_id) :
    project = Project.query.get_or_404(project_id)
    if g.user != project.user :
        flash("삭제 권한이 없습니다.")
        return render_template('project/project_view.html', project=project)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project._list'))

