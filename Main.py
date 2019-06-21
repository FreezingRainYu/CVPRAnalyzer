from CVPRAnalyzer import *

years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
data_list = []
for year in years:
    data = parse_data(year)
    data_dict = titleword_wordfrequncy_analyze(data)
    data_list.append(data_dict)
    print(data_dict)
csv_generate(years, data_list, 'title')
