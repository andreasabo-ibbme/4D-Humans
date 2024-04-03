```
pyenv install -v 3.10.11
pyenv virtualenv 3.10.11 hmr3.10
pyenv activate hmr3.10

python -m pip install --upgrade pip
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
pip install wheel
pip install -e .[all]


python demo.py --img_folder example_data/images --out_folder demo_out --batch_size=48 --side_view --save_mesh --full_frame
```