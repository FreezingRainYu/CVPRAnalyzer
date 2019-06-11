import os
from urllib.request import urlopen


def get_data(year):
    if not os.path.isdir('data'):
        os.makedirs('data')
    url = 'http://openaccess.thecvf.com/CVPR' + year + '.py'
    source = urlopen(url).read().decode('utf-8').splitlines()
    initials = ['a', 't']
    data = [i for i in source if i and i[0] in initials]
    with open('data/CVPR' + year, 'w', encoding='utf-8') as f:
        for i in data:
            f.write(i)
            f.write('\n')
    return data


if __name__ == '__main__':
    lst = ['2013', '2014', '2015', '2016', '2017', '2018', '2019']
    for y in lst:
        d = get_data(y)
        print(d)
