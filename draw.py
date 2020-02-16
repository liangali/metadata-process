import numpy as np
import cv2
import json
import sys

imgpath = 'dog.bmp'
image = cv2.imread(imgpath) 
image_out =  image

def getROI(jsonfile):
    rois = []
    with open(jsonfile, "rt") as f:
        data = f.read()
    jd = json.loads(data)

    label = [256, 256, 259, 254, 259, 229, 239, 153]

    for f in jd:
        frame, detect = '', []
        if 'objects' in f.keys():
            idx = 0
            for d in f['objects']:
                c = d['detection']['confidence']
                l = d['detection']['label_id']
                r = [d['x'], d['y'], d['w'], d['h'], label[idx]]
                idx = idx + 1
                rois.append(r)
    return rois

if len(sys.argv) == 1:
    jsonfile = 'data.json'
elif len(sys.argv) == 2:
    jsonfile = sys.argv[1]
else:
    print("ERROR: bad command line! example: python draw.py data.json")
    exit()

rois = getROI(jsonfile)

i = 0
for r in rois:
    # dump ROI as image files
    crop_image = image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
    roi_name = 'out_roi_' + str(i) + '.png'
    cv2.imwrite(roi_name, crop_image)

    # resize ROI and dump
    resized_image = cv2.resize(crop_image, (224, 224))
    resized_name = 'out_roi_resize_' + str(i) + '.png'
    cv2.imwrite(resized_name, resized_image)

    # draw ROI region mask
    start_point = (r[0], r[1]) 
    end_point = (r[0]+r[2], r[1]+r[3]) 
    blue_color = (255, 0, 0) 
    green_color = (0, 255, 0) 
    thickness = 2
    image_out = cv2.rectangle(image_out, start_point, end_point, blue_color, thickness)
    cv2.putText(image_out, str(r[4]), (r[0], r[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, green_color, 2)
    i = i + 1

cv2.imwrite('out_mask.png',image_out)

print('done')
























