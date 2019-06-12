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


class ParsedData:
    def __init__(self, author_list, title_list):
        self.author_list = author_list
        self.title_list = title_list


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
    return ParsedData(author_list, title_list)


# 作者-论文数量
def author_paperquantity_analyze(author_list):
    author_paperquantity_dict = {}
    for i in author_list:
        for j in i:
            if j not in author_paperquantity_dict:
                author_paperquantity_dict[j] = 1
            else:
                author_paperquantity_dict[j] += 1
    author_paperquantity_list = sorted(author_paperquantity_dict.items(), key=lambda item: item[1], reverse=True)
    return author_paperquantity_list


# 标题长度-论文数量
def titlelength_paperquantity_analyze(title_list):
    titlelength_paperquantity_dict = {}
    for i in title_list:
        if len(i) not in titlelength_paperquantity_dict:
            titlelength_paperquantity_dict[len(i)] = 1
        else:
            titlelength_paperquantity_dict[len(i)] += 1
    titlelength_paperquantity_list = sorted(titlelength_paperquantity_dict.items(), reverse=True)
    return titlelength_paperquantity_list


# 论文数量-作者数量
def paperquantity_authorquantity_analyze(author_list):
    author_paperquantity_dict = {}
    for i in author_list:
        for j in i:
            if j not in author_paperquantity_dict:
                author_paperquantity_dict[j] = 1
            else:
                author_paperquantity_dict[j] += 1
    paperquantity_authorquantity_dict = {}
    for i in author_paperquantity_dict:
        if author_paperquantity_dict[i] not in paperquantity_authorquantity_dict:
            paperquantity_authorquantity_dict[author_paperquantity_dict[i]] = 1
        else:
            paperquantity_authorquantity_dict[author_paperquantity_dict[i]] += 1
    paperquantity_authorquantity_list = sorted(paperquantity_authorquantity_dict.items())
    return paperquantity_authorquantity_list


if __name__ == '__main__':
    lst = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
    for y in lst:
        d = parse_data(y)
        pal = paperquantity_authorquantity_analyze(d.author_list)
        print(pal)
