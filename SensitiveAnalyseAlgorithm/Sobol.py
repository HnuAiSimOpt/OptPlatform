from pickle import PROTO
from numpy import random
from SALib.analyze import sobol 
import numpy as np
# Sobol算法。
#输入：x,y 
#输出：各参数敏感系数，值越大敏感性越大；
#为了保证程序能够正常运行，请用户输入不少于(2*D+2)个训练样本点的数据，D为训练样本的维度值。
#Warning:用户采用蒙特卡洛采样之后输入的数据，才能得到较为准确的结果;
#由于蒙特卡洛采样具有随机性，每次得到的结果并不相同，建议用户按照一阶参数从大到小选择

# Define the model inputs
def sobol_model(x,y):
    y_=y.flatten()
    num_vars=np.shape(x)[1]
    num_x=np.shape(x)[0]
    n=int(num_x/(2*num_vars+2))

    _x=[]
    _y=[]
    index_i=np.random.choice(num_x,size=(n*2*(num_vars+1)),replace=False)
    for i in index_i:
        _x.append(x[i])
        _y.append(y_[i])
        
    input_x=np.array(_x)
    input_y=np.array(_y)
    names=[]
    bound=[]
    for i in range(num_vars):
        names.append("V-" +str(i+1))
    for i in range(num_vars):
        upperbound=np.max(input_x[:,i])
        lowerbound=np.min(input_x[:,i])
        bound.append([lowerbound,upperbound])

    problem = {
    'num_vars': num_vars,
    'names': names,
    'bounds': bound
    }

    Si=sobol.analyze(problem,input_y,print_to_console=False)
    SI=list(Si['ST_conf'])
    Sa1=abs(Si['S2'])
    S1=abs(Si['S1'])
    for i in range (num_vars):
        Sa1[i,i]=S1[i]

    Sa_list=np.zeros(int(num_vars*(num_vars-1)/2+num_vars))
    index=np.zeros([int(num_vars*(num_vars-1)/2+num_vars),2])
    aa=0
    for i in range(num_vars):
        Sa_list[aa]=Sa1[i,i]
        index[aa,0]=i+1
        index[aa,1]=i+1
        aa=aa+1
    for i in range(num_vars-1):
        for j in range(i+1,num_vars):
            Sa_list[aa]=Sa1[i,j]
            index[aa,0]=i+1
            index[aa,1]=j+1
            aa=aa+1
    
    Sa_list_sort=abs(np.sort(-1*Sa_list))
    Sa_sort_index=np.argsort(-1*Sa_list)
    Sa_sort=np.zeros([int(num_vars*(num_vars-1)/2+num_vars),3])  

    for i in range(int(num_vars*(num_vars-1)/2+num_vars)):
        Sa_sort[i,0]=Sa_list_sort[i]
        Sa_sort[i,1]=index[Sa_sort_index[i],0]
        Sa_sort[i,2]=index[Sa_sort_index[i],1]
    
    Sa_mat=np.mat(Sa1)
    Sa_mat_t=Sa_mat.T
    Sa=Sa_mat
    Sa_sort_=Sa_sort
    
    return  Sa_sort_,SI,Sa