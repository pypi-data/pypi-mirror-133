"""convert pdf to html"""
__version__ = '0.1.0'
import os
import sys
from pathlib import Path
import shutil

def get_name_of_file_without_extension(file_name):
    """Get the name of a file without extension .

    Args:
        file_name ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    
    name = Path(file_name).stem
    print(name)
    return name

def create_directory(directory_name):
    """
    create directory
    Args:
     - directory_name
    Return:
     - os.makedirs(directory_name)
    
    """
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)
    os.makedirs(directory_name)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def cp_file(file_name, directory_name):
    os.system('cp ' + file_name + ' ' + directory_name)

def check_if_executable_exists(executable_name):
    """Check if executable exists.
    """ 
    exist = shutil.which(executable_name)
    return exist
def main():
    if len(sys.argv) > 2 and len(sys.argv) <= 1:
        print('Usage: python main.py [file_name]')
        return
    file_name = sys.argv[1]
    # wrap the file name in quotes
    print(file_name)
    name = get_name_of_file_without_extension(file_name)
    name = name.replace(' ', '_')
    print(name)
    create_directory(name)
    print(f'{name} created')
    # copy file_name to name dir
    shutil.copy(file_name, name)

    print(f'{file_name} copied')
    # check current directory
    os.chdir(name)
    # Get real path of current directory
    current_directory = os.getcwd()
    print(f'Current directory: {current_directory}')
    


    if not check_if_executable_exists('pdftohtml'):
        print('pdftohtml not found')
        return
    else:
        command = f'pdftohtml  -c -noframes  "{file_name}"  index.html'
        os.system(command)
        # remove file_name
        os.remove(file_name)
        os.chdir('..')

__name__ == '__main__' and main()
