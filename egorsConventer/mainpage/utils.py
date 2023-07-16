import docker
import os
import shutil
import time

from docker.errors import NotFound

menu = [   {'title': "info", 'url_name': "inf"},
        {'title':"mainpage", 'url_name':"home"}]

class DataMixin:
    def get_user_context(self, **kwargs):
            context = kwargs
            context['menu'] = menu
            return context


def process_picture(image_name):

    # создаем контейнер или запускаем если уже создан
    client = docker.from_env()


    try:
        container = client.containers.get("automatic_image_processing")
        if container.status != 'running':
            container.start()
            print("Контейнер найден и успешно возообновлен!")

    except NotFound:
        print(" Контейнер не найден, запускаем новый")
        Bind_path = os.path.join(os.getcwd(), 'temp')
        volumes = {
            Bind_path: {
                'bind': '/app/temp/',
                'mode': 'z'
            }
        }
        try:
            container = client.containers.run('image-processing',
                                              volumes=volumes,
                                              detach=True,
                                              name="automatic_image_processing",)
            print("Контейнер успешно запущен!")
        except docker.errors.ContainerError as e:
            print("Ошибка запуска контейнера:", str(e))
        except docker.errors.ImageNotFound as e:
            print("Ошибка поиска образа:", str(e))

    # обмен картинками с контейнером
    Request_imageF_path = os.path.join(os.getcwd(), 'temp', 'request')
    Post_imageF_path = os.path.join(os.getcwd(), 'temp', 'post')
    ProjectImageF_path = os.path.join(os.getcwd(), 'media', 'images')
    ProjectEditedImageF_path = os.path.join(os.getcwd(), 'media', 'edited_images')

    # закидываем картинку контейнеру
    shutil.copy(os.path.join(ProjectImageF_path, image_name), os.path.join(Request_imageF_path, image_name))
    # ожидаем когда контейнер вернет картинку а после останавливаем его

    file_list = os.listdir(Post_imageF_path)
    image_files = [f for f in file_list if f.endswith((".jpg", ".png"))]

    while len(image_files) == 0:
        file_list = os.listdir(Post_imageF_path)
        image_files = [f for f in file_list if f.endswith((".jpg", ".png"))]
        time.sleep(0.005)
    print("Получили изображения от контейнера:")
    print(image_files)
    container.stop(timeout=0)

    shutil.move(os.path.join(Post_imageF_path, image_name), os.path.join(ProjectEditedImageF_path,image_name))



