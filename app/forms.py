from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from .choices import survey_list ,country_list, status_list, survey_tool
from .fnc import valueDateTimeFormat


class ProjectForm(FlaskForm):
    name = StringField("Project Name", validators=[DataRequired("프로젝트 이름 입력")])
    type = SelectField("Type", choices=survey_list, validate_choice=True, validators=[DataRequired("프로젝트 타입 선택")])
    status = SelectField("Status", choices=status_list, validate_choice=True, validators=[DataRequired("Status 선택")])
    country = SelectMultipleField("Country", choices=country_list, validators=[DataRequired("조사 국가 선택")])
    tool = SelectField("Survey Tool", choices=survey_tool, validators=[DataRequired("Tool 선택")])
    tracking = IntegerField("Tracking")
    startday = StringField("Start Day", validators=[DataRequired("시작 날짜 선택")])
    testlinkday = StringField("Test link send")
    livelinkday = StringField("Live link send")
    testqc = IntegerField("Test QC Count", [validators.Optional()])
    liveqc = IntegerField("Live QC Count", [validators.Optional()])
    endday = StringField("End Day")
    sample = IntegerField("Total Sample", [validators.Optional()])
    comment = TextAreaField("관련 사항  입력")


class UserCreateForm(FlaskForm) :
    username = StringField("ID", validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('Check Password', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField("ID", validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])

class UserInfo(FlaskForm) :
    slack_token = StringField("Slack Token")
    slack_bot = StringField("Channel name")
    slack_flag = IntegerField("Bot check")

