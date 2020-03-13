ARCFACE 모델 개선하기

---

## 1. github에 있는 모델 그대로 구현

#### 참고
- [arcface-tf2](https://github.com/peteryuX/arcface-tf2)에 있는 모델 사용
- 하이퍼 파라미터 설정
|  general | | train pram  | | test pram | |
| ---------- | -------- | ---------- | -------- | ---------- | ------- |
| barch_size| 128| binary_img  | True | mode| fit |
| input_size | 112| num_classes | 85,742  | loss | Softmax |
| embd_size | 512| num_samples | 5,822,653  | data | acc |
| sub_name | 'arc-res50'| epochs  | 5  |lfw | 0.9710 |
| back_bone | 'ResNet50'| base_lr  | 0.01  | AgeDB-30 | 0.8520 |
| head_type | ArcHead| w_decay  | float 5e-4  | CFP-FP | 0.8757 |
| is_ccrop | False| save_steps | 1000  | k-face | None  |
- 결과
<img src="0.200220_test_1/200220_test_1.png" />

