#!/bin/bash

pyenv activate hmr3.10
x=0
# echo $bak_file
# Continue to try processing while the back up file exists
while [[ $x -le 600 ]]
do
    # python alphapose_for_pipeline.py --input $bak_file --config-file-custom $config_file
    python track_demo.py
    x=$(( $x + 1 ))
done

pyenv deactivate