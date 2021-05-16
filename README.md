# 2D-single-image-to-3D-model-with-geometric-depthmap
## DIP_project


> 살기좋은 주거공간을 찾기 위한 3D 모델링



![image](https://user-images.githubusercontent.com/46091177/116972531-1b024d00-acf6-11eb-8d3f-a34f25153528.png)




<수행환경>
우분투PC or 윈도우PC+가상머신(vmware workstation)
python3.6
matlab (방의 layout 알아내기 위해서 open source사용)


####요구되는 python 라이브러리####
-numpy
-matplotlib
-numpy
-scipy
-pylab
-opencv
-open3d 


####open3d 설치방법####
$git clone --recursive https://github.com/intel-isl/Open3D

$util/scripts/install-deps-ubuntu.sh

$which python3.6 와 python -V 창에 입력해서 파이썬 위치와 버전 파악

$cmake -DPYTHON_EXECUTABLE=/usr/bin/python3.6  
-- Found PythonInterp: /usr/bin/python3.6 (found version "3.6.9") 뜨는지 확인

$cmake -DCMAKE_INSTALL_PREFIX=/home/juyeon(본인경로)/Open3D/build ..

$cd Open3D

$pip uninstall open3d 

$make install-pip-package 


####코드 시행하기####

해당 위치에서의 우분투 터미널창에 다음의 커맨드 입력해서 시행
input 폴더에는 입력물이 있으며
output 폴더에서 각 코드의 결과물은 볼 수 있으며 output(mid_ppt)에선 중간발표까지의 결과물을 볼 수 있습니다.
layout폴더에는 mat형태의 room layout map이 RGB 3개 있습니다.
인풋 한장만을 넣어놧는데 만약 다른 인풋의 실행결과를 보고싶다면 따로 메일 주세요

=> 터미널 창에 입력할 커맨드
python3 1region-based_segmetation.py 

python3 2VanishingPoint.py 

python3 3SceneGrouping.py 

python3 4fine_Depthmap_v3.py ./output/seg_final.jpg ./output/sceneGrouping.jpg 437 259 
=> !!!!attention!!!!: 2번째 python 코드를 실행하면 나오는 소실점 좌표 입력 ex) 437 259 

python3 test.py 
=>rough 3d 모델과 이상치 제거된 final depth 모델

python3 customized_visualization.py  
=>K 키를 누르면 검정 배경  R키를 누르면 하얀 배경 .키를 누르면 3D 모델의 depth 캡쳐 ,키를 누르면 3D 모델의 gray image 캡쳐


