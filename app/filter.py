# import locale
# locale.setlocale(locale.LC_ALL, '')
from flask import url_for
from .choices import country_list

def format_datetime(value, fmt='%Y-%m-%d'):
    if not value == None :
        return value.strftime(fmt)
    else :
        return value

def checked(value) :
    if not value == None :
        if value == 0 :
            return ""
        if value == 1 :
            return "<img src='{}'/ width='30px'>".format(url_for('static', filename='img/check.png'))

def country_name_list(value) :
    if not value == None :
        value = value.split(',')
        country_name_list = [name for alpha_3, name in country_list if alpha_3 in value]
        return country_name_list

def country_cnt(value) :
    if not value == None :
        value = value.split(',')
        if len(value) <= 3 :
            return ", ".join(value)
        else :
            return "{} Country".format(len(value))

def country_only_cnt(value) :
    if not value == None :
        value = value.split(',')
        return len(value)

def comma_number(value) :
    if not value == None :
        return format(value,',')

