import requests
from datetime import datetime
import pandas as pd
from app.models import Project, User

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )

def dbgout():
    user = User.query.filter_by(slack_flag=1)
    print(1)
    user_df = pd.read_sql(user.statement, user.session.bind)
    user_id = list(user_df['id'])

    if user_id :
        for ids in user_id :
            project = Project.query.filter_by(userid=ids)
            project_df = pd.read_sql(project.statement, project.session.bind)

            project_live = list(project_df[project_df['status']=='LIVE']['name'])

            if project_live :
                message = '\n'.join(project_live)
            else :
                message = "Not Live Project"

            token_set = user_df[user_df['id']==ids]['slack_token']
            channel_name = "#{}".format(user_df[user_df['id']==ids]['slack_bot'])

            strbuf =datetime.now().strftime('LIVE Check [%m/%d %H:%M:%S]\n') + message

            post_message(token_set, channel_name, strbuf)

