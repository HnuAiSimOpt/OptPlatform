from SALib.analyze import morris 
import numpy as np
# Morris算法。
#输入：x,y 
#输出：各参数敏感系数，值越大敏感性越大；
#为了保证程序能够正常运行，请用户输入不少于(D*D+1)个训练样本点的数据，D为训练样本的维度值。


# Define the model inputs
def morris_model(x,y):
    num_vars=np.shape(x)[1]
    num_x=np.shape(x)[0]
    _x=[]
    _y=[]
    index_i=np.random.choice(num_x,size=(num_vars*(num_vars+1)),replace=False)
    for i in index_i:
        _x.append(x[i])
        _y.append(y[i])
        
    input_x=np.array(_x)
    input_y=np.array(_y)

    names=[]
    bound=[]
    for i in range(num_vars):
        names.append("V" +str(i+1))
    for i in range(num_vars):
        upperbound=np.max(input_x[:,i])
        lowerbound=np.min(input_x[:,i])
        bound.append([lowerbound,upperbound])

    problem = {
    'num_vars': num_vars,
    'names': names,
    'bounds': bound
    }
    # =========================================================
    # print(input_x)
    # print('|||||||||||||||||||||||||||||||||||||||')
    # print(input_y)
    Si = morris.analyze(problem, input_x, input_y, conf_level=0.95,
                        print_to_console=True, num_levels=4)
    S_name=Si['names']
    S_value=abs(Si['mu'])
    S_resort=abs(np.sort(-1*S_value))
    S_sort_index=np.argsort(-1*S_value)
    Si_sort=[]
    S_V=[]
    S_i=[]
    si = []
    for i in range (num_vars):
        value=S_resort[i]
        v_name='V'+str(S_sort_index[i]+1)
        S_V.append(value)
        S_i.append(v_name)
    Si_sort.append([S_i,S_V])

        
    return Si_sort, S_value, [S_name, list(S_value)]