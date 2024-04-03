from icecream import ic
import glob, os
from typing import Optional, Tuple
from omegaconf import DictConfig

import hydra
from hydra.core.config_store import ConfigStore

from track_pipeline import main as track_main


INPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/POCO_samples/input"
OUTPUT_FOLDER = r"/home/saboa/mnt/n_drive/AMBIENT/POCO_samples/output_HMR2"

# args_base = '--mode video --cfg configs/demo_poco_cliff.yaml --ckpt data/poco_cliff.pt '
def list_vids(root_folder, exts=['.avi', 'mp4']):
    all_vids = []
    for ext in exts:
        all_vids.extend(glob.glob(os.path.join(root_folder, "**", "*" +  ext), recursive=True))

    return all_vids

# def process_vid(args, in_vid, out_vid):
#     pa

def process_all_vids(input_vids, cfg):
    i = 0
    for vid in input_vids:
        # i = i + 1
        # if i <= 5: 
        #     continue
        print(i, len(input_vids))
        out_vid = vid.replace(INPUT_FOLDER, OUTPUT_FOLDER)
        out_folder = os.path.split(out_vid)[0]
        name = os.path.splitext(os.path.split(out_vid)[-1])[0]
        out_new_vid = os.path.join(out_folder, f"PHALP_{name}.mp4")

        if os.path.exists(out_new_vid):
            continue

        cfg['video']['source'] = vid
        cfg['video']['output_dir'] = out_folder
        track_main(cfg)

@hydra.main(version_base="1.2", config_name="config")
def main(cfg: DictConfig) -> Optional[float]:
    
    input_vids = list_vids(INPUT_FOLDER)
    process_all_vids(input_vids, cfg)


if __name__ == "__main__":
    main()

