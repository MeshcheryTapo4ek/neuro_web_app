import os
from PIL import Image
import numpy as np
import tensorflow as tf
import time

autoencoder_model = None

def load_autoencoder_model():
    global autoencoder_model
    if autoencoder_model is None:
        #model_path = os.path.join(os.getcwd(), "models", "autoencoder_model.h5")
        model_path = "/app/models/autoencoder_model.h5"
        autoencoder_model = tf.keras.saving.load_model(model_path)
        print("Модель автоэнкодера загружена")
def pil_loader(path: str) -> Image.Image:
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert("RGB")
def process_image(image_path):
    size = [540, 360]
    im = pil_loader(image_path)
    original_width, original_height = im.size
    im = im.resize((size[0], size[1]))
    im = im.convert("L")
    im = np.asarray(im)

    im = im.reshape(size[1], size[0], 1)
    im = np.array(im).astype('float32') / 255.0
    expanded_im = np.expand_dims(im, axis=0)

    transformed_image = autoencoder_model.predict(expanded_im)

    transformed_image = (transformed_image * 255).astype(np.uint8)
    transformed_image = transformed_image.reshape(size[1], size[0])
    transformed_image = Image.fromarray(transformed_image, mode='L')

    transformed_image = transformed_image.resize((original_width, original_height))

    filename = os.path.basename(image_path)

    save_path = "/app/temp/post/"
    save_path = os.path.join(save_path, filename)
    transformed_image.save(save_path)

load_autoencoder_model()
#folder_path = os.path.join(os.getcwd(), "temp", "request")
folder_path = "/app/temp/request/"

while True:
    file_list = os.listdir(folder_path)
    image_files = [f for f in file_list if f.endswith((".jpg", ".png"))]
    if len(image_files) != 0:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            process_image(image_path)
            os.remove(image_path)
    time.sleep(0.005)