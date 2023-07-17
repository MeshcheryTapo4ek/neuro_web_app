import os
import docker
from docker.errors import ContainerError, ImageNotFound


class CContainer:
    def __init__(self, containerID, name, request_path, post_path):
        self.name = name
        self.containerID = containerID
        self.request_path = request_path
        self.post_path = post_path

container_name = "auto_image_processing_container_"

def create_container(container_N):
    client = docker.from_env()

    try:
        container = client.containers.get(container_name + str(container_N))
        print("Контейнер " + container_name + str(container_N) + " уже был создан!")
    except docker.errors.NotFound:
        print("Контейнер " + container_name + str(container_N) + " создается ")

        Bind_path = os.path.join(os.getcwd(),'container_management', 'temp_list', 'temp'+str(container_N))
       # print(Bind_path)
        volumes = {
            Bind_path: {
                'bind': '/app/temp/',
                'mode': 'z'
            }
        }
        try:
            container = client.containers.run('meshcherytapo4ek/auto_image_processer:image-processing',
                                              volumes=volumes,
                                              detach=True,
                                              name= (container_name + str(container_N)) )
            print("Контейнер "+ container_name + str(container_N)+ " успешно создан!")

            request_path = os.path.join(Bind_path, 'request')
            post_path = os.path.join(Bind_path, 'post')
            c_container = CContainer(container.id,container_N, request_path, post_path)

            container.stop()
            return c_container

        except ContainerError as e:
            print("Ошибка запуска контейнера:", str(e))
        except ImageNotFound as e:
            print("Ошибка поиска образа:", str(e))



def create_containers(num_containers):
    client = docker.from_env()

    containers = []
    for i in range(num_containers):
        container_name = f"auto_image_processing_container_{i}"
        try:
            containerID = (client.containers.get(container_name)).id
            bind_path = os.path.join(os.getcwd(), 'container_management', 'temp_list', f'temp{i}')
            request_path = os.path.join(bind_path, 'request')
            post_path = os.path.join(bind_path, 'post')
            c_container = CContainer(containerID, f"{i}", request_path, post_path)
            containers.append(c_container)
        except docker.errors.NotFound:
            container_name = f"{i}"
            container = create_container(container_name)
            if container:
                containers.append(container)

    return containers

def find_first_stopped_container(CContainers):
    client = docker.from_env()

    for CContainer in CContainers:
        container = client.containers.get(CContainer.containerID)
        if  container.status!= "running":
            return CContainer

    return None

def test_containers():
    created_containers = create_containers(5)

    for container in created_containers:
        print("Номер контейнера:", container.name)
        print("ID контейнера:", container.containerID)
        print("Путь к папке 'request':", container.request_path)
        print("Путь к папке 'post':", container.post_path)
        print()

    stopped_ccontainer = find_first_stopped_container(created_containers)
    client = docker.from_env()
    container = client.containers.get(stopped_ccontainer.containerID)
    if stopped_ccontainer:
        print("Найден первый остановленный контейнер:")
        print("ID контейнера:", stopped_ccontainer.containerID)
        print("Имя контейнера:", stopped_ccontainer.name)
        print("Статус контейнера:", container.status)
    else:
        print("Все контейнеры находятся в состоянии 'running'")

def startCCont(CContainer):
    client = docker.from_env()
    container = client.containers.get(CContainer.containerID)
    container.start()

def stopCCont(CContainer):
    client = docker.from_env()
    container = client.containers.get(CContainer.containerID)
    container.stop(timeout=0)

#test_containers()