import pycountry

survey_list = [
    ("","Nothing selected"),("Online", "Online"), ("CAPI", "CAPI"), ("CATI","CATI"), ("Hybrid", "Hybrid(Gang/FGD)"), ("Other", "Other")
]
country_list = [(c.alpha_3, c.name) for c in list(pycountry.countries)]

status_list = [
    ("TEST", "Programming"),
    ("QC", "Test Link Send"),
    ("LIVE", "Live Link Send"),
    ("END", "End of Survey")
]

survey_tool = [
    ("","Nothing selected"),
    ("Dimension", "Dimension"),
    ("Nfiled", "Nfield"),
    ("Decipher", "Decipher"),
    ("Confirmit", "Confirmit"),
    ("Smartsurvey", "Smart Survey")
]