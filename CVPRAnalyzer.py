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
def author_papernum_analyze(data):
    author_papernum_dict = {}
    for i in data.author_list:
        for j in i:
            if j not in author_papernum_dict:
                author_papernum_dict[j] = 1
            else:
                author_papernum_dict[j] += 1
    return author_papernum_dict


# 标题单词-词频
def titleword_wordfrequency_analyze(data):
    titleword_wordfrequency_dict = {}
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    for i in data.title_list:
        word_list = i.lower().split(' ')
        for j in word_list:
            j = j.strip('!"%&\'()*+,-.:;=?`~­–—“”')
            if len(j) > 1 and j[-2] == '\'':
                j = j[:-2]
            j = lemmatizer.lemmatize(j, pos='n')
            j = lemmatizer.lemmatize(j, pos='v')
            if len(j) > 1 and j not in stop_words:
                if j not in titleword_wordfrequency_dict:
                    titleword_wordfrequency_dict[j] = 1
                else:
                    titleword_wordfrequency_dict[j] += 1
    return titleword_wordfrequency_dict


# 标题字符长度-论文数量
def titlecharlength_papernum_analyze(data):
    titlecharlength_papernum_dict = {}
    for i in data.title_list:
        if len(i) not in titlecharlength_papernum_dict:
            titlecharlength_papernum_dict[len(i)] = 1
        else:
            titlecharlength_papernum_dict[len(i)] += 1
    return titlecharlength_papernum_dict


# 标题单词长度-论文数量
def titlewordlength_papernum_analyze(data):
    titlewordlength_papernum_dict = {}
    for i in data.title_list:
        title_word_list = i.split(' ')
        if len(title_word_list) not in titlewordlength_papernum_dict:
            titlewordlength_papernum_dict[len(title_word_list)] = 1
        else:
            titlewordlength_papernum_dict[len(title_word_list)] += 1
    return titlewordlength_papernum_dict


# 论文数量-作者数量
def papernum_authornum_analyze(data):
    author_papernum_dict = {}
    for i in data.author_list:
        for j in i:
            if j not in author_papernum_dict:
                author_papernum_dict[j] = 1
            else:
                author_papernum_dict[j] += 1
    papernum_authornum_dict = {}
    for i in author_papernum_dict:
        if author_papernum_dict[i] not in papernum_authornum_dict:
            papernum_authornum_dict[author_papernum_dict[i]] = 1
        else:
            papernum_authornum_dict[author_papernum_dict[i]] += 1
    return papernum_authornum_dict


# 作者数量-论文数量
def authornum_papernum_analyze(data):
    authornum_papernum_dict = {}
    for i in data.author_list:
        if len(i) not in authornum_papernum_dict:
            authornum_papernum_dict[len(i)] = 1
        else:
            authornum_papernum_dict[len(i)] += 1
    return authornum_papernum_dict


def csv_generate(years, original_dicts, filename):
    if len(years) != len(original_dicts):
        print(filename + '.csv generation failed.')
        return
    previous_dict = original_dicts[0]
    for i in original_dicts:
        current_dict = i
        if previous_dict != current_dict:
            for j in current_dict:
                value = previous_dict.get(j)
                if value:
                    current_dict[j] += value
            for j in previous_dict:
                value = previous_dict.get(j)
                find = current_dict.get(j)
                if not find:
                    current_dict[j] = value
        previous_dict = current_dict
    if not os.path.isdir('csv'):
        os.makedirs('csv')
    with open('csv/' + filename + '.csv', 'w', newline='', encoding='utf-8')as f:
        header = ['name', 'value', 'date']
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(years)):
            for j in original_dicts[i]:
                row = [j, original_dicts[i][j], years[i]]
                writer.writerow(row)
    print(filename + '.csv generation succeeded.')


if __name__ == '__main__':
    print('CVPRAnalyzer')
