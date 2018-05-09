#coding utf-8
from numpy import *
"""参考机器学习实战"""
class SMO:
    def __init__(self,dataMatIn,classLabels,C,toler,maxIter):
        self.X=dataMatIn
        self.labelMat =classLabels
        self.C=C
        self.tol =toler
        self.maxIter = maxIter
    def smo(dataMatIn,classLabels,C,toler,maxIter):
        dataMatrix = mat(dataMatIn)
        labelMat =mat(classLabels).transpose()
        b=0
        m,n=shape(dataMatirx)#样本空间是(m*n)
        alphas =mat(zeros((m,1))) #alphas (m*1)
                                  #wi=(alphas(i)*y(i)*x(i))
        iter =0
        while(iter<maxIter):
            #修改a的次数
            alphaPairsChanged = 0
            
            #外层循环，找第一个不符合KKT条件的a1
            for i in  range(m):
                
                #求出第i个样本对应的预测值
                fXi=float(multiply(alphas,labelMat).T*(dataMatrix[i,:].T)) +b
                # 求出预测值与真实值之间的差值，这个差值也就是迭代更新需要缩小的值
                Ei =fXi-float(labelMat[i])
                if((labelMat[i]*Ei <-toler)and(alphas[i]<C))or((labelMat[i]*Ei>toler)and(alphas[s]>0)):
                    j=selectJrand(i,m)
                    fXj= float(multiply(alphas,labelMat).T*(dataMatirx[j,:].T))+b

                    Ej=fXj-float(labelMat[j])

                    alphaIold =alphas[i].copy()
                    alphaJold =alphas[j].copy()
                    #求上下边界
                    if(labelMat[i]!=labelMat[j]):
                        L=max(0,alphas[j]-alphas[i])
                        H=min(C,C+alphas[j]-alphas[i])
                    else:
                        L=max(0,alphas[j]+alphas[i]-C)
                        H=min(C,alphas[j]+alphas[i])
                    if L==H:
                        print("L==H")
                        continue
                    eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                    if eta>=0:
                        print("eta>=0")
                        continue
                    #求出a2的更新值
                    alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                    #依据上下边界对a2进行剪辑
                    alphas[j]=clipAlpha(alphas[j],H,L)
                    #判断新值与旧值之间是否有修改，没有修改则不符合，下一个
                    if(abs([alphas[j]-alphaJold])<0.00001):
                        print("j not moving enough")
                        continue
                    # 新a1值
                    alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                    对b的值进行修改
                    b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                    b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                    if (0 < alphas[i]) and (C > alphas[i]): b = b1
                    elif (0<alphas[j])and(C>alphas[i]):b=b2
                    else:
                        b=(b1+b2)/2
                    # 一旦上面有对a做了更新就+1
                    alphaPairsChanged += 1
                    print( "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
                    
            # 在遍历完一遍a的所有值后就判断是否有更新，有更新就迭代次数不变，继续，若没有就迭代数加1
            if (alphaPairsChanged == 0): iter += 1
            else: iter = 0
            print( "iteration number: %d" % iter)
                    
        return b,alphas           
                    
                    
                
