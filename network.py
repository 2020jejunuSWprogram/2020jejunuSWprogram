import tensorflow as tf
import numpy as np

classes={0:'swirl', 1:'heart', 2:'horizontal', 3:'vertical'}
data_set=[]
for i in range(4):
    f=open('class_'+classes[i]+'.txt','r')
    lines=f.readlines()
    for line in lines:
        temp=line.split(',')
        if len(temp)==1025:
            data_set.append(list(map(float,temp[:-1]))+[i])

data_cnt=len(data_set)
data_set=np.array(data_set)
np.random.shuffle(data_set)
rate=0.8
train_X,test_X,train_Y,test_Y=data_set[:int(rate*data_cnt),:-1],data_set[int(rate*data_cnt):,:-1],data_set[:int(rate*data_cnt),-1],data_set[int(rate*data_cnt):,-1]
train_Y = tf.keras.utils.to_categorical(train_Y, num_classes = 4)
test_Y = tf.keras.utils.to_categorical(test_Y, num_classes = 4)

model = tf.keras.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(1024,)))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(4, activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model.fit(train_X, train_Y, epochs=5)

model.evaluate(test_X, test_Y)
    