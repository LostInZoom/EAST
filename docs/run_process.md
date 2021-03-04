## Cloner le dépôt
```
git clone https://github.com/ilokhat/EAST.git
```

### Créer un venv avec les dépendances requises :
```
mac@Lea:~/hdd/code/python/EAST$ python3 -m venv .venv
mac@Lea:~/hdd/code/python/EAST$ source .venv/bin/activate
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip install --upgrade pip
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip install pillow matplotlib shapely opencv-python rasterio
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip install keras-adamw
```

Attention keras-adamw installe tensorflow (version cpu), il faut donc le désinstaller
```
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip uninstall tensorflow
```

Puis installer _tensorflow-gpu_ et _keras_
```
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip install tensorflow-gpu==1.15.2
(.venv) mac@Lea:~/hdd/code/python/EAST$ pip install keras==2.3.1
```
### Créer le sous-répertoire tmp/east_resnet_50_rbox :
```
(.venv) mac@Lea:~/hdd/code/python/EAST$ mkdir -p tmp/east_resnet_50_rbox

```

### Entrainer le modèle
Par exemple en fine-tunant à partir d'un modèle pré-entraîné sur ICDAR15+13 avec des nouvelles images de taille 512x512 :
```
python train2.py --input_size=512 --batch_size=5 --nb_workers=1 --training_data_path=../data/My\ Drive/east_cas_corr/train/ --validation_data_path=../data/My\ Drive/east_cas_corr/val/ --restore_model=EAST_IC15+13_model.h5 --max_epochs=2
```

Le modèle en sortie s'appelle `east_test_american.h5` et on peut le tester sur des images en faisant :

```
python eval_filled.py --gpu_list=0 --test_data_path=/path/to/images --model_path=./east_test_american.h5 --output_dir=./res/
```
On obtient en sortie, des images avec les boites de texte en overlay, et des fichiers textes correspondant, avec les coordonnées en pixels des boîtes

### Évaluer les résultats de différents modèles entraînés sur des images pour lesquelles on a une "verité terrain"

La vérité terrain consiste à avoir les coordonnées des rectangles des boîtes de texte pour une image donnée sous forme d'un geojson.
Ces fichiers geojson doivent avoir le même nom que les images e.g. : cassini_1.jpg --> cassini_1.geojson

Le script à utiliser est dans `cassini_tif_scripts/eval_results.py`

Il suffit de changer les variables suivantes pour indiquer où sont :
 - `ref_jsons` : les geojsons de référence 
 - `res_root_dir` : le répertoire racine contenant les sous-répertoires des résultats des différents modèles (les fichiers textes des coordonnées des boîtes) 
 - `res_dirs` : une liste des noms de ces sous-répertoires

```python
ref_jsons = './cassini_ref'
res_root_dir = '/home/mac/hdd/code/python/myEAST/EAST'
res_dirs = ['mask4ep', 'mask5ep', 'mask6ep', 'klodo', 'res_cas2_2ep', 'res_cas_2ep', 'res_cas_ext2_1ep']
```
