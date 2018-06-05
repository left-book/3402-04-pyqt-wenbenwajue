
import regex
import re
import jieba
import jieba.posseg as psg

def write(path,linkList,openStyle="w"): #path为文件名，linkList为一串字符或者中文,判断输出其中内容
    if isinstance(linkList,list) or isinstance(linkList,set):
        #如果linkList是list(列表)或者是set(集合)的实例，返回Ture，否则Fluse
        with open(path,openStyle,encoding="utf-8") as f:
            for each in linkList:
                f.write(each+"\n") #把linkList中的每个字为一行输出

    if isinstance(linkList,str):
        #如果它是str类型的
        with open(path, openStyle, encoding="utf-8") as f:
            f.write(linkList)



def GetStopWordsList(filePath): #将filePathe里的内容加到stopWords（停用词）列表里
    #stopWords=[line.strip() for line in open(filePath,"r",encoding="utf-8").readlines()]
    stopWords=[]
    for line in open(filePath,"r",encoding="utf-8").readlines():
        unicodeHead="\ufeff"     #unicode文件头
        line=line.strip("\r\n %s"%unicodeHead)
        stopWords.append(line)
    return stopWords



def GetFileContent(filePath): #读取并输出filePath的内容
    with open(filePath,"r",encoding="utf-8") as f:
        return f.read()
    return ""



def ReadFileList(filePath): #将filePath的内容去除换行符并放进List中
    List=[]
    with open(filePath, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip("\n ")  # 'https://flowerillust.com/frame.html\n'  去掉换行符
            List.append(line)
    return List


def BBiaodian(str): #判断str开头是否是标点符号
    re = regex.compile(r"^[-！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.]+$")
    bMatch = re.match(str)
    if bMatch:
        return True
    else:
        return False


def BEng(str): #判断str开头是否是数字或者字母

    re=regex.compile(r"^[A-Za-z0-9]+$")
    bMatch=re.match(str)
    if bMatch:
        return True
    else:
        return False



def GetTop(n,wlist):  #将wlist中的元素出现的次数从大到小排列[('a',20),('d',15),('h',8)......]
    if n>len(wlist):  #如果n大于wlist的长度，则将wlist的长度值赋予n
        n=len(wlist)

    keys = set(wlist) #keys是wlist元素的集合（无序，不重复）
    dic = {}
    for w in keys:
        dic[w] = wlist.count(w) #dic内是wlist中每个元素出现的次数的数量的字典

    dlist = list(dic.items()) #把dic字典里的内容变成列表存储到dlist中
    dlist.sort(key=lambda x: x[1], reverse=True) #将dlist的元素值从大到小排序

    relist=[]
    for i in range(20): #relist=['0','1','2'....'19']
        relist.append(i)

    return relist

