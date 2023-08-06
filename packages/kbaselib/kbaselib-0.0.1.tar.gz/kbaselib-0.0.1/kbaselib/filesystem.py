"""
@author: Jebin Jolly Abraham 
Date: 08/01/2022
"""

#Libraries 
import os


#functions 
def subfolder(path):
    """
    A function tht retruns return all the subfolders path in a folder as a list of strings. 

    Parameters: 
        path (str): The path of the folder.

    Returns:
        folder_list (list(str)): A list of all the subfolders in the folder.
    """
    folder_list = [f.path for f in os.scandir(path) if f.is_dir()]
    return folder_list


def get_files(path):
    """
    Function to retruns the path of all the files in a folder.
    
    Parameters: 
        path (str): The path of the folder.

    Returns:
        complete_file_list (list(str)): A list of all the path of files in all the subfolders in the folder.
    """
    file_list = os.listdir(path)
    complete_file_list = list()
    for file in file_list:
        complete_path = os.path.join(path, file)
        if os.path.isdir(complete_path):
            complete_file_list = complete_file_list + get_files(complete_path)
        else:
            complete_file_list.append(complete_path)

    return complete_file_list


def delete_exept_files(path, wanted_files):
    """
    A function to delete all the files in a folder except the files in the wanted_files list.
    
    Parameters:
        path (str): The path of the folder.
        wanted_files (list(str)): A list of all the files in the folder.
    
    Returns:
        None
    """
    file_list = get_files(path)
    for file in file_list:
        complete_path = os.path.join(path, file)
        if os.path.isdir(complete_path):
            delete_exept_files(complete_path, wanted_files)
        else:
            if file not in wanted_files:
                os.remove(complete_path)