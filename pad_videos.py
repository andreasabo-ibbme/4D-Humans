import os, glob, sys
import cv2
from icecream import ic
import numpy as np


INPUT_PATH = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/hmr2_resize"
OUTPUT_PATH = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/hmr2_resize_padded"


def pad_file(input_file, output_file, new_ratio=0.85):
    ic(input_file, out_file)
    cap = cv2.VideoCapture(input_file)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec_code =  cap.get(cv2.CAP_PROP_FOURCC)
    str_codec = int(codec_code).to_bytes(4, byteorder=sys.byteorder).decode()
    ic(int(codec_code).to_bytes(4, byteorder=sys.byteorder).decode())
    out = cv2.VideoWriter(
        output_file,
        # cv2.VideoWriter_fourcc("F", "M", "P", "4"),
        cv2.VideoWriter_fourcc(*str_codec),
        fps,
        (frame_width, frame_height),
    )

    while(True):
        ret, frame = cap.read()
        
        if ret == True: 
            out.write(frame)
        else:
            break 


    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    input_files = glob.glob(os.path.join(INPUT_PATH, "*.avi"))
    ic(input_files)

    for file in input_files:
        out_file = file.replace(INPUT_PATH, OUTPUT_PATH)
        pad_file(file, out_file)
        quit()
