import os
import re 
from fnmatch import fnmatch
import numpy as np
import cv2


# rac = 'cassini_25'
# testfile = f'../EAST/mask5/{rac}.txt'
# testfile2 = f'../EAST/mask5c/{rac}_niblack_.txt'
# testfile3 = f'../EAST/mask5c/{rac}_sauvola_.txt'
# testimg = f'./res2/{rac}.jpg'

images_dir = './mask8ep'
rects_dir  = './mask8ep'
result_dir = './res8'

def get_rectangles(txtfile):
    r = []
    with open(txtfile) as f:
        for l in f:
            n = np.array(list(map(int, l.split(',')))).reshape((4,2))
            r.append(n)
    #print(r)
    return r

def add_masques(image_path, rectangles, alpha=0.75):
    image = cv2.imread(image_path)
    orig = image.copy()
    for r in rectangles:
        cv2.fillPoly(image, [r], 1, 255)
    image_new = cv2.addWeighted(image, alpha, orig, 1 - alpha, 0)
    return image_new

def mask_combine(images_dir, rects_dir, result_dir):
    onlyfiles = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f)) and f.endswith('jpg')]
    rect_files = [f for f in os.listdir(rects_dir) if os.path.isfile(os.path.join(rects_dir, f)) and f.endswith('txt')]
    for f in onlyfiles:
        m = re.search(r".*_\d*", f)
        motif = m.group()
        sel =  [ff for ff in rect_files if ff.startswith(motif+"_") or ff.startswith(motif+".")] # fnmatch(ff, f'{motif}_*.jpg')]
        r = []
        print(len(sel))
        for rfile in sel:
            #print(f'{rects_dir}/{rfile}')
            r.extend(get_rectangles(f'{rects_dir}/{rfile}'))
        print(motif, f'{images_dir}/{f}', f'{result_dir}/{f}')
        im = add_masques(f'{images_dir}/{f}', r)
        cv2.imwrite(f'{result_dir}/{motif}_masked.jpg', im)

        
    #print(rect_files)



#r = get_rectangles(testfile)
# r = np.concatenate((get_rectangles(testfile), get_rectangles(testfile2)))
# r = np.concatenate((r, get_rectangles(testfile3)))
# im = add_masques(testimg, r)
# cv2.imwrite(f'{rac}.jpg', im)
mask_combine(images_dir, rects_dir, result_dir)
#print(type(r))