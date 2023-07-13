from PIL import Image
import os
import tensorflow as tf
import numpy as np
from numpy import asarray

menu = [   {'title': "info", 'url_name': "inf"},
        {'title':"mainpage", 'url_name':"home"}]


class DataMixin:
    def get_user_context(self, **kwargs):
            context = kwargs
            context['menu'] = menu
            return context


def pil_loader(path: str) -> Image.Image:
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert("RGB")

def process_image(image_path, name):
    model_path = os.path.join(os.getcwd(), 'models', 'my_model.keras')
    autoencoder_model = tf.keras.models.load_model(model_path)

    image_path= os.path.join(os.getcwd(), 'media', 'images', name)

    size = [540, 360]
    im = pil_loader(image_path)

    original_width, original_height = im.size
    im = im.resize((size[0], size[1]))
    im = im.convert("L")
    im = asarray(im)

    im = im.reshape(size[1], size[0], 1)
    im = np.array(im).astype('float32') / 255.0
    expanded_im = np.expand_dims(im, axis=0)

    transformed_image = autoencoder_model.predict(expanded_im)

    transformed_image = (transformed_image * 255).astype(np.uint8)
    transformed_image = transformed_image.reshape(size[1], size[0])
    transformed_image = Image.fromarray(transformed_image, mode='L')

    transformed_image = transformed_image.resize((original_width, original_height))

    image_path = os.path.join(os.getcwd(), 'media', 'images',"TR"+ name.rsplit(".", 1)[0] +".jpg")
    transformed_image.save(image_path)
