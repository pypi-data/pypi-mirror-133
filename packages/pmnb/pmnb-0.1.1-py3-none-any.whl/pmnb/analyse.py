#coding=utf-8
try:
    import numpy as np
    import pandas as pd
    import time
    from sklearn.linear_model import LogisticRegression
except ModuleNotFoundError as err:
    print("你还没有安装程序所依赖的包，请输入以下命令安装:pip install {0} --yes".format(err.name))
    
else:
    def importance_lr():
        """
        重要影响分析线性版本
        :param file: 本地文件地址
        :return: 特征以及重要程度
        """
        #数据准备
        print('①请按照下面的格式，准备您的excel数据,格式要求见文档https://shimo.im/sheets/hPdQxXWCwP3chpDk/MODOC/')
        print("②输入你准备好的excel数据的本地地址，比如：/Users/xxx/Desktop/test1.xlsx")
        time.sleep(1)
       #获取数据
        print('请输入')
        file=str(input())
        data=pd.read_excel(file)
        
       #建模
        labelList=data.iloc[:,-1]
        featurelist=pd.get_dummies(data.iloc[:,0:-1])
        
        #初始化LogisticRegression
        lr = LogisticRegression() 
        #训练
        lr.fit(featurelist, labelList) 
        
        #输出结果
        features=['']
        importance=['']
        features=list(featurelist.head(0))
        importance=list(lr.coef_[0])
        print('数据录入成本，分析结果如下')
        res=pd.DataFrame({'特征':features,'重要程度':importance})
        res=res.sort_values(by='重要程度')
        return res
