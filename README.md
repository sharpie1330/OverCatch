# OverCatch

This project refers to yolov5. <br>
yolov5 copyright is not reserved by this project. <br>

**Overwatch Aimhack Detection**
<br>
(2022-10-22) Optimized for OVERWATCH 1
<br>


**model file download**


- download and must place model file at yolov5/datasets


> [release demo v0.0.1](https://github.com/sharpie1330/OverCatch/releases/tag/demo)


---


**HISTORY**


**[핵 판별 알고리즘 수정] (2022-10-22 update)**


- yolov5 내 새로 추가된 파일 목록
  - downsize.py -> 학습 중간에 중단된 파일 용량 줄이기
  - dist.py -> 킬사인 프레임 추출, 킬사인 기준 이전 30프레임 분석해 킬사인에 대한 타겟 파악, 30프레임 데이터 저장(보간, 이상치 제거 등)
  - train_data_generate.py

- yolov5 수정된 파일
  - detect.py -> dist 파일 저장하도록
  - utils 폴더 내 plots.py -> 조준점과 오브젝트 헤드 추정 부분(중점에서 조금 위) 사이 거리 시각화

- 핵 판별 결과 반환 코드
  - overcatch.py -> dist.py 및 detect.py 참조하여 lstm모델 통과, 결과 반환
