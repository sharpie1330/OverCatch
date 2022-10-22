"""
Reduce yolov5 Checkpoint Model Size
reference: [https://github.com/ultralytics/yolov5/issues/6417]

edited by @sharpie1330
"""

import argparse
from pathlib import Path
import sys
import os

from utils.general import strip_optimizer, increment_path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def run(
        # edit: set as default pt file, change path later, download option
        weights=ROOT / 'datasets/models/epoch60.pt',
        project=ROOT / 'runs/downsize',
        name='exp',
        exist_ok=False,  # existing project/name ok, do not increment
):
    # Directories
    save_name = Path(weights).name
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    save_dir.mkdir(parents=True, exist_ok=True)  # make dir

    strip_optimizer(weights, save_dir/save_name)


def parse_opt():
    parser = argparse.ArgumentParser()
    # edit: change default path
    parser.add_argument('--weights', type=str, default=ROOT / 'datasets/models/epoch60.pt', help='downsize checkpoint file, strip optimizer from this weights file')
    parser.add_argument('--project', default=ROOT / 'runs/downsize', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    return opt


def main(opt):
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)