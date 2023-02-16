import numpy as np


seed = 0


def load_dataset1():
    np.random.seed(seed)


    #dataset 1: simple 2 class, 
    #6  features, but only the last has non-zero values in
    
    n = 150
    numTr= 100
    
    numFeatures=6
    data1 = np.zeros((n,numFeatures))
    labels1 = np.zeros(n,dtype=int)
    keyFeature = numFeatures - 1

    
    for i in range(n):
        data1[i][keyFeature] = 5 +np.random.normal()
        if (data1[i][keyFeature] <5 ) :
            labels1[i] = 1
        else:
            labels1[i]=0

    train1_X= data1[0:numTr,:]
    train1_y= labels1[0:numTr]
    test1_X= data1[numTr:,:]
    test1_y= labels1[numTr:]       
    return train1_X,train1_y,test1_X,test1_y


def load_dataset2():
    # dataset 2: 3 classes, first linearly seperable from other two, 
    #other two are once the cases from class 0 are removed 
    # relevant feature are 2nd and 3rd, all others are pure noise from U(0,100)
    np.random.seed(seed)

    
    numSamplesPerClass= 50
    n = numSamplesPerClass*3
    nTr = numSamplesPerClass*2
    numFeatures=6
    data2 = np.random.rand(3*numSamplesPerClass,numFeatures+1)*20 #  one for label 


    #make the data in triples
    #starting by providing points at the bounding box edges so
    # I know min and max x-y values are present in the training set

    # region labelled 0 covers x 6-8, y1-5 
    data2[0][1] , data2[0][2], data2[0][numFeatures] = 6,1,0
    data2[1][1], data2[1][2], data2[1][numFeatures] = 8,5,0
    # region labelled 1 covers x 1-5, y0-2
    data2[2][1], data2[2][2], data2[2][numFeatures] = 1,0,1
    data2[3][1], data2[3][2], data2[3][numFeatures] = 5,2,1
    # region labelled 2 covers x 1-5, y3-5
    data2[4][1], data2[4][2], data2[4][numFeatures] = 1,3,2
    data2[5][1], data2[5][2], data2[5][numFeatures] = 5,5,2

    #print(data2[:6, :])
    
    # now random points in this box for the other 144 instances
    for i in range ( 6,3*(numSamplesPerClass ),3):
        # region labelled 0 covers x 6-8, y1-5 
        data2[i][1], data2[i][2], data2[i][numFeatures] = 6 +np.random.random()*2,1 + np.random.random()*4,0
        # region labelled 1 covers x 1-5, y0-2
        data2[i+1][1], data2[i+1][2], data2[i+1][numFeatures] = 1 +np.random.random()*4, np.random.random()*2, 1
        # region labelled 2 covers x 1-5, y3-5
        data2[i+2][1], data2[i+2][2], data2[i+2][numFeatures] = 1 +np.random.random()*4, 3 + np.random.random()*2, 2
 

    #splt data into train & test, shuffle rows
    train= data2[0:nTr,:]
    test = data2[nTr:,:]
    #shuffle rows
    np.random.shuffle(train)
    np.random.shuffle(test)
    #split into X and y
    train2_X= train[: , :numFeatures]
    train2_y= train[: , numFeatures].astype(int)
    test2_X=   test[: , :numFeatures]
    test2_y=   test[: , numFeatures].astype(int)
    
    

    return(train2_X,train2_y,test2_X,test2_y)


def load_dataset3():
    #dataset 3: simple 2 class, 
    #6  features with uniformly distributed values,
    # only 1 randomly chosen feature is important

    np.random.seed(seed)
    n = 200
    nTr=100
    numFeatures=6

    #. populate data arrays from U(0,100) to start with
    data3 = np.random.rand(n,numFeatures) *20
    labels3 = np.zeros(n,dtype=int)

    #make sure we have one value near the threshold
    for feat in range(numFeatures):
        data3[0][feat] = 5.00

    #select random feature to be key
    keyFeature =  0 # np.random.randint(numFeatures) 

    # then apply a simple 2-class one features labelling scheme
    for i in range(n):
        if (data3[i][keyFeature]) <5.000 :
            labels3[i] = 1
        else:
            labels3[i]=0

    train3_X= data3[0:nTr,:]
    train3_y= labels3[0:nTr]
    test3_X= data3[nTr:,:]
    test3_y= labels3[nTr:]
    
    return( train3_X,train3_y,test3_X,test3_y)


def load_dataset4():
    #dataset 4: simple 2 class, 
    #6  features with gaussian distributed values,
    #  2 randomly chosen feature are important 
    #decision boundary is based on their product

    np.random.seed(seed)
    n = 200
    nTr=150
    numFeatures=6

    #. populate data arrays from  5 +N(0,2.5) to start with
    data4 = np.random.normal(loc=5,scale=2.5,size=(n,numFeatures))
    labels4 = np.zeros(n,dtype=int)

    #make sure we have one value near the threshold
    for feat in range(numFeatures):
        data4[0][feat] = 5.00

    #select random feature to be key
    keyFeature =  0 
    keyFeature2 =  1+ np.random.randint(numFeatures-1) 

    # then apply a simple 2-class one features labelling scheme
    for i in range(n):
        product = data4[i][keyFeature] * data4[i][keyFeature2]
        if product <25.000 :
            labels4[i] = 1
        else:
            labels4[i]=0

    train4_X= data4[0:nTr,:]
    train4_y= labels4[0:nTr]
    test4_X= data4[nTr:,:]
    test4_y= labels4[nTr:]
    
    return( train4_X,train4_y,test4_X,test4_y)



def load_dataset5():
    #dataset 5: simple 3 class, 
    #6  features with gaussian distributed values,
    #  3 randomly chosen feature are important 
    #decision boundary is based on their division

    np.random.seed(seed)
    n = 150
    nTr=100
    numFeatures=6

    #. populate data arrays from  5 +N(0,2.5) to start with
    data5 = np.random.normal(loc=5,scale=2.5,size=(n,numFeatures))
    labels5 = np.zeros(n,dtype=int)
    #make sure we have one value near the threshold
    for feat in range(numFeatures):
        data5[0][feat] = 5.00

    #select random feature to be key
    keyFeature =  0 
    keyFeature2 =  1+ np.random.randint(numFeatures-1) 
    keyFeature3 =  1+ np.random.randint(numFeatures-1) 

    # then apply a simple 2-class one features labelling scheme
    for i in range(n):
        a = data5[i][keyFeature]
        b = data5[i][keyFeature2]
        diff = a-b
        if abs(b)>0:
            product = (a-b)*(a-b)
        if data5[i][keyFeature] * data5[i][keyFeature2] * data5[i][keyFeature3]  >100.00:
            labels5[i] = 1
        else:
            labels5[i]=0

    train5_X= data5[0:nTr,:]
    train5_y= labels5[0:nTr]
    test5_X= data5[nTr:,:]
    test5_y= labels5[nTr:]
    print(np.unique(labels5, return_counts=True))
    return( train5_X,train5_y,test5_X,test5_y)



def load_dataset5old():
    #dataset 5: simple 3 class, 
    #6  features with gaussian distributed values,
    #  3 randomly chosen feature are important 
    #decision boundary is based on their division

    np.random.seed(seed)
    n = 200
    nTr=150
    numFeatures=5

    #. populate data arrays from  5 +N(0,2.5) to start with
    data5 = np.random.normal(loc=5,scale=2.5,size=(n,numFeatures))
    labels5 = np.zeros(n,dtype=int)
    #make sure we have one value near the threshold
    for feat in range(numFeatures):
        data5[0][feat] = 5.00

    #select random feature to be key
    keyFeature =  0 
    keyFeature2 =  1+ np.random.randint(numFeatures-1) 
    keyFeature3 =  1+ np.random.randint(numFeatures-1) 

    # then apply a simple 2-class one features labelling scheme
    for i in range(n):
        a = data5[i][keyFeature]
        b = data5[i][keyFeature2]
        diff = a-b
        if abs(b)>0:
            product = (a-b)*(a-b)
        if diff*diff <3.5 :
            labels5[i] = 1
        #elif diff*diff <5:
        #    labels5[i]=2
        else:
            labels5[i]=0

    train5_X= data5[0:nTr,:]
    train5_y= labels5[0:nTr]
    test5_X= data5[nTr:,:]
    test5_y= labels5[nTr:]
    print(np.unique(labels5, return_counts=True))
    return( train5_X,train5_y,test5_X,test5_y)