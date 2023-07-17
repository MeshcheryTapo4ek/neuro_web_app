from container_management.container_manager import *

# тут указано количество создаваемых контейнеров для проекта
def init_containers():
    CContainer_list = create_containers(5)
    return CContainer_list

def checkCC(CContainer_list):
    if CContainer_list:
        for container in CContainer_list:
            print( "Container №" + container.name + " is active!")
          #  print("Номер контейнера:", container.name)
           # print("ID контейнера:", container.containerID)
           # print("Путь к папке 'request':", container.request_path)
           # print("Путь к папке 'post':", container.post_path)

    else:
        print(" its empty!")

    print(" ")
