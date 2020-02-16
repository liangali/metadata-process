import json
import sys

class DetectOut():
    def __init__(self, confidence, label, rect):
        self.confidence = confidence
        self.label = label
        self.rect = rect
        self.strline = self.toString()
    def toString(self):
        out = 'Detection: {'
        out = out + 'label = ' + str(self.label) + ', '
        strv = "{0:.4f}".format(self.confidence)
        out = out + 'confidence = ' + strv + ', '
        tmp = ''
        for r in self.rect:
            tmp = tmp + str(r) + ', '
        out = out + 'rect = [' + tmp[0:len(tmp)-2] + ']' 
        out = out + '}'
        return out

class ClassifyOut():
    def __init__(self, topv, topi):
        self.topv = topv
        self.topi = topi
        self.strline = self.toString()
    def toString(self):
        out = 'Classification: {'
        topstr = ''
        for i in range(len(self.topv)):
            strv = "{0:.4f}".format(self.topv[i])
            topstr = topstr + str(self.topi[i]) + ' : ' + strv + '; '
        out = out + topstr + '}'
        return out

class MetaOutput():
    def __init__(self, d, c):
        self.detect = d
        self.classify = c
        self.outline = self.toString()
    def toString(self):
        return self.detect.strline + ';  ' + self.classify.strline

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: bad command line! example: python meta.py out.json")
        exit()
    jsonfile = sys.argv[1]

    with open(jsonfile, "rt") as f:
        data = f.read()
    jd = json.loads(data)

    obj_count, frame_idx = 0, 0
    for f in jd:
        frame, detect, classify = '', [], []
        if 'objects' in f.keys():
            for d in f['objects']:
                c = d['detection']['confidence']
                l = d['detection']['label_id']
                r = [d['x'], d['y'], d['w'], d['h']]
                dout = DetectOut(c, l, r)
                detect.append(dout)
        if 'tensors' in f.keys():
            for t in f['tensors']:
                if 'data' in t.keys():
                    probs = t['data']
                    topv = sorted(probs, reverse=True)[0:5]
                    topi = sorted(range(len(probs)), key=lambda k: probs[k], reverse=True)[0:5]
                    cout = ClassifyOut(topv, topi)
                    classify.append(cout)
        if len(detect) != len(classify):
            print('WARNING: object number of detection and classification does not match!')
        for i in range(len(detect)):
            vaout = MetaOutput(detect[i], classify[i])
            frame = 'frame_id = ' + str(frame_idx) + ';  '
            frame = frame + vaout.outline
            print(frame)
        frame_idx = frame_idx + 1
        obj_count = obj_count + len(detect)

    print('done!', obj_count, 'objects in', frame_idx, 'frames')