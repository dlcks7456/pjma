from .choices import status_list
from .colors import colors
import random
import pandas as pd
import numpy as np
from collections import OrderedDict

class dashboardData :
    def __init__(self, df):
        self.df = df

        #status 변수
    def status(self) :
        status_count = {value:self.df[self.df["status"] == value ].shape[0] for value, label in status_list }
        status_count["TOTAL"] = sum(status_count.values())
        return status_count

    def sa(self, var):
        sa_count = dict(self.df.groupby([var])[var].count())
        sa_labels = list(sa_count.keys())
        sa_data = list(sa_count.values())
        sa_color = random.sample(colors, len(sa_data))

        return {"labels": sa_labels, "data": sa_data, "color": sa_color}

    def tracking(self):
        trc_count = {}
        trc_count["Ad hoc"] = self.df[self.df["tracking"]==0].shape[0]
        trc_count["Tracking"] = self.df[self.df["tracking"]==1].shape[0]

        trc_labels = list(trc_count.keys())
        trc_data = list(trc_count.values())

        trc_color = random.sample(colors, len(trc_count.values()))

        return {"labels": trc_labels, "data": trc_data, "color": trc_color}

    def country_2way(self):
        try :
            country_data = self.df["country"].str.split(",")
            country_data = list(country_data)
            total_cnt = len(country_data)
            kor_cnt = country_data.count(["KOR"])
            foreign_cnt = total_cnt - kor_cnt

            labels = ["KOR", "MCP"]
            data = [kor_cnt, foreign_cnt]
            color = random.sample(colors, len(data))

            return {"labels": labels, "data": data, "color": color, "total": total_cnt}
        except :
            return {"labels": [], "data": [], "color": [], "total": 0}

    def country(self):
        try :
            country_data = sum(list(self.df["country"].str.split(",")), [])
            country_data = {"country": country_data}
            country_df = pd.DataFrame(country_data)
            country_dict = dict(country_df.groupby(["country"])["country"].count())

            ordered_dict = OrderedDict()

            if "KOR" in country_dict.keys() :
                ordered_dict["KOR"] = country_dict["KOR"]

            for key, value in country_dict.items() :
                if not key == "KOR" :
                    ordered_dict[key] = value

            labels = []
            data = []
            for key, value in ordered_dict.items() :
                labels.append(key)
                data.append(value)

            color = random.sample(colors, len(data))

            return {"labels": labels, "data":data, "color":color, "total":len(data)}
        except :
            return {"labels": [], "data": [], "color": [], "total": 0}

    def qc(self):
        try :
            test_qc_df = self.df[['testqc']]
            test_qc_descibe = dict(test_qc_df.describe().round())
            test_qc_dict = dict(test_qc_descibe['testqc'])
            test_qc_dict['total'] = test_qc_df['testqc'].sum()

            live_qc_df = self.df[['liveqc']]
            live_qc_descibe = dict(live_qc_df.describe().round())
            live_qc_dict = dict(live_qc_descibe['liveqc'])
            live_qc_dict['total'] = live_qc_df['liveqc'].sum()

            return {'testqc': test_qc_dict, 'liveqc': live_qc_dict}
        except :
            return {'testqc': [], 'liveqc': []}

    def month_qc(self):
        try :
            date_df = self.df[['startday','testqc','liveqc', 'sample']]
            date_df.set_index('startday', inplace=True)
            date_df.fillna(np.nan)

            test_month_data = []
            live_month_data = []
            project_count_data = []
            sample_count_data = []
            for m in range(1, 13) :
                test_mean = 0
                live_mean = 0
                project_count = 0
                sample_count = 0
                for n, g in date_df.groupby(pd.Grouper(freq='M')) :
                    if n.month == m :
                        test_mean = g['testqc'].mean()
                        live_mean = g['liveqc'].mean()
                        project_count = g.shape[0]
                        sample_count = g['sample'].sum()

                test_month_data.append(test_mean)
                live_month_data.append(live_mean)
                project_count_data.append(project_count)
                sample_count_data.append(sample_count)

            month_df = {'testqc':test_month_data, 'liveqc':live_month_data, 'project_count': project_count_data, 'sample_count': sample_count_data}
            month_df = pd.DataFrame(month_df)
            month_df.fillna(0, inplace=True)

            color = random.sample(colors, 2)

            return {'testqc': list(month_df['testqc']),
                    'liveqc': list(month_df['liveqc']),
                    'project_count': list(month_df['project_count']),
                    'sample_count': list(month_df['sample_count']),
                    'total_sample' : int(sum(list(month_df['sample_count']))),
                    'color':color}
        except :
            return {'testqc': [], 'liveqc': [], 'project_count':[], 'sample_count':[], 'total_sample':0, 'color': []}


    def duration(self):
        try :
            days_df = self.df[['start_test', 'test_live', 'live_end', 'start_end']]
            return {'start_test': dict(days_df['start_test'].describe().round()),
                    'test_live' : dict(days_df['test_live'].describe().round()),
                    'live_end' : dict(days_df['live_end'].describe().round()),
                    'start_end' : dict(days_df['start_end'].describe().round())}
        except :
            return {'start_test': {}, 'test_live' : {}, 'live_end' : {}, 'start_end' : {}}