# from operator import le
# from pickle import PROTO
# import re
import numpy as np
# from numpy.lib.npyio import loadtxt
# from numpy.testing._private.utils import build_err_msg
from sklearn.preprocessing import MinMaxScaler
# from scipy import linalg

def rs_hdmr(samplex,sampley):
    #输入：X，y为设计参数和对应响应值
    #输出：输出1.从大到小排序后的敏感性系数以及对应耦合变量的索引；2.累加敏感性系数

    M=3
    tempx=samplex
    rf=sampley
    y0=rf.reshape((-1,1))
    numb_x=int(np.shape(tempx)[0])
    numb_variables=int(np.shape(tempx)[1])

    #normalization
    mm=MinMaxScaler()
    x=mm.fit_transform(tempx)

    # construction of orthonormal polynomials
    p=np.mat(np.zeros([numb_variables,6]))
    f1=np.mat(np.zeros([1,numb_variables]))
    f2=np.mat(np.zeros([1,numb_variables]))
    f3=np.mat(np.zeros([1,numb_variables]))
    dd=np.mat(np.zeros([1,numb_variables]))
    d1=np.mat(np.zeros([1,numb_variables]))
    d2=np.mat(np.zeros([1,numb_variables]))
    d3=np.mat(np.zeros([1,numb_variables]))
    c3=np.mat(np.zeros([1,numb_variables]))
    c1=np.mat(np.zeros([numb_variables,9]))
    for i in range(numb_variables):
        for j in range(6):
            for k in range(numb_x):
                p[i,j]=p[i,j]+np.power(x[k,i],(j+1))
            p[i,j]=p[i,j]/numb_x     

    for i in range (numb_variables):
        f1[0,i]=np.sqrt((p[i,3]-np.power(p[i,1],2))*(p[i,1]-np.power(p[i,0],2))-np.power((p[i,2]-p[i,0]*p[i,1]),2))
        f2[0,i]=np.sqrt(p[i,1]-np.power(p[i,0],2))
        f3[0,i]=p[i,2]-p[i,0]*p[i,1]
        dd[0,i]=(p[i,1]*p[i,3]-np.square(p[i,2]))-p[i,0]*(p[i,0]*p[i,3]-p[i,1]*p[i,2])+p[i,1]*(p[i,0]*p[i,2]-np.square(p[i,1]))
        d1[0,i]=(-p[i,2]*(p[i,1]*p[i,3]-np.square(p[i,2]))+p[i,3]*(p[i,0]*p[i,3]-p[i,1]*p[i,2])-p[i,4]*(p[i,0]*p[i,2]-np.square(p[i,1])))/dd[0,i]               
        d2[0,i]=(p[i,2]*(p[i,0]*p[i,3]-p[i,1]*p[i,2])-p[i,3]*(p[i,3]-np.square(p[i,1]))+p[i,4]*(p[i,2]-p[i,0]*p[i,1]))/dd[0,i]
        d3[0,i]=(-p[i,2]*(p[i,0]*p[i,2]-np.square(p[i,1]))+p[i,3]*(p[i,2]-p[i,0]*p[i,1])-p[i,4]*(p[i,1]-np.square(p[i,0])))/dd[0,i]
        c3[0,i]=np.sqrt(p[i,2]*d1[0,i]+p[i,3]*d2[0,i]+p[i,4]*d3[0,i]+p[i,5])

    for i in range(numb_variables):
        c1[i,0]=-p[i,0]/f2[0,i]
        c1[i,1]=1/f2[0,i]
        c1[i,2]=p[i,0]*f3[0,i]/(f1[0,i]*f2[0,i])-p[i,1]*f2[0,i]/f1[0,i]
        c1[i,3]=-f3[0,i]/(f1[0,i]*f2[0,i])
        c1[i,4]=f2[0,i]/f1[0,i]
        c1[i,8]=1/c3[0,i]
        c1[i,5]=d1[0,i]*c1[i,8]
        c1[i,6]=d2[0,i]*c1[i,8]
        c1[i,7]=d3[0,i]*c1[i,8]

    # Examine the orthogonality
    p1=np.zeros([numb_variables,3])
    p2=np.zeros([numb_variables,3])  
    pq=np.zeros([numb_variables,3])
    phi=np.zeros([numb_variables,3])
    
    for nd in range(numb_x):
        
        x1=np.zeros([1,numb_variables])
        for i in range(numb_variables):
            x1[0,i]=x[nd,i]
        
        for i in range(numb_variables):
            xx=x1[0,i]
            phi[i,0]=c1[i,1]*xx+c1[i,0]
            phi[i,1]=(c1[i,4]*xx+c1[i,3])*xx+c1[i,2]
            phi[i,2]=((c1[i,8]*xx+c1[i,7])*xx+c1[i,6])*xx+c1[i,5]     
        
        for i in range(numb_variables):
            for j in range(3):
                p1[i,j]=p1[i,j]+phi[i,j]
                p2[i,j]=p2[i,j]+phi[i,j]**2
                
        for i in range(numb_variables):
            ii=0
            for j in range(2):
                for k in range(j+1,3):
                    ii=ii+1
                    pq[i,ii-1]=pq[i,ii-1]+phi[i,j]*phi[i,k]
    p1=p1/numb_x
    p2=p2/numb_x
    pq=pq/numb_x
    # coefficient matrix
    numb_2nd=2*M+np.square(M)
    numb_tot1st=int(numb_variables*M)
    numb_tot2nd=int((numb_variables*(numb_variables-1)/2)*numb_2nd)
    numb_tot=numb_tot1st+numb_tot2nd

    coefmatrix=np.mat(np.zeros([numb_x,numb_tot]))#H矩阵  所有系数
    y_train=np.mat(np.zeros([numb_x,1]))
    f0=np.mean(y0[:,0])

    for nd in range(numb_x):
        x_=np.mat(np.zeros([1,numb_variables]))
        for i in range(numb_variables):
            x_[0,i]=x[nd,i]
        for i in range(numb_variables):
            xx=x_[0,i]
            phi[i,0]=c1[i,1]*xx+c1[i,0]
            phi[i,1]=(c1[i,4]*xx+c1[i,3])*xx+c1[i,2]
            phi[i,2]=((c1[i,8]*xx+c1[i,7])*xx+c1[i,6])*xx+c1[i,5]
        
        kk=0
        for i in range(numb_variables):
            for j in range(M):
                coefmatrix[nd,kk]=phi[i,j]
                kk=kk+1
        for i in range(numb_variables-1):
            for j in range(i+1,numb_variables):
                for i1 in range(M):
                    coefmatrix[nd,kk]=phi[i,i1]
                    kk=kk+1
                for i2 in range(M):
                    coefmatrix[nd,kk]=phi[j,i2]
                    kk=kk+1
                for i3 in range(M):
                    for i4 in range(M):   
                        coefmatrix[nd,kk]=phi[i,i3]*phi[j,i4]
                        kk=kk+1


        y_train[nd,0]=y0[nd,0]-f0
    
    #cost matrix
    c0=np.mat(np.sum(coefmatrix,axis=0)/numb_x)
    cc=(coefmatrix.T).dot(coefmatrix)/numb_x  #层次正交性
    
    kk=0
    c2=np.zeros([int(numb_variables*(numb_variables-1)/2),2*M+1,numb_2nd])
    c2t=np.zeros([int((numb_variables*(numb_variables-1)/2)),numb_2nd,numb_2nd])

    for i in range(numb_variables-1):
        for j in range(i+1,numb_variables):
            for iii in range (numb_2nd):
                c2[kk,0,iii]=c0[0,numb_tot1st+(kk)*numb_2nd+iii]
            for k in range(2*M):
                for iii in range (numb_2nd):
                    c2[kk,k+1,iii]=cc[numb_tot1st+(kk)*numb_2nd+k,numb_tot1st+(kk)*numb_2nd+iii]
            c2t[kk,:,:]=(c2[kk,:,:].T).dot(c2[kk,:,:])
            kk=kk+1
    
    B=np.mat(np.zeros([numb_tot,numb_tot]))
    
    for kk in range(int(numb_variables*(numb_variables-1)/2)):
        B[numb_tot1st+kk*numb_2nd:numb_tot1st+(kk+1)*numb_2nd,numb_tot1st+kk*numb_2nd:numb_tot1st+(kk+1)*numb_2nd]=c2t[kk,:,:]
    
    A_=cc
    A=np.mat(A_[numb_tot1st:-1,:])
    d_=(coefmatrix.T).dot(y_train)/numb_x
    d=np.mat(d_[numb_tot1st:-1,:])
    Apinv=np.linalg.pinv(A)
    w0=Apinv.dot(d)
    Ia=np.eye(numb_tot,numb_tot)
    Pr=Ia-(Apinv.dot(A))
    PB=Pr.dot(B)    
    U_,S,Vt=np.linalg.svd(PB)
    V_=Vt.T

    Is=1
    sdd=np.zeros([1,numb_tot])
    sdd[0]=0
    sd=0

    for i in range(1,numb_tot):
        sdd[0,i]=(S[i-1]-S[i])/S[i]
        if (sdd[0,i]>sd and S[i]!=0):
            sd=sdd[0,i]
            Is=i
    U=np.mat(U_[:,Is:])
    V=np.mat(V_[:,Is:])
    UV=(U.T).dot(V)
    UVinv=np.linalg.inv(UV)
    Q=V.dot(UVinv).dot(U.T)
    w=Q.dot(w0)

    zz=0
    Va=np.mat(np.zeros([numb_variables,numb_variables]))
    # 一阶方差
    for i in range(numb_variables):
        Va[i,i]=0
        for j in range(M):
            Va[i,i]=Va[i,i]+np.power(w[zz,0],2)
            zz=zz+1
    # 二阶方差
    for i in range(numb_variables-1):
        for j in range(i+1,numb_variables):
            Va[i,j]=0
            for i1 in range(M):
                Va[i,j]=Va[i,j]+np.power(w[zz,0],2)
                zz=zz+1
            for i1 in range(M):
                Va[i,j]=Va[i,j]+np.power(w[zz,0],2)
                zz=zz+1
            for i1 in range(M):
                for i2 in range(M):
                    Va[i,j]=Va[i,j]+np.power(w[zz,0],2)
                    zz=zz+1    
    #总方差
    Vall=0
    for i in range(numb_variables):
        Vall=Vall+Va[i,i]
    for i in range(numb_variables-1):
        for j in range(i+1,numb_variables):
            Vall=Vall+Va[i,j]
    #一阶敏感性系数
    Sa=np.zeros([numb_variables,numb_variables])
    for i in range(numb_variables):
        Sa[i,i]=Va[i,i]/Vall
    for i in range(numb_variables-1):
        for j in range(i+1,numb_variables):
            Sa[i,j]=Va[i,j]/Vall
    Sa_=np.copy(Sa)
    Sa[Sa==0]=float('nan')
    
    #各变量敏感性系数之和
    SI=np.zeros(numb_variables)
    for i in range (numb_variables):
        SI[i]=np.sum(Sa_[i,:])+np.sum(Sa_[:,i])-Sa_[i,i]
    
    #排序结果显示

    Sa_list=np.zeros(int(numb_variables*(numb_variables-1)/2+numb_variables))
    index=np.zeros([int(numb_variables*(numb_variables-1)/2+numb_variables),2])
    aa=0
    for i in range(numb_variables):
        Sa_list[aa]=Sa_[i,i]
        index[aa,0]=i+1
        index[aa,1]=i+1
        aa=aa+1
    for i in range(numb_variables-1):
        for j in range(i+1,numb_variables):
            Sa_list[aa]=Sa_[i,j]
            index[aa,0]=i+1
            index[aa,1]=j+1
            aa=aa+1
    
    Sa_list_sort=abs(np.sort(-1*Sa_list))
    Sa_sort_index=np.argsort(-1*Sa_list)
    Sa_sort=np.zeros([int(numb_variables*(numb_variables-1)/2+numb_variables),3])  

    for i in range(int(numb_variables*(numb_variables-1)/2+numb_variables)):
        Sa_sort[i,0]=Sa_list_sort[i]
        Sa_sort[i,1]=index[Sa_sort_index[i],0]
        Sa_sort[i,2]=index[Sa_sort_index[i],1]
        
    return Sa_sort, SI, Sa