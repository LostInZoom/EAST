from os import listdir
import os.path

import json
from shapely.geometry import Polygon
from shapely.geometry import box
from PIL import Image

data_path = '/home/mac/hdd/data/text_detection/weinman/maps'
output = '/home/mac/hdd/data/text_detection/weinman/out_1024'
HEIGHT, WIDTH = 1024, 1024

def translate_coords(new_x, new_y, coords):
    return [[c[0] - new_x, c[1] - new_y] for c in coords]

# item => top_left to bottom_left = coords
# icdar => bottom_left to top_left = s
# en coordonees images
def item_to_icdar(item, polygon, new_x, new_y):
    coords = item["points"]
    text = item["text"]
    if len(coords) > 4:
        return ''
    coords = [[int(c[0]), int(c[1])] for c in coords]
    text_box = Polygon(coords)
    if polygon.contains(text_box):
        coords = translate_coords(new_x, new_y, coords)
        #print(Polygon(coords))
    else:
        bounds = text_box.intersection(polygon).bounds # (minx, miny, maxx, maxy)
        coords = [[bounds[0], bounds[3]], [bounds[2], bounds[3]], [bounds[2], bounds[1]], [bounds[0], bounds[1]]]
        coords = [[int(c[0]), int(c[1])] for c in coords]
        coords = translate_coords(new_x, new_y, coords)
        #print(Polygon(coords))
    s = (f'{coords[3][0]},{coords[3][1]},{coords[2][0]},{coords[2][1]},'
         f'{coords[1][0]},{coords[1][1]},{coords[0][0]},{coords[0][1]},{text}')
    return s

def get_items_intesecting(polygon, data):
    sel = []
    for e in data:
        items = e["items"]
        for item in items:
            coords = item["points"]
            coords = [[int(c[0]), int(c[1])] for c in coords]
            coords.append(coords[0])
            if polygon.intersects(Polygon(coords)):
                sel.append(item)
    return sel

def split_tiff(tiff, data, out_path, H=720, W=1280, prefix=''):
    im = Image.open(tiff)
    width, height = im.size   # Get dimensions
    c = 0
    for x in range(0, width, W):
        r = 0
        for y in range(0, height, H):
            txt = []
            print(prefix, r, c)
            left = width - W if (width - x) < W else x
            top = height - H if (height - y) < H else y
            right, bottom = left + W, top + H
            tile = Polygon([[left, top], [right, top], [right, bottom], [left ,bottom], [left, top]])
            sel = get_items_intesecting(tile, data)
            for item in sel:
                line = item_to_icdar(item, tile, left, top)
                if line != '':
                    txt.append(line)
            cropped = im.crop((left, top, right, bottom))
            basename = f'{prefix}_{r}_{c}'
            cropped.save(f'{out_path}/{basename}.jpg')
            with open(f'{out_path}/gt_{basename}.txt','w') as f:
                f.write('\n'.join(txt))
            r += 1
            print("------------------------------------------")
        c += 1

tiff_files = (f for f in listdir(data_path) if f.endswith('.tiff'))
for i, tif in enumerate(tiff_files):
    tif_path = f'{data_path}/{tif}'
    (base, _) = os.path.splitext(tif)
    jsonfile = f'{data_path}/{base}.json'
    with open(jsonfile) as j:
        data = json.load(j)
    print(tif, "-->", f'{output}/{i}_r_c.jpg')
    split_tiff(tif_path, data, output, H=HEIGHT, W=WIDTH, prefix=i)
