import shutil
import time
import multiprocessing

# импортируем данные для работы с созданным классом CContainer
from container_management.container_manager import *
from mainpage import CContainer_list


menu = [   {'title': "info", 'url_name': "inf"},
        {'title':"mainpage", 'url_name':"home"}]

class DataMixin:
    def get_user_context(self, **kwargs):
            context = kwargs
            context['menu'] = menu
            return context


def user_process_picture(image_name):

    # ожидаем и находим свободный контейнер
    WorkingCContainer = find_first_stopped_container(CContainer_list)
    while WorkingCContainer == None:
        WorkingCContainer = find_first_stopped_container(CContainer_list)
        time.sleep(0.05)

    # обмен картинками с контейнером
    Request_imageF_path = WorkingCContainer.request_path
    Post_imageF_path = WorkingCContainer.post_path
    ProjectImageF_path = os.path.join(os.getcwd(), 'media', 'images')
    ProjectEditedImageF_path = os.path.join(os.getcwd(), 'media', 'edited_images')

    # закидываем картинку контейнеру и активируем его
    shutil.copy(os.path.join(ProjectImageF_path, image_name), os.path.join(Request_imageF_path, image_name))

    startCCont(WorkingCContainer)
    # ожидаем когда контейнер вернет картинку а после останавливаем его

    file_list = os.listdir(Post_imageF_path)
    image_files = [f for f in file_list if f.endswith((".jpg", ".png"))]

    while len(image_files) == 0:
        file_list = os.listdir(Post_imageF_path)
        image_files = [f for f in file_list if f.endswith((".jpg", ".png"))]
        time.sleep(0.005)
    print("Получили изображения от контейнера №:" + WorkingCContainer.name)
    print(image_files)

    # после получения выключаем контейнер
    stopCCont(WorkingCContainer)

    shutil.move(os.path.join(Post_imageF_path, image_name), os.path.join(ProjectEditedImageF_path,image_name))





