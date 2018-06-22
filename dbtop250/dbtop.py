from bs4 import BeautifulSoup
from urllib.request import urlopen


def onePage(this_url):
    html = urlopen(this_url)
    bs = BeautifulSoup(html, 'html.parser')
    movie_list = bs.findAll("div", {"class": "info"})
    info = []
    for i in movie_list:
        # title
        title = i.span.get_text()

        # link
        link = i.a['href']

        # director
        str_director = i.p.get_text().split()
        if str_director[1][0] >= 'A' and str_director[1][0] <= 'Z':   # 处理英文名
            director = str_director[1] + ' ' + str_director[2]
        else:
            director = str_director[1]

        # score
        tag_score = i.select('[class="rating_num"]')
        score = tag_score[0].get_text()

        # quote
        quote = ''
        tag_quote = i.select('[class="quote"]')
        if len(tag_quote) > 0:                      # 存在空标签
            list_quote = tag_quote[0].get_text().split()
            for j in list_quote:
                quote += (j + ' ')
            quote = quote.strip()

        info.append([title, director, score, link, quote])      # 每条信息

    return info


def writeFile(info, index, first):
    if first:
        mode = 'wt'
    else:
        mode = 'a'      # 追加模式打开文件
    with open('dbtop250.txt', mode, encoding='utf-8') as file:       # 存在外文字符，使用UTF-8编码
        now = 1
        for i in info:
            file.write(str(now + index) + ' ')
            file.write('  '.join(i) + '\n')
            index += 1
            print(i)
    file.close()


def main():
    mode = True
    for i in range(10):  # 10 pages
        if i != 0:
            mode = False
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        info = onePage(url)
        writeFile(info, i * 25, mode)


if __name__ == '__main__':
    main()