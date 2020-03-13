ARCFACE 모델 개선하기

---

## 0. github에 있는 모델 그대로 구현

#### 참고

- [arcface-tf2](https://github.com/peteryuX/arcface-tf2)에 있는 모델 다운로드하여 그대로 사용
- 하이퍼 파라미터 설정
|  general | | train pram  | | test pram | |
| ---------- | -------- | ---------- | -------- | ---------- | ------- |
| barch_size| 128| binary_img  | True | mode| fit |
| input_size | 112| num_classes | 85,742  | loss | Softmax |
| embd_size | 512| num_samples | 5,822,653  | data | acc |
| sub_name | 'arc-res50'| epochs  | 5  |lfw | 0.9935 |
| back_bone | 'ResNet50'| base_lr  | 0.01  | AgeDB-30 | 0.9503 |
| head_type | ArcHead| w_decay  | float 5e-4  | CFP-FP | 0.9036 |
| is_ccrop | False| save_steps | 1000  | k-face | None  |
- 결과
<img src="0.200220_test_1/200220_test_1.png" />

---

## 1. 위의 모델을 그대로 구현해보자

#### 1.1. dataset

- MS-Celeb-1M : [download](https://drive.google.com/file/d/1X202mvYe5tiXFhOx82z4rPiPogXD435i/view)

- tfrecord 파일로 변환 ([참고](https://github.com/peteryuX/arcface-tf2/blob/master/data/convert_train_binary_tfrecord.py))

  <img src="./1.200216_sameModel/tfrecord.png"  />

#### 1.2. train

	- github에 있는 소스코드 참고([참고](https://github.com/peteryuX/arcface-tf2/blob/master/train.py))
	- 하이퍼 파라미터 설정

|            |             | train pram  |            | test pram |         |
| ---------- | ----------- | ----------- | ---------- | --------- | ------- |
| barch_size | 128         | binary_img  | True       | mode      | fit     |
| input_size | 112         | num_classes | 85,742     | loss      | Softmax |
| embd_size  | 512         | num_samples | 5,822,653  | data      | acc     |
| sub_name   | 'arc-res50' | epochs      | 5          | lfw       | 0.9710  |
| back_bone  | 'ResNet50'  | base_lr     | 0.01       | AgeDB-30  | 0.8520  |
| head_type  | ArcHead     | w_decay     | float 5e-4 | CFP-FP    | 0.8757  |
| is_ccrop   | False       | save_steps  | 1000       | k-face    | None    |

#### 1.3. 결과

<img src="./1.200216_sameModel/1.train_0_test_result.jpg" />

#### 1.4. 해석

- github에 올려놓은 모델로 학습했을 때보다 성능이 떨어지는 것을 볼 수 있음.

- 학습시 환경이나 setting이 다르기 때문이라고 생각됨. 

- 이 성능을 개선시키기 위한 다양한 방법을 시도해봐야겠음.

---

  ## 2. Kface dataset을 추가해서 학습해보자

#### 2.1. dataset

- [Ms1m_align_112](https://drive.google.com/file/d/1X202mvYe5tiXFhOx82z4rPiPogXD435i/view)  : 85,742명, 5,822,653장
- [AI_hub:K-Face](http://www.aihub.or.kr/aidata/73) :  400명,  49,491장 
- 모두  86,142폴더, 5,872,144장 이미지 

#### 2.2. train

- 이전 모델의 구조, 하이퍼 파라미터 그대로 사용

general | | train pram  | | test pram | |
| ---------- | -------- | ---------- | -------- | ---------- | ------- |
| barch_size| 128| binary_img  | True | mode| fit |
| input_size | 112| num_classes | 86,142  | loss | Softmax |
| embd_size | 512| num_samples | 5,872,144  | data | acc|
| sub_name | 'arc-res50'| epochs  | 5  |lfw | 0.9705 |
| back_bone | 'ResNet50'| base_lr  | 0.01  | AgeDB-30 | 0.8560|
| head_type | ArcHead| w_decay  | float 5e-4  | CFP-FP | 0.8817 |
| is_ccrop | False| save_steps | 1000  |       |        |

## 2.3. 결과

<img src="./2.200221_kfacesetModel/2.train_1_test_result.jpg" />