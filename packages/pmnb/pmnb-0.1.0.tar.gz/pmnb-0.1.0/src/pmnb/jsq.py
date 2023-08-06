"""
写一个常用的包，用来解决平时的各种问题
"""
#!/usr/bin/env python
# coding: utf-8

try:
    import numpy as np
    import time
    from math import sqrt
    from statsmodels.stats.power import NormalIndPower

except ModuleNotFoundError as err:
    print("你还没有安装程序所依赖的包，请输入以下命令安装:pip install {0} --yes".format(err.name))
    
else:
#提升多少ipr

    def ipr(old_num,new_num):
        print ('{0} 相比{1}:  提升绝对值{2},  相对值{3}%'.format(new_num,old_num,round((new_num-old_num),2),round((new_num-old_num)/old_num*100,2)))

    #AB样本量计算ABSample
    def ABSample():
        print("请输入实验主要指标当前值 __ %（点击率，留存率等，比如：35%请直接输入 35）")
        u=input()
        u=float(u)/100
        print("请输入最小可以观测的提升比例__% （就是最少提升百分之几你觉得才ok，相对提升的量）")
        r=input()
        r=abs(float(r)/100)
        zpower = NormalIndPower()
        effect_size =u*r/np.sqrt(u*(1-u))
        res=(zpower.solve_power(
           effect_size=effect_size,
           nobs1=None,
           alpha=0.05,
           power=0.8,
           ratio=1.0,
           alternative='two-sided'
                ))
        print("计算中……,计算结果如下")
        time.sleep(3)
        print('******* 您的AB实验，实验组需要的用户量为：{0}人 ******'.format(int(res)))
        
    def rank_wilson_score(pos, total, p_z=1.96):
        """
        威尔逊得分计算函数
        :param pos: 正例数
        :param total: 总数
        :param p_z: 正太分布的分位数
        :return: 威尔逊得分
        """
        pos_rat = pos/ total  # 正例比率
        score = (pos_rat + (np.square(p_z) / (2* total)) - ((p_z / (2* total)) * np.sqrt(4 * total * (1 - pos_rat) * pos_rat + np.square(p_z)))) / \
        (1 + np.square(p_z) / total)
        return score
            