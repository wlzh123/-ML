#coding:utf-8
from math import *
import operator
"""
@参考《机器学习实战》
"""
def creatData():
    data=[["青绿","蜷缩","硬滑","是"],
          ["乌黑","蜷缩","软粘","否"],
          ["青绿","蜷缩","硬滑","是"],
          ["青绿","稍蜷","硬滑","否"],
          ["浅白","蜷缩","硬滑","是"],
          ["浅白","稍蜷","硬滑","否"]
          ]
    label=["H","B"]#H:好瓜，B：坏瓜
    return data , label
#计算数据的熵
def culShannon(data):
    labels={}
    
    dataSumCount=len(data)
    for vec in data:
        labelvalue =vec[-1]
        if labelvalue not in labels.keys():
            labels[labelvalue]=0
        labels[labelvalue]+=1
    shannon=0.0
    for label in labels:
        p=float(labels[label]/dataSumCount)
        shannon=shannon-(p*log(p,2))
    return shannon

#根据属性划分数据
def splitdata(data,axis,value):
    """
    data:数据集
    axis:第几个特征
    value:特征值
    """
    redataset=[]
    for dv in data:
        if dv[axis]==value:
            re=dv[:axis]
            re.extend(dv[axis+1:])
            redataset.append(re)
    return redataset
#选择最佳的属性进行分类
def chooseBestFeatureSplit(dataset):
    numF=len(dataset[0])-1 #属性个数
    beforeEnc=culShannon(dataset) #数据的基本熵
    datasetSize =len(dataset)
    bestFeature=-1
    bastInfoGain=0.0
    for i in range(numF):
        feaList=[ex[i] for ex in dataset]#选出第i个属性的所有特征
        ufeaList=set(feaList)
        newEntropy =0.0
        for value in ufeaList:  #计算每一个属性的分类增益
            subset=splitdata(dataset,i,value)
            prob = float(len(subset))/datasetSize
            newEntropy+=prob*culShannon(subset)
        infoGain=beforeEnc-newEntropy
        if(infoGain >bastInfoGain):#保存最大增益的属性
            bastInfoGain=infoGain
            bestFeature =i
    return bestFeature

def majorityLabel(labelList):
    labelCount={}
    for label in labelList:
        if label not in labelCount:
            labelCount[label]=0
        labelCount[count]+=1
    sortedCount = sorted(labelCount.items(),key=operator.itemgetter(1),reversed=True);
    return sortedCount[0][0]

def creatTree(dataset,labels):
    classList=[vect[-1] for vect in dataset]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataset[0])==1:
        return majorityLabel(classList)
    labelscp=labels[:]
    bestFeature = chooseBestFeatureSplit(dataset)
    bestLabel = labelscp[bestFeature]
    del(labelscp[bestFeature])
    mytree ={bestLabel:{}}
    feature=[vect[bestFeature] for vect in dataset]
    uniqFeatValue=set(feature)
    for value in uniqFeatValue:
        sublabels = labelscp[:]
        mytree[bestLabel][value] = creatTree(splitdata(dataset,bestFeature,value),sublabels) #递归创建子树
    return mytree
'''分类识别函数'''
def classify(inputTree,labels,testVect):
    firstStr = list(inputTree.keys())[0]
    # firstStr = inputTree.keys()[0];#获得当前树的根属性的key值
    secondDict = inputTree[firstStr];#获得根节点的子树集合
    feataindex = labels.index(firstStr);#获得当前根属性标签在属性集合中的位置

    for key in secondDict.keys():#遍历当前属性的对应的所有值
        if testVect[feataindex] == key:
           
            if isinstance(secondDict[key],(dict)):
                classlabel = classify(secondDict[key],labels,testVect);
            else: classlabel = secondDict[key]

    return  classlabel
if __name__ =='__main__':   
    data,labels=creatData()
    shannon=culShannon(data)
    tree = creatTree(data,labels)
    print(tree)
    print(chooseBestFeatureSplit(data))
