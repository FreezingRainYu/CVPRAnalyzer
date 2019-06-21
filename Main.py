from CVPRAnalyzer import *

years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
titleword_wordfrequncy_list = []
for year in years:
    data = parse_data(year)
    titleword_wordfrequncy_dict = titleword_wordfrequncy_analyze(data)
    titleword_wordfrequncy_list.append(titleword_wordfrequncy_dict)
csv_generate(years, titleword_wordfrequncy_list, 'title')
