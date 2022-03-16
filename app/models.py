from app import db

class Project(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(45), nullable=False, server_default='TEST')
    type = db.Column(db.String(45),  nullable=False)
    tool = db.Column(db.String(45), nullable=False)
    country = db.Column(db.Text(), nullable=False)
    tracking = db.Column(db.Integer, nullable=False, server_default='0')
    startday = db.Column(db.DateTime(), nullable=False)
    testlinkday = db.Column(db.DateTime(), nullable=True)
    start_test = db.Column(db.Integer, nullable=True)
    livelinkday = db.Column(db.DateTime(), nullable=True)
    test_live = db.Column(db.Integer, nullable=True)
    endday = db.Column(db.DateTime(), nullable=True)
    live_end = db.Column(db.Integer, nullable=True)
    start_end = db.Column(db.Integer, nullable=True)
    testqc = db.Column(db.Integer, nullable=True)
    liveqc = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text(), nullable=True)
    sample = db.Column(db.Integer, nullable=True)
    user = db.relationship('User', backref=db.backref('project'))


class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    #slack bot id
    slack_token = db.Column(db.Text, nullable=True)
    slack_bot = db.Column(db.Text, nullable=True)
    slack_flag = db.Column(db.Integer, nullable=False, server_default='0')
    email = db.Column(db.String(120), unique=True, nullable=False)


