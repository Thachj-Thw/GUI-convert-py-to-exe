import os


def check_and_mkdir(dir_name):
    path = os.path.join(os.getcwd(), dir_name)
    if not os.path.isdir(path):
        os.mkdir(path)


check_and_mkdir("build")
check_and_mkdir("dist")
check_and_mkdir("spec")

requirements_path = os.path.join(os.getcwd(), "requirements.txt")
err = os.system(f'pip install -r "{requirements_path}"')
if err:
    print("Erorr")
else:
    print("Successfully")

input("Press enter to exit")
