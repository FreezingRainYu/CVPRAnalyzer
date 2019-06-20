from CVPRAnalyzer import *

yrs = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
twds = []
for y in yrs:
    d = parse_data(y)
    twd = titleword_wordfrequncy_analyze(d.title_list)
    twds.append(twd)
    print(twd)
csv_generate(yrs, twds, 'title')
