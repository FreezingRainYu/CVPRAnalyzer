import csv
import os
from copy import deepcopy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from urllib.request import urlopen


# 获取数据
def get_data(year):
    year = str(year)
    if not os.path.isdir('data'):
        os.makedirs('data')
    if not os.path.isfile('data/CVPR' + year):
        url = 'http://openaccess.thecvf.com/CVPR' + year + '.py'
        source = urlopen(url).read().decode('utf-8').splitlines()
        initials = ['a', 't']
        data = [line for line in source if line and line[0] in initials]
        with open('data/CVPR' + year, 'w', encoding='utf-8') as f:
            for line in data:
                f.write(line)
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


# 解析数据
def parse_data(year):
    author_list = []
    title_list = []
    data = get_data(year)
    for line in data:
        if line[0] == 'a':
            reversed_name_list = []
            original_name_list = line[10:-6].split(' and ')
            for original_name in original_name_list:
                separated_name = original_name.split(', ')
                separated_name.reverse()
                reversed_name = ' '.join(separated_name)
                reversed_name_list.append(reversed_name)
            author_list.append(reversed_name_list)
        if line[0] == 't':
            title = line[9:-6]
            title_list.append(title)
    return ParsedData(year, author_list, title_list)


# {作者: 该作者的论文数量}
def author_papernum_analyze(data):
    author_papernum_dict = {}
    for authors in data.author_list:
        for author in authors:
            if author not in author_papernum_dict:
                author_papernum_dict[author] = 1
            else:
                author_papernum_dict[author] += 1
    return author_papernum_dict


# {标题单词: 该单词的词频}
def titleword_wordfrequency_analyze(data):
    titleword_wordfrequency_dict = {}
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    for title in data.title_list:
        words = title.lower().split()
        for word in words:
            word = word.strip('!"%&\'()*+,-.:;=?`~­–—“”')
            if len(word) > 1 and word[-2] == '\'':
                word = word[:-2]
            word = lemmatizer.lemmatize(word, pos='n')
            word = lemmatizer.lemmatize(word, pos='v')
            if len(word) > 1 and word not in stop_words:
                if word not in titleword_wordfrequency_dict:
                    titleword_wordfrequency_dict[word] = 1
                else:
                    titleword_wordfrequency_dict[word] += 1
    return titleword_wordfrequency_dict


# {标题字符长度: 符合该长度的论文数量}
def titlecharlength_papernum_analyze(data):
    titlecharlength_papernum_dict = {}
    for title in data.title_list:
        if len(title) not in titlecharlength_papernum_dict:
            titlecharlength_papernum_dict[len(title)] = 1
        else:
            titlecharlength_papernum_dict[len(title)] += 1
    return titlecharlength_papernum_dict


# {标题单词长度: 符合该长度的论文数量}
def titlewordlength_papernum_analyze(data):
    titlewordlength_papernum_dict = {}
    for title in data.title_list:
        words = title.split()
        if len(words) not in titlewordlength_papernum_dict:
            titlewordlength_papernum_dict[len(words)] = 1
        else:
            titlewordlength_papernum_dict[len(words)] += 1
    return titlewordlength_papernum_dict


# {论文数量: 满足该论文数量的作者数量}
def papernum_authornum_analyze(data):
    author_papernum_dict = author_papernum_analyze(data)
    papernum_authornum_dict = {}
    for author in author_papernum_dict:
        if author_papernum_dict[author] not in papernum_authornum_dict:
            papernum_authornum_dict[author_papernum_dict[author]] = 1
        else:
            papernum_authornum_dict[author_papernum_dict[author]] += 1
    return papernum_authornum_dict


# {作者数量：满足该作者数量的论文数量}
def authornum_papernum_analyze(data):
    authornum_papernum_dict = {}
    for authors in data.author_list:
        if len(authors) not in authornum_papernum_dict:
            authornum_papernum_dict[len(authors)] = 1
        else:
            authornum_papernum_dict[len(authors)] += 1
    return authornum_papernum_dict


# 累加历年数据字典，生成数据字典列表
def accumulate_dicts(years, original_dicts_list):
    if len(years) != len(original_dicts_list):
        raise IndexError
    accumulated_dicts_list = deepcopy(original_dicts_list)
    previous_dict = accumulated_dicts_list[0]
    for original_dict in accumulated_dicts_list:
        current_dict = original_dict
        if previous_dict != current_dict:
            for i in current_dict:
                value = previous_dict.get(i)
                if value:
                    current_dict[i] += value
            for i in previous_dict:
                value = previous_dict.get(i)
                find = current_dict.get(i)
                if not find:
                    current_dict[i] = value
        previous_dict = current_dict
    return accumulated_dicts_list


# 根据某年数据字典生成csv文件
def generate_csv_by_dict(year, source_dict, filename):
    if not os.path.isdir('csv'):
        os.makedirs('csv')
    with open('csv/' + filename + '.csv', 'w', newline='', encoding='utf-8')as f:
        header = ['name', 'value', 'date']
        writer = csv.writer(f)
        writer.writerow(header)
        for item in source_dict:
            row = [item, source_dict[item], year]
            writer.writerow(row)


# 根据历年数据字典列表生成csv文件
def generate_csv_by_list(years, source_dicts_list, filename):
    if not os.path.isdir('csv'):
        os.makedirs('csv')
    with open('csv/' + filename + '.csv', 'w', newline='', encoding='utf-8')as f:
        header = ['name', 'value', 'date']
        writer = csv.writer(f)
        writer.writerow(header)
        for index in range(len(years)):
            for item in source_dicts_list[index]:
                row = [item, source_dicts_list[index][item], years[index]]
                writer.writerow(row)


if __name__ == '__main__':
    print('CVPRAnalyzer')
