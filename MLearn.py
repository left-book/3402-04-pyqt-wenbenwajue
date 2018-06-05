#!/usr/bin/env Python
#coding=gbk
import jieba
import common
from head import *
import dataParse

import pickle #save and load����

from gensim import corpora, models, similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#�����־���涨�����ʽ

def GenList(filePath,att="",bAddTail=False):
    dataParse.init()
    sentences = dataParse.GetGensimList(filePath, att,bAddTail=bAddTail)
    genList = dataParse.CleanWords_gensim(sentences, nMinLen=1, att=att,bAddTail=bAddTail)
    return genList



#�����ֵ�
def GenDic(filePath,att="",savePath=""):
    genList = GenList(filePath,att=att)
    dictionary = corpora.Dictionary(genList)
    if savePath!="":
        dictionary.save(savePath)
    return dictionary

#�����ֵ�
def GenDic_byList(genList,savePath=""):
    dictionary = corpora.Dictionary(genList)
    if savePath!="":
        dictionary.save(savePath)
    return dictionary


#���ֵ佫���ϴʴ�ת��Ϊ�����ռ�
def GenList2Bow(genList,dic,savePath=""):
    corpus=[dic.doc2bow(subtextList) for subtextList in genList]
    if savePath!="":
        corpora.MmCorpus.serialize(savePath,corpus)
    return corpus

#��ʼ����ת��Ϊtfidf����
def OriCorpus2tfidf(corpus,savePath=""):
    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf=tfidf_model[corpus]

    if savePath:
        corpora.MmCorpus.serialize(savePath, corpus_tfidf)

    return corpus_tfidf

#tfidf���ϣ����Ƴ�����
def ToIndex(corpus_tfidf,savePath=""):
    index=similarities.MatrixSimilarity(corpus_tfidf)

    if savePath:
        index.save(savePath)
    return index


class MyCorpus(object):
    def __init__(self,dic,filePath):
        self.dic=dic
        self.filePath=filePath

    def __iter__(self):
        for line in open(self.filePath,"r",encoding="utf-8"):
            line=line.strip()
            if line=="":
                continue
            wList=jieba.cut(line)
            yield self.dic.doc2bow(wList)

#�������ļ���ת��Ϊ�����ռ�
def ToBow(dic,filePath,savePath=""):
    '''

    :param dic:       �ֵ�
    :param filePath:
    :return:          ����
    '''
    corpus_mem_friendly=MyCorpus(dic,filePath)
    vec=[]
    for lineVec in corpus_mem_friendly:
        if lineVec: #�ǿ��������룬       ����������ȥ
            vec.append(lineVec)

    if savePath:
        corpora.MmCorpus.serialize(savePath, vec)  # store to disk, for later use
    return vec


def SaveVec(vec,savePath):
    if savePath:
        corpora.MmCorpus.serialize(savePath, vec)  # store to disk, for later use

#Ԥ����׶Σ����ɲ����������Ϣ
def SaveRc(filePath,bookName,dirPath=""):

    #�����ֵ�
    dic=GenDic(filePath)
    if dirPath:
        prePath="/".join([dirPath,bookName])
    else:
        prePath=bookName

    #�����ֵ�
    dicPath=".".join([prePath,"dict"])
    dic.save(dicPath)                                      # �ֵ� dict

    genList=GenList(filePath,bAddTail=True)

    #�ĵ������䣩������Ӧ��ϵ
    docMapPath=".".join([prePath, "pkl"]) #�ĵ�ӳ�䣬�����Ƕ���ӳ��
    docDict={}
    nIndex=0
    for li in genList:
        doc=li[-1]
        docDict[nIndex]=doc
        del li[-1]
        nIndex+=1

    output=open(docMapPath,"wb")
    pickle.dump(docDict,output)        # ����  �ĵ�����
    output.close()

    #��ʼ����
    corpus=GenList2Bow(genList,dic)
    #ģ��
    tfidf_model = models.TfidfModel(corpus)
    #tf����
    corpus_tfidf=tfidf_model[corpus]
    #��������
    bowPath_tfd = ".".join([prePath, "mm_tf"])
    corpora.MmCorpus.serialize(bowPath_tfd, corpus_tfidf) # tfidf����

    #����ģ��
    tf_modelPath = ".".join([prePath, "tfidf"])
    tfidf_model.save(tf_modelPath)                         # tfidfģ��

    #lsiģ�ͣ���lsi����
    lsi_model = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=200)
    corpus_lsi = lsi_model[corpus_tfidf]

    #����lsi����
    bowPath_lsi= ".".join([prePath, "mm_lsi"])
    corpora.MmCorpus.serialize(bowPath_lsi, corpus_lsi)    #lsi ����

    #����lsiģ��
    lsi_modelPath = ".".join([prePath, "lsi"])
    lsi_model.save(lsi_modelPath)     #lsiģ��     same for tfidf, lda, ...

    Word2Vec(genList, ".".join([prePath, "w2v"]))


    #��lsi���ϱ��Ƴ�������ʽ�������ѯ��������
    simIndex = similarities.MatrixSimilarity(corpus_lsi)  #��������
    indexPath=".".join([prePath, "index"])
    simIndex.save(indexPath)


#���ظ�����Ϣ
def LoadRc(bookName,dirPath=""):
    if dirPath:
        prePath="/".join([dirPath,bookName])
    else:
        prePath=bookName
    #�����ĵ��������ֵ��Ӧ��ϵ
    pklfile=open(".".join([prePath,"pkl"]),"rb")
    docDict=pickle.load(pklfile)
    pklfile.close()
    #�����ֵ�
    dic = corpora.Dictionary.load(".".join([prePath,"dict"]))
    #����tfidf����
    corpus_tf = corpora.MmCorpus(".".join([prePath,"mm_tf"]))
    #����lsi����
    corpus_lsi = corpora.MmCorpus(".".join([prePath, "mm_lsi"]))
    #����tfidfģ��
    tf_model = models.TfidfModel.load(".".join([prePath, "tfidf"]))
    #����lsiģ��
    lsi_model = models.LsiModel.load(".".join([prePath, "lsi"]))

    #�������ϱ��Ƶ������ļ�
    simIndex = similarities.MatrixSimilarity.load(".".join([prePath, "index"]))

    return dic,corpus_tf,corpus_lsi,tf_model,lsi_model,docDict,simIndex

#��ѯ�����
def Qurey(qStr,dic,tfidf_model,lsi_model,simIndex,docDict):

    #��ѯ�ַ���ת��ʼ����
    bow=dic.doc2bow(jieba.cut(qStr))
    #��ʼ����תtfidf����
    tfidf_bow=tfidf_model[bow]
    #tfidf����תlsi����
    lsi_bow=lsi_model[tfidf_bow]
    #�����ѯ���������������ռ��������
    sim_q=simIndex[lsi_bow]
    #������Ƚ�������
    sims = sorted(enumerate(sim_q), key=lambda item: -item[1])
    for k, v in sims[:50]:
        print(k, v, docDict[k])


def QureyStr(qStr,bNeedSave=False):

    if bNeedSave:
        # ��ʼ��
        # ��¥���ֵ����ɡ��������ɡ�ģ�����ɡ��������ɣ��ĵ���Ӧ��ϵ������������
        SaveRc("��¥��.txt","��¥��","tmp")

    # �����ֵ䡢���ϡ�ģ�͡��������ĵ���Ӧ��ϵ
    dic, corpus_tf, corpus_lsi, tf_model, lsi_model, docDict, simIndex = LoadRc("��¥��", "tmp")

    # ��С˵�� ��ѯ����һ�仰��������Ķ���
    Qurey(qStr, dic, tf_model, lsi_model, simIndex, docDict)



def Word2Vec(simList,savePath=""):
    model=models.Word2Vec(simList,       #gensim �б���ʽ�����
                            size=100,    #������ά��
                            window=5,
                            min_count=5, #ֻ���ǳ��ִ�������5�Ĵ�
                            workers=4)

    if savePath:
        model.save(savePath)

    return model

def QureyWord(qWord):
    model=models.Word2Vec.load("tmp//��¥��.w2v")
    for k,v in model.most_similar(positive=[qWord]):
        print(k,v)

#find_relationship("����","����","����")
def find_relationship(a, b, c):
    """
    ���� d
    a��b�Ĺ�ϵ����c��d�Ĺ�ϵһ��
    """
    model = models.Word2Vec.load("tmp//��¥��.w2v")
    d, _ = model.most_similar(positive=[c, b], negative=[a])[0]
    print("������{}���롰{}������{}���͡�{}�������ƵĹ�ϵ".format(a, b, c, d))

SaveRc("f0.txt","f0","tmp")
#QureyWord("���")
#find_relationship("����","����","���")
