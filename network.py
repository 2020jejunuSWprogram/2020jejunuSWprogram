import tensorflow as tf
import numpy as np

classes={0:'swirl', 1:'heart', 2:'horizontal', 3:'vertical', 4:'up', 5:'left',6:'down',7:'right'}
data_set=[]
for i in range(6):
    f=open('class_'+classes[i]+'.txt','r')
    lines=f.readlines()
    for line in lines:
        temp=line.split(',')
        if len(temp)==1025:
            data_set.append(list(map(float,temp[:-1]))+[i])
            if i==4:
                temp2=np.array(temp[:-1]).reshape((32,32))
                temp3=np.zeros((32,32))
                for ii in range(32):
                    temp3[i,:]=temp2[31-i,:]
                temp3=temp3.flatten().tolist()
                data_set.append(list(map(float,temp3))+[6])
            elif i==5:
                temp2=np.array(temp[:-1]).reshape((32,32))
                temp3=np.zeros((32,32))
                for ii in range(32):
                    temp3[:,i]=temp2[:,31-i]
                temp3=temp3.flatten().tolist()
                data_set.append(list(map(float,temp3))+[7])

data_cnt=len(data_set)
data_set=np.array(data_set)
np.random.shuffle(data_set)
rate=0.8
train_X,test_X,train_Y,test_Y=data_set[:int(rate*data_cnt),:-1],data_set[int(rate*data_cnt):,:-1],data_set[:int(rate*data_cnt),-1],data_set[int(rate*data_cnt):,-1]
train_Y = tf.keras.utils.to_categorical(train_Y, num_classes = 8)
test_Y = tf.keras.utils.to_categorical(test_Y, num_classes = 8)

model = tf.keras.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(1024,)))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(8, activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model.fit(train_X, train_Y, epochs=15)

model.evaluate(test_X, test_Y)
    