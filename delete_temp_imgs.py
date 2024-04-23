import os, glob, shutil
from icecream import ic

from split import splitall

OUTPUT_FOLDER_HMR2 = r"/home/saboa/mnt/n_drive/AMBIENT/HMR2"


if __name__ == "__main__":
    image_folders = glob.glob(os.path.join(OUTPUT_FOLDER_HMR2, '**', "_DEMO"), recursive=True)
    
    for i in range(len(image_folders)):
        folder_to_del = image_folders[i]
        ic(i, len(image_folders), folder_to_del)

        try:
            shutil.rmtree(folder_to_del)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

