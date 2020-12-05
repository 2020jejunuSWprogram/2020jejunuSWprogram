import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

class Network:
    def __init__(self):
        self.classes = {0:'swirl', 1:'heart', 2:'horizontal', 3:'vertical', 4:'up', 5:'left',6:'down',7:'right'}
        self.data_set = []
        self.data_cnt = 0
        self.rate = 0.8
    def read_data(self):
        for i in range(6):
            f=open('class_'+self.classes[i]+'.txt','r')
            lines=f.readlines()
            for line in lines:
                temp=line.split(',')
                if len(temp)==1025:
                    self.data_set.append(list(map(float,temp[:-1]))+[i])
                    if i==4:
                        temp2=np.array(temp[:-1]).reshape((32,32))
                        temp3=np.zeros((32,32))
                        for ii in range(32):
                            temp3[ii,:]=temp2[31-ii,:]
                        temp3=temp3.flatten().tolist()
                        self.data_set.append(list(map(float,temp3))+[6])
                    elif i==5:
                        temp2=np.array(temp[:-1]).reshape((32,32))
                        temp3=np.zeros((32,32))
                        for ii in range(32):
                            temp3[:,ii]=temp2[:,31-ii]
                        temp3=temp3.flatten().tolist()
                        self.data_set.append(list(map(float,temp3))+[7])
            f.close()
        
        self.data_set=np.array(self.data_set)
        self.data_cnt = len(self.data_set)
        X_data_set=self.data_set[:,:-1].reshape(self.data_cnt,32,32,1)
        Y_data_set=self.data_set[:,-1]
        Y_data_set=tf.keras.utils.to_categorical(Y_data_set, num_classes = 8)
        sorted_data_set=np.zeros((self.data_cnt,32,32,1))
        for data_num in range(self.data_cnt):
            up=33
            down=0
            for i in range(32):
                flag=False
                for j in range(32):
                    if X_data_set[data_num,i,j,0]!=0:
                        down=max(down,j)
                        if not flag:
                            flag=True
                            up=min(up,j)

            left=33
            right=0
            for i in range(32):
                flag=False
                for j in range(32):
                    if X_data_set[data_num,j,i,0]!=0:
                        right=max(right,j)
                        if not flag:
                            flag=True
                            left=min(left,j)
            
            if up==33 or down==0 or left==33 or right==0:
                continue

            temp=X_data_set[data_num,left:right,up:down,0]
            temp=np.pad(temp,(((32-right+left)//2,32-(right-left)-(32-right+left)//2),((32-down+up)//2,32-(down-up)-(32-down+up)//2)),'constant',constant_values=0)

            sorted_data_set[data_num,:,:,0]=temp
        
        self.data_set = sorted_data_set
        self.rate=0.8
        train_X,test_X=X_data_set[:int(self.rate*self.data_cnt)],X_data_set[int(self.rate*self.data_cnt):]
        train_Y,test_Y=Y_data_set[:int(self.rate*self.data_cnt)],Y_data_set[int(self.rate*self.data_cnt):]

        return train_X, train_Y, test_X, test_Y
    def gen_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Conv2D(32,(3,3),activation='relu', input_shape=(32,32,1)))
        model.add(tf.keras.layers.MaxPooling2D((2,2)))
        model.add(tf.keras.layers.Conv2D(64,(3,3),activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2,2)))
        model.add(tf.keras.layers.Conv2D(64,(3,3),activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2,2)))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(8, activation='softmax'))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['mae'])
        return model

    def fit(self, model, train_X, train_Y, test_X, test_Y):
        history = model.fit(train_X, train_Y, epochs=10)
        model.evaluate(test_X, test_Y)
        model.save('network.h5')
        return model, history


network = Network()
# model=tf.keras.models.load_model('network.h5')
model=network.gen_model()
train_X, train_Y, test_X, test_Y=network.read_data()
model, history=network.fit(model,train_X, train_Y, test_X, test_Y)
# model.summary()

plt.plot(history.history['acc'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train'], loc='upper left')
plt.show()