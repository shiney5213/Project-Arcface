import os
import sys
import cv2

from pathlib import Path
from PIL import Image

import face_src.utils as utils

def make_aligned_dataset(img_root, align_root):
        root_path  = Path(img_root)
        align_path = Path(align_root)

        # org directory
        for obj in root_path.iterdir():
            if obj.is_file():
                continue
            else:
                
                target_dir = align_path / obj.name
                if not os.path.exists(target_dir.absolute()) :
                    target_dir.mkdir()

                for file in obj.iterdir():
                    if not file.is_file():
                        continue
                    else:
                        target_file = target_dir / file.name
                        img = Image.open(file.absolute())

                        aligned = utils.align_face(img)
                        if not aligned is None:
                            # aligned = aligned.resize((112, 112))
                            aligned.save(target_file.absolute())
                        else:
                            print("source none", file.absolute())
                            #image = cv2.imread(file_name)
                        

