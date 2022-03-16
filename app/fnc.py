from datetime import datetime

def valueDateTimeFormat(value) :
    if not value == '' :
        return datetime.strptime(value, '%Y-%m-%d %H:%M')
    else :
        return None


def dateValueCheck(date1, date2) :
    if not date1 == None and not date2 == None :
        if date1 > date2 :
            return True
        else :
            return False
    else :
        return False
