# encoding:UTF-8
from urllib import request
import re

def spider(key):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Connection': 'keep-alive'
    }

    itemb = []
    # 修改页数
    for i in range(0, 50):
        url1 = 'https://www.sogou.com/sogou?site=news.qq.com&ie=utf-8&query='
        url = url1 + request.quote(key) + '&page=' + str(i + 1)
        req = request.Request(url, headers=headers)  # 请求，生成对象
        request1 = request.urlopen(req).read()  # 爬取源代码
        content = request1.decode('UTF-8')
        pattern = r'<h3.+?>.*?</h3>'
        item1 = re.findall(pattern, content, re.S | re.M)
        item2 = ''.join(item1)  # 合并列表为字符串
        pattern = r'href=\"(http.*?)"'
        itema = re.findall(pattern, item2, re.S | re.M)
        itemb = itemb + itema
    i = 0
    for line in itemb:
        url2 = line
        req = request.Request(url2, headers=headers)
        request1 = request.urlopen(req).read()
        content = request1.decode('UTF-8')
        pattern = re.compile(r'URL=\'(.*?)\'')
        itemc = re.findall(pattern, content)
        url = itemc[0]
        try:
            req1 = request.Request(url, headers=headers)
            request1 = request.urlopen(req1).read()
            content_b = request1.decode('gbk')
            pattern_a = r'<p.*?>(.*?)</p>'
            items = re.findall(pattern_a, content_b, re.S | re.M | re.I)
            p = i // 100
            filename = str(p) + '.txt'
            f1 = open('C:/Users/gsl/Desktop/大三/工作室/tmp/' + filename, 'a')  # 输出文件地址，要改一下
            f1.write('第' + str(i) + '章')
            f1.write("\n")
            for item in items:
                item = re.sub("[a-z]", "", item)  # 去除英文字母
                f1.write(item)
                f1.write("\n")
            f1.close()
            i = i + 1
        except:
            pass



