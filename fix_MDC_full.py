import os, glob, shutil
from icecream import ic

from split import splitall

OUTPUT_FOLDER_HMR2 = r"/home/saboa/mnt/n_drive/AMBIENT/HMR2"

def list_MDC_full(input_path):
    dirs = glob.glob(os.path.join(input_path, "*", "MDC_FULL"))
    return dirs


def move_files(orig_dirs):
    for dir in orig_dirs:
        parts = splitall(dir)
        new_dir = os.path.join(*parts[:-2], parts[-1], parts[-2])
        ic(parts, new_dir)
        shutil.move(dir, new_dir)


if __name__ == "__main__":
    files = list_MDC_full(OUTPUT_FOLDER_HMR2)
    move_files(files)
    ic(len(files))