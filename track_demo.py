import glob, os
from typing import Optional, Tuple
from omegaconf import DictConfig

import hydra
from hydra.core.config_store import ConfigStore

from icecream import ic
from enum import Enum
import pandas as pd
import glob

from split import splitall
from track_pipeline import main as track_main


# INPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/POCO_samples/input"
# INPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/ROM_Apr22_2024"
# OUTPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/POCO_samples/output_HMR2"
# OUTPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/HMR2"
OUTPUT_FOLDER_HMR2 = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/ROM_Apr22_2024_posetracked_v3"
OUTPUT_FOLDER_HMR2 = r"/home/saboa/mnt/n_drive/AMBIENT/HMR2"

class VID_TYPE(Enum):
    ALL=1
    SPLIT=2
    FULL=3


# args_base = '--mode video --cfg configs/demo_poco_cliff.yaml --ckpt data/poco_cliff.pt '
def list_vids(root_folder, exts=['.avi', 'mp4']):
    all_vids = []
    for ext in exts:
        all_vids.extend(glob.glob(os.path.join(root_folder, "**", "*" +  ext), recursive=True))

    return all_vids



def list_custom_vids(input_folder, file_types=['mp4', 'avi']):
    all_files = []
    for ext in file_types:
        all_files.extend(glob.glob(os.path.join(input_folder, "**", f"*.{ext}"), recursive=True))

    all_vids_dict = format_MDC_output(all_files, input_folder, "Andrea_S/ROM_Apr22_2024_posetracked")

    
    return all_vids_dict
    
def list_TRI_PD_vids():
    TRI_INPUT_ROOT = r"/home/saboa/mnt/n_drive/AMBIENT/Data_Storage/TRI/videos"
    PD_scores_file = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/OBJ1- TRI Parkinsonism Data/ALL_PD_SCORES_AND_CLINICAL_DATA.xlsx"
    df = pd.read_excel(PD_scores_file)
    df.rename(columns={"AMBIENT ID": "AMBID", "File Number/Title ": "file"}, inplace=True)


    potential_files = [os.path.join(TRI_INPUT_ROOT, amb, file, "Video.avi") for amb, file in zip(df["AMBID"].to_list(), df["file"].to_list())]


    valid_vids = {}
    invalid_vids = []
    for file in potential_files:
        if os.path.exists(file):
            output_base = file.replace(TRI_INPUT_ROOT, OUTPUT_FOLDER_HMR2)
            parts = splitall(output_base)
            name = os.path.splitext(parts[-1])[0]
            output_file = os.path.join(*parts[:-3], "TRI_UPDRS",  parts[-2], f"PHALP_{name}.mp4")
            valid_vids.update({file: output_file})
            # valid_vids.append(file)
        else:
            invalid_vids.append(file)
    
    return valid_vids


def list_TRI_non_PD_vids():
    TRI_INPUT_ROOT = r"/home/saboa/mnt/n_drive/AMBIENT/Data_Storage/TRI/videos"
    PD_scores_file = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/OBJ1- TRI Parkinsonism Data/ALL_PD_SCORES_AND_CLINICAL_DATA.xlsx"
    df = pd.read_excel(PD_scores_file)
    df.rename(columns={"AMBIENT ID": "AMBID", "File Number/Title ": "file"}, inplace=True)
    pd_vids_potential_files = [os.path.join(TRI_INPUT_ROOT, amb, file, "Video.avi") for amb, file in zip(df["AMBID"].to_list(), df["file"].to_list())]

    all_full_vids = glob.glob(os.path.join(TRI_INPUT_ROOT, "**", "*.avi"), recursive=True)


    valid_vids = {}
    invalid_vids = []
    for file in all_full_vids:
        if file not in pd_vids_potential_files:
            output_base = file.replace(TRI_INPUT_ROOT, OUTPUT_FOLDER_HMR2)
            parts = splitall(output_base)
            name = os.path.splitext(parts[-1])[0]
            output_file = os.path.join(*parts[:-3], "TRI_NON_UPDRS",  parts[-2], f"PHALP_{name}.mp4")
            valid_vids.update({file: output_file})
            # valid_vids.append(file)
        else:
            invalid_vids.append(file)
    
    return valid_vids
    

def format_MDC_output(input_vids, input_folder, output_intermediate_folder):
    output_dict ={}

    for vid in input_vids:
        output_base = vid.replace(input_folder, OUTPUT_FOLDER_HMR2)
        parts = splitall(output_base)
        name = os.path.splitext(parts[-1])[0]
        output_file = os.path.join(*parts[:-1], output_intermediate_folder,  os.path.splitext(parts[-1])[0], f"PHALP_{name}.mp4")
        output_dict.update({vid: output_file})

    return output_dict


def list_MDC_vids(vid_type=VID_TYPE.ALL):
    MDC_SPLIT_VID_DIR = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/Fasano_dataset_2021/objective_2/cropped_and_split_vids"
    MDC_SPLIT_VID_DIR = r"/home/saboa/mnt/n_drive/AMBIENT/Andrea_S/Fasano_dataset_2021/objective_2/cropped_vids_may2024"
    MDC_FULL_VID_DIR = r"/home/saboa/mnt/n_drive/AMBIENT/Data_Storage/MDC/videos"
    
    all_split_vids = glob.glob(os.path.join(MDC_SPLIT_VID_DIR, "*.avi"))
    all_full_vids = glob.glob(os.path.join(MDC_FULL_VID_DIR, "**", "*.avi"), recursive=True)
    ic(len(all_split_vids), len(all_full_vids))

    # Format the output files
    if vid_type in [VID_TYPE.SPLIT, VID_TYPE.ALL]:
        all_split_vids_dict = format_MDC_output(all_split_vids, MDC_SPLIT_VID_DIR, "MDC_SPLIT_NON_CROPPED")
    if vid_type in [VID_TYPE.FULL, VID_TYPE.ALL]:
        all_full_vids_dict = format_MDC_output(all_full_vids, MDC_FULL_VID_DIR, "MDC_FULL")

    # Forcing split vids first in python version which preserve key order
    if vid_type in [VID_TYPE.ALL]:
        all_split_vids_dict.update(all_full_vids_dict)
    
    # Returning the requested dict
    if vid_type in [VID_TYPE.SPLIT, VID_TYPE.ALL]:
        return all_split_vids_dict
    else:
        return all_full_vids_dict



# def process_all_vids(input_vids, cfg):
#     i = 0
#     for vid in input_vids:

#         print(i, len(input_vids))
#         out_vid = vid.replace(INPUT_FOLDER, OUTPUT_FOLDER)
#         out_folder = os.path.split(out_vid)[0]
#         name = os.path.splitext(os.path.split(out_vid)[-1])[0]
#         out_new_vid = os.path.join(out_folder, f"PHALP_{name}.mp4")

#         if os.path.exists(out_new_vid):
#             continue

#         cfg['video']['source'] = vid
#         cfg['video']['output_dir'] = out_folder
#         track_main(cfg)


def process_all_vids_dict(input_vids, cfg):
    i = 0
    for vid, out_new_vid in input_vids.items():
        i = i + 1
        # if i == 1:
        #     continue
        print(i, len(input_vids), vid)
        res = "results"
        out_first, out_file = os.path.split(out_new_vid)
        pkl_file = os.path.join(out_first, "results", f"demo_{os.path.splitext(out_file)[0][6:]}.pkl")
        if os.path.exists(pkl_file):
            ic("skipping", out_new_vid)
            continue

        cfg['video']['source'] = vid
        cfg['video']['output_dir'] = os.path.split(out_new_vid)[0]
        ic("writing to: ", os.path.split(out_new_vid)[0])
        track_main(cfg)


@hydra.main(version_base="1.2", config_name="config")
def main(cfg: DictConfig) -> Optional[float]:
    input_vids = {}
    # input_vids = list_TRI_PD_vids()
    # input_vids = list_TRI_non_PD_vids()
    mdc_vids = list_MDC_vids(vid_type=VID_TYPE.SPLIT)

    input_vids.update(mdc_vids)

    # input_vids = list_custom_vids(INPUT_FOLDER)
    # ic(input_vids)
    # ic(len(input_vids))
    # i = 0
    # for key, val in input_vids.items():
    #     i = i + 1
    #     ic(key, val)
    #     if i > 6 :
    #         break
    # quit()
    process_all_vids_dict(input_vids, cfg)



if __name__ == "__main__":
    main()

