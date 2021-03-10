## Cloner la branche dev du dépôt "Pay20Y/FOTS_TF"
```
git clone --single-branch -b dev https://github.com/Pay20Y/FOTS_TF.git
```

## De manière générale, suivre le README.md

À savoir :
### Récupérer les checkpoints d'un modèle pré-entraîné (SynthText 6 epochs) :
 ```
 wget https://github.com/Pay20Y/FOTS_TF/releases/download/v2/SynthText_6_epochs.tar
 ```
### et les extraire à la racine du dépôt : 
 ```
 tar xf SynthText_6_epochs.tar
 ```

### Créer un venv avec les dépendances requises :
```
mac@Lea:~/hdd/code/python/fots/FOTS_TF$ python3 -m venv .venv
mac@Lea:~/hdd/code/python/fots/FOTS_TF$ source .venv/bin/activate
(.venv) mac@Lea:~/hdd/code/python/fots/FOTS_TF$ pip install --upgrade pip
(.venv) mac@Lea:~/hdd/code/python/fots/FOTS_TF$ pip install tensorflow==1.15.0
(.venv) mac@Lea:~/hdd/code/python/fots/FOTS_TF$ pip install opencv-python
(.venv) mac@Lea:~/hdd/code/python/fots/FOTS_TF$ pip install shapely
```

### Entraîner le modèle en utilisant ses images et le modèle pré-entraîné sur SynthText

```
python main_train.py --gpu_list='0' --learning_rate=0.0001 --train_stage=0 --training_data_dir='/home/mac/hdd/data/us_maps/' --training_gt_data_dir='/home/mac/hdd/data/us_maps' --pretrained_model_path='SynthText_6_epochs/'

```

### Tester le modèle sur des imagettes
```
python main_test.py --gpu_list='0' --test_data_path=/home/mac/hdd/code/python/wms_grid_gen/tiles --checkpoint_path=checkpoints/ --output_dir='results' --no_write_images=False
```
