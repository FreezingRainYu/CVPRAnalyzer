import os
from urllib.request import urlopen


def get_data(year):
    year = str(year)
    if not os.path.isdir('data'):
        os.makedirs('data')
    if not os.path.isfile('data/CVPR' + year):
        url = 'http://openaccess.thecvf.com/CVPR' + year + '.py'
        source = urlopen(url).read().decode('utf-8').splitlines()
        initials = ['a', 't']
        data = [i for i in source if i and i[0] in initials]
        with open('data/CVPR' + year, 'w', encoding='utf-8') as f:
            for i in data:
                f.write(i)
                f.write('\n')
        return data
    else:
        with open('data/CVPR' + year, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
        return data


def parse_data(year):
    author_list = []
    title_list = []
    data = get_data(year)
    for i in data:
        if i[0] == 'a':
            original_name_list = i[10:-6].split(' and ')
            reversed_name_list = []
            for original_name in original_name_list:
                separated_name = original_name.split(', ')
                separated_name.reverse()
                reversed_name = ' '.join(separated_name)
                reversed_name_list.append(reversed_name)
            author_list.append(reversed_name_list)
        if i[0] == 't':
            title = i[9:-6]
            title_list.append(title)
    return dict(zip(title_list, author_list))


if __name__ == '__main__':
    lst = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
    for y in lst:
        d = parse_data(y)
        print(d)
