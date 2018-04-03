# -*- coding: utf-8 -*-
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from userApp import userApp, db
from userApp.dbc import Picture, Cnnrec
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import glob, os

# Каталог с данными для тестирования
test_dir = userApp.config.get('DATA_PATH')
# Размеры изображения
img_width, img_height = 150, 150
# Размер мини-выборки
batch_size = 16
# Количество изображений для тестирования
nb_test_samples = 100

print("Загружаю сеть из файлов")
# Загружаем данные об архитектуре сети из файла json
json_file = open("norma_bolnoe/mnist_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
# Создаем модель на основе загруженных данных
loaded_model = model_from_json(loaded_model_json)
# Загружаем веса в модель
loaded_model.load_weights("norma_bolnoe/mnist_model.h5py")
print("Загрузка сети завершена")

# Компилируем модель
loaded_model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

c = 0
d = 0

all_pics = db.session.query(Picture.Picture).all()
print str(len(all_pics))


for pic in all_pics:
    exists_pic = db.session.query(Cnnrec.Cnnrec.id).filter(Cnnrec.Cnnrec.pic_id == pic.id, Cnnrec.Cnnrec.symp_id == 20).all()
    if(len(exists_pic) > 0):
        img = image.load_img(path=test_dir +"/"+ pic.pic_name,target_size=(150,150,3))
        img = image.img_to_array(img)
        test_img = np.expand_dims(img, axis=0)
        img_class = loaded_model.predict_classes(test_img)
        classname = img_class[0]
        cnn = Cnnrec.Cnnrec()
        cnn.pic_id = pic.id
        #Больное
        if(classname < 0.5):
            # cnn.symp_id = 22
            c+=1
        #Норма
        if (classname > 0.5):
            cnn.symp_id = 27
            d+=1
            db.session.add(cnn)
        if((d+c)%100==0):
            print ("_Больное: " + str(c))
            print ("_Норма: " + str(d))

db.session.commit()
print ("Больное: "+str(c))
print ("Норма: "+str(d))


# plt.imshow(img)
# plt.title(classname)
# plt.show()