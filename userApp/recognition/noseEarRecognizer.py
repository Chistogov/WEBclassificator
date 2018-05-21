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
json_file = open("E_N_T/mnist_model92.json", "r")
loaded_model_json = json_file.read()
json_file.close()
# Создаем модель на основе загруженных данных
loaded_model = model_from_json(loaded_model_json)
# Загружаем веса в модель
loaded_model.load_weights("E_N_T/mnist_model92.h5py")
print("Загрузка сети завершена")

# Компилируем модель
loaded_model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

c = 0
d = 0
l = 0

recognized_pics = db.session.query(Cnnrec.Cnnrec.pic_id)
all_pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.notin_(recognized_pics)).all()
print str(len(all_pics))


for pic in all_pics:
    img = image.load_img(path=test_dir +"/"+ pic.pic_name,target_size=(150,150,3))
    img = image.img_to_array(img)
    test_img = np.expand_dims(img, axis=0)
    datagen = ImageDataGenerator(rescale=1. / 255)
    pred_0 = loaded_model.predict_generator(
        datagen.flow(test_img, batch_size=50),
        steps=(len(test_img) // 50) + 1,
        workers=1,
        use_multiprocessing=True
    )
    predicted = np.argmax(pred_0, axis=-1)
    # print (pred_0)
    cnn = Cnnrec.Cnnrec()
    cnn.pic_id = pic.id
    #Горло
    if(predicted == 0):
        cnn.symp_id = 21
        c+=1
    #Нос
    if (predicted == 1):
        cnn.symp_id = 22
        d+=1
    #Ухо
    if (predicted == 2):
        cnn.symp_id = 20
        l += 1
    db.session.add(cnn)
    if(d%1000==0):
        db.session.commit()
        print ("Нос: " + str(d))
        print ("Ухо: " + str(l))
        print ("Горло: " + str(c))

db.session.commit()
print ("Нос: "+str(d))
print ("Ухо: "+str(l))
print ("Горло: "+str(c))


# plt.imshow(img)
# plt.title(classname)
# plt.show()