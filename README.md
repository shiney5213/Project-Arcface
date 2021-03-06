# [Project] Korean Face Classification 
> Korean Face Classification Model by Arcface

## dataset

* [Ms1m_align_112](https://drive.google.com/file/d/1X202mvYe5tiXFhOx82z4rPiPogXD435i/view)
* [AI_hub:K-Face](http://www.aihub.or.kr/aidata/73)

## data preprocessing

#### 1. [Select K-Face dataset](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/1.Select%20_K-face_dataset_and_split_train_and_test.ipynb)
- 한 사람당 image가  32,400장으로 너무 많아 L1(조명-ㅣLux1000), S001(액세서리-보통), E01~E03(표정) 데이터만 사용하기로 함(1인당 train 40, test 20)
#### 2. [face_recognition](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/2.face_recognition_align_112.ipynb)
- ms1m_align_112 데이터가 가로,세로 모두 112pixel로 얼굴만 detection한 이미지이므로 k-face 데이터셋도 얼굴만 detection하여 저장함
	
  <img src="images/compare_dataset.png" alt="compare datasets" style="zoom:48%;" />
	
-  ms1m_align_112 dataset이 데이터 수도 많고, 정면 얼굴도 많아 k-face dataset과 확연히 비교가 됨.
	
#### 3.[More Select K-Face dataset](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/3.Select_more_K-face_dataset.ipynb)
- k-face dataset에서 조명을 다양하게 하고, 수를 늘리는 재작업 수행
- 조명(L1, L2, L3),  액세서리(S001, S002, S005), 방향(C5~C10), 표정(E1, E2, E3) 데이터 사용(1인당 train 132, test 30)
- face detection 할 때 ms1m dataset과 비교하여 눈,코,입 부분만을 검출하거나 입이 잘리는 이미지가 있어 box크기를 조절함.
 ![132images](images/132images.png)
#### 4. [Variety Image](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/4.make_variety_image.ipynb) : random으로 이미지에 톤의 변화를 줌.

- Gammma_LUD방법을 사용하여 hue, satuationr값을 랜덤으로 조절

  <table>
      <tr>
      <td><img src = 'images/data1.png' width = 250</td>
      <td><img src = 'images/data2.png' width = 250</td>
      <td><img src = 'images/data3.png' width = 250</td>
      <td><img src = 'images/data4.png' width = 250</td>
      </tr>
  </table>

#### 5. [trian data](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/5.convert_train_binary_tfrecord.py) : tensorflow에서 빠르게  training 하기 위해 tfrecord 파일 만들기 
<img src = 'images/tfrecord.png'  width = 100%>
- slm_align_112 데이터:  85,742명, 5,822,653장
- K-face 데이터 :  400명,  49,491장  (52,800장을 기대했으나 face detection하면서 이미지가 줄어듦.) 
- **test시에는 더 성능이 좋은 face detection model을 사용해야겠음**
- 모두  86,142폴더, 5,872,144장 이미지 준비  

#### 6. [test data]() : K-face  test set 만들기 

#### - [arcface-tf2](https://github.com/peteryuX/arcface-tf2) 에서 사용한  lwf, AgeDB, cfp dataset 과 함께 k-face을 사용하기 위해 K-face set도 다른 데이터셋과 같은 구조로 만듦.

- train data와 같이 얼굴을 찾아 112 * 112로 조절
- [file rename](): 파일 이름을 폴더명(사람 이름)_0001.jpeg로 rename
- [k-face_pairs.txt 생성]: 같은 사람의 사진 pairs와 다른 사람의 사진 paris 를 표기한 txt 파일 생성
- [k-face.bin 생성 ](https://github.com/shiney5213/Project-Arcface/blob/master/preprocessing/8.make_kface_bin.py) : kface_prairs.txt 파일을 가지고 kface.bin 파일 생성
- 
- k_face.lst 파일 생성
- k_face.rec, k_face.idx 파일 생성
- k_face.bin 파일 생성
- 위에서 만든  .rec, .idx, .bin 파일을 한 폴더에 정리하기
- [](https://github.com/deepinsight/insightface/issues/791)


## train/test

#### 0. [ordinary_train] : k-face dataset을 추가하기 전의 학습
<img src = 'images/2.train_0_test_result.jpg'  width = 100%>

|  general | | train pram  | | test pram | |
| ---------- | -------- | ---------- | -------- | ---------- | ------- |
| barch_size| 128| binary_img  | True | mode| fit |
| input_size | 112| num_classes | 85,742  | loss | Softmax |
| embd_size | 512| num_samples | 5,822,653  | data | acc |
| sub_name | 'arc-res50'| epochs  | 5  |lfw | 0.9710 |
| back_bone | 'ResNet50'| base_lr  | 0.01  | AgeDB-30 | 0.8520 |
| head_type | ArcHead| w_decay  | float 5e-4  | CFP-FP | 0.8757 |
| is_ccrop | False| save_steps | 1000  | k-face | None  |


#### 1. [first_train](https://github.com/shiney5213/Project-Arcface/blob/master/training/1.train_1.py) 
- 모델 : 참고한 [ArcFace](https://github.com/peteryuX/arcface-tf2#Training-and-Testing)의 모델의 구조 , 하이퍼 파라미터  등을 그대로 학습
- 데이터: Ms1m data + K-face data :  400명,  49,491장을 추가하여 학습
<img src = 'images/2.train_1_test_result.jpg'  width = 100%>

|  general | | train pram  | | test pram | |
| ---------- | -------- | ---------- | -------- | ---------- | ------- |
| barch_size| 128| binary_img  | True | mode| fit |
| input_size | 112| num_classes | 86,142  | loss | Softmax |
| embd_size | 512| num_samples | 5,872,144  | data | acc|
| sub_name | 'arc-res50'| epochs  | 5  |lfw | 0.9705 |
| back_bone | 'ResNet50'| base_lr  | 0.01  | AgeDB-30 | 0.8560|
| head_type | ArcHead| w_decay  | float 5e-4  | CFP-FP | 0.8817 |
| is_ccrop | False| save_steps | 1000  | k-face | 0.5652 |




## reference
* [ArcFace](https://arxiv.org/abs/1801.07698): ArcFace Paper
* [InsightFace](https://github.com/deepinsight/insightface/) : 2D and 3D Face Analysis Project
* [arcface-tf2](https://github.com/peteryuX/arcface-tf2): InsightFace by tensorflow
* [preparing_data](https://github.com/Talgin/preparing_data)
* 