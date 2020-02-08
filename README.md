# [Project] Korean Face Classification 
> Korean Face Classification Model by Arcface

## dataset

* [Ms1m_align_112](https://drive.google.com/file/d/1X202mvYe5tiXFhOx82z4rPiPogXD435i/view)
* [AI_hub:K-Face](http://www.aihub.or.kr/aidata/73)

## data preprocessing

### 1. [Select K-Face dataset]()
- 한 사람당 image가  @@@장으로 너무 많아 L1(조명-ㅣLux1000), S001(액세서리-보통), E01~E03(표정) 데이터만 사용하기로 함(1인당 train 40, test 20)
### 2. [face_recognition]()
- ms1m_align_112 데이터가 가로,세로 모두 112pixel로 얼굴만 detection한 이미지이므로 k-face 데이터셋도 얼굴만 detection하여 저장함
	
  <img src="images/compare_dataset.png" alt="compare datasets" style="zoom:48%;" />
	
-  ms1m_align_112 dataset이 데이터 수도 많고, 정면 얼굴도 많아 k-face dataset과 확연히 비교가 됨.
	
	
### 3.[More Select K-Face dataset]([https://github.com/shiney5213/Project-Arcface/blob/master/3.%20Select%20more%20K-face%20dataset%20.ipynb](https://github.com/shiney5213/Project-Arcface/blob/master/3. Select more K-face dataset .ipynb))
- k-face dataset에서 조명을 다양하게 하고, 수를 늘리는 재작업 수행 후, 다시 112 *  112로 자름
- 


mslm_align_112 데이터와 K-face data : 모두 86142 폴더, 5838653개 이미지

* > face detection 112

*  [Making tfrecord_file]




## reference
* [ArcFace](https://arxiv.org/abs/1801.07698)
* [arcface-tf2](https://github.com/peteryuX/arcface-tf2)