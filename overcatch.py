from yolov5.detect import Inference
from yolov5.dist import Dist
from pathlib import Path
import os
import sys
import numpy as np

from pandas import Series
import tensorflow as tf
import keras

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class OverCatch:
    weights = ROOT / 'yolov5' / 'datasets' / 'overwatch_best.pt'
    model_dist = ROOT / 'yolov5' / 'datasets' / 'dist_model_vanilla.h5'
    imgsz = (1080, 1920)
    conf = 0.1
    source = ''
    project = ROOT / 'result'
    name = ''
    data = ROOT / 'datasets' / 'data.yaml'
    nosave = False
    save_dist = True
    save_conf = True
    exist_ok = True

    def __init__(self, filename):
        OverCatch.name = str(Path(filename).stem)
        OverCatch.source = ROOT / 'original' / '{}'.format(filename)

    @staticmethod
    def predict():
        if not os.path.exists(OverCatch.project):
            os.makedirs(OverCatch.project)
        Inference.run(weights=OverCatch.weights, imgsz=OverCatch.imgsz, conf_thres=OverCatch.conf,
                      source=OverCatch.source, project=OverCatch.project, name=OverCatch.name,
                      data=OverCatch.data, nosave=OverCatch.nosave, save_dist=OverCatch.save_dist,
                      save_conf=OverCatch.save_conf)
        dist_filepath = str(ROOT / 'result' / OverCatch.name / 'dist' / '{}_dist.txt'.format(OverCatch.name))
        ks_frame_target, dist, dist_diff, dist_vanilla = Dist.get_dict(dist_filepath)

        # dist
        frame_list = list()
        sequences = list()
        for k, v in dist_vanilla.items():
            frame_list.append(k)
            sequences.append(Series(v).fillna(0).tolist())
        padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(sequences,
                                                                      padding='post',
                                                                      truncating='post',
                                                                      dtype='float',
                                                                      maxlen=30,
                                                                      value=0)
        model = keras.models.load_model(OverCatch.model_dist)
        pred = model.predict(padded_inputs)
        # test_preds = (pred > 0.5).astype("int32")
        # tp = model.predict(padded_inputs).astype("float64")
        # print(tp)
        # hack = 0
        # for i in range(len(test_preds)):
        #     if test_preds[i][0] == 1:
        #         hack += test_preds[i][0]

        # print('Hack : {}, General : {}'.format(hack / len(test_preds), 1 - (hack / len(test_preds))))
        # if hack / len(test_preds) > (1 - (hack / len(test_preds))):
        #     print('핵 사용 의심됨!')
        # else:
        #     print('핵을 사용하지 않음으로 판단됨.')
        pc_list = pred.flatten(order='C').tolist()
        pc_mean = np.mean(pc_list)

        if pc_mean > 0.5:
            seq_index = pc_list.index(max(pc_list))
        else:
            seq_index = pc_list.index(min(pc_list))

        pc_seq = Series(sequences[seq_index]).interpolate().dropna().tolist()

        target_index = ks_frame_target[frame_list[seq_index]]
        target_list = ['ANA', 'BASTION', 'CASSIDY', 'LUCIO', 'MEI',
                       'REAPER', 'ROADHOG', 'SOLDIER-76', 'SOMBRA', 'TORBJORN',
                       'ZARYA', 'ZENYATA', 'kill-sign']
        target = target_list[target_index]

        # percent = np.mean(pred.flatten(order='C').tolist())
        return pc_mean, pc_seq, target