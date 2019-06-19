import csv
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
    def __init__(self, year, author_list, title_list):
        self.year = year
        self.author_list = author_list
        self.title_list = title_list


def parse_data(year):
    author_list = []
    title_list = []
    data = get_data(year)
    for i in data:
        if i[0] == 'a':
            reversed_name_list = []
            original_name_list = i[10:-6].split(' and ')
            for original_name in original_name_list:
                separated_name = original_name.split(', ')
                separated_name.reverse()
                reversed_name = ' '.join(separated_name)
                reversed_name_list.append(reversed_name)
            author_list.append(reversed_name_list)
        if i[0] == 't':
            title = i[9:-6]
            title_list.append(title)
    return ParsedData(year, author_list, title_list)


# 作者-论文数量
def author_paperquantity_analyze(author_list):
    author_paperquantity_dict = {}
    for i in author_list:
        for j in i:
            if j not in author_paperquantity_dict:
                author_paperquantity_dict[j] = 1
            else:
                author_paperquantity_dict[j] += 1
    return author_paperquantity_dict


# 标题单词-词频
def titleword_wordfrequncy_analyze(title_list):
    titleword_wordfrequncy_dict = {}
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    for i in title_list:
        word_list = i.lower().split(' ')
        for j in word_list:
            j = j.strip('!"%&\'()*+,-.:;=?`~­–—“”')
            if len(j) > 1 and j[-2] == '\'':
                j = j[:-2]
            j = lemmatizer.lemmatize(j, pos='n')
            j = lemmatizer.lemmatize(j, pos='v')
            if j and len(j) > 1 and j not in stop_words:
                if j not in titleword_wordfrequncy_dict:
                    titleword_wordfrequncy_dict[j] = 1
                else:
                    titleword_wordfrequncy_dict[j] += 1
    return titleword_wordfrequncy_dict


# 标题长度-论文数量
def titlelength_paperquantity_analyze(title_list):
    titlelength_paperquantity_dict = {}
    for i in title_list:
        if len(i) not in titlelength_paperquantity_dict:
            titlelength_paperquantity_dict[len(i)] = 1
        else:
            titlelength_paperquantity_dict[len(i)] += 1
    return titlelength_paperquantity_dict


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
    return paperquantity_authorquantity_dict


def csv_generate(years, original_dicts, filename):
    index = 0
    previous_dict = original_dicts[0]
    current_dict = original_dicts[0]
    for i in original_dicts:
        if previous_dict != current_dict:
            for j in current_dict:
                value = previous_dict.get(j)
                if value:
                    current_dict[j] += value
        previous_dict = original_dicts[index]
        index += 1
        if index < len(original_dicts):
            current_dict = original_dicts[index]
    if not os.path.isdir('result'):
        os.makedirs('result')
    with open('result/' + filename + '.csv', 'w', newline='', encoding='utf-8')as f:
        header = ['name', 'value', 'date']
        body = []
        writer = csv.writer(f)
        writer.writerow(header)
        index = 0
        for i in original_dicts:
            for j in i:
                row = [j, i[j], years[index]]
                body.append(row)
                writer.writerow(row)
            index = index + 1


if __name__ == '__main__':
    yrs = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
    apds = []
    for y in yrs:
        d = parse_data(y)
        apd = author_paperquantity_analyze(d.author_list)
        apds.append(apd)
        print(apd)
    csv_generate(yrs, apds, 'author')
