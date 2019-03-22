import pandas as pd
from keras.utils.np_utils import to_categorical 
from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D
from keras import optimizers
from keras.preprocessing import image
import cv2
import os
import image_filters

save_model = True

def read_files(path):
    first=True
    images=[]
    outs=[]
    for i in os.listdir(path):
        if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg'):
            img=cv2.imread(path+"/"+i,0)
            img=cv2.resize(img,(28,9))
            img = image_filters.focus_filter(img,0.5,2)   
            #img = image_filters.sobel_y(img)
            img=pd.DataFrame(data=img)
            img=img.values.reshape(1,252)
            img=pd.DataFrame(data=img)
            outs.append(int(i[0]))
            if first:
                first=False
                images=img
            else:
                images=pd.concat([images,img])
    return (images,outs)

def mean(lists):
    new_list=[]
    for i in lists:
        new_list.append(float(sum(i)) / max(len(i), 1))
    return new_list

if save_model:
    '''
    train=pd.read_csv("train.csv")
    test=pd.read_csv("test.csv")
    x_train=train.drop(["label"],axis=1)
    y_train=pd.DataFrame(train["label"])
    '''
    x_train,y_train=read_files("train2")
    
    x_train/=255.0
    x_train=x_train.values.reshape(-1,28,9,1)
    y_train=to_categorical(y_train,num_classes=8)
    
    x_train,x_test,y_train,y_test=train_test_split(x_train,y_train,\
                                    test_size=0.1,random_state=2)
    
    model=Sequential()
    
    model.add(Conv2D(filters = 8, kernel_size = (5,5),padding = 'Same',\
                     activation ='relu', input_shape = (28,9,1)))
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(filters = 8, kernel_size = (3,3),padding = 'Same',\
                     activation ='relu'))
    model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    
    model.add(Dense(128, activation = "relu"))
    model.add(Dropout(0.1))
    model.add(Dense(256, activation = "relu"))
    model.add(Dropout(0.1))
    model.add(Dense(128, activation = "relu"))
    model.add(Dropout(0.1))
    model.add(Dense(64, activation = "relu"))
    model.add(Dropout(0.25))
    model.add(Dense(32, activation = "relu"))
    model.add(Dropout(0.25))
    model.add(Dense(8, activation = "softmax"))
    
    optimizer = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
    
    model.compile(optimizer=optimizer,loss="categorical_crossentropy",\
                  metrics=["accuracy"])
    
    # data augmentation
    datagen = image.ImageDataGenerator(rotation_range=0.5,
            zoom_range = 0.5,
            width_shift_range=0.5,
            height_shift_range=0.5)
    
    datagen.fit(x_train)
    
    batch_size=1000
    model.fit_generator(datagen.flow(x_train,y_train, batch_size=batch_size),
                                  epochs= 5000,validation_data = (x_test,y_test),\
                                  steps_per_epoch=x_train.shape[0] / batch_size)
    model.save("model.h5")
    
else:
    model = load_model("model.h5")

class Detect():
    def __init__(self):
        self.model = load_model("model.h5")
    def set_img(self,img):
        img=cv2.resize(img,(28,9))
        img=pd.DataFrame(data=img)
        img=img.values.reshape(1,252)
        img=pd.DataFrame(data=img)
        test = img
        test/=255.0
        test=test.values.reshape(-1,28,9,1)
        pred = self.model.predict_classes(test)
        return pred
