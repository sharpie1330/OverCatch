import streamlit as st
from PIL import Image

# set page
st.set_page_config(
    page_title="OVERCATCH",
    page_icon="🎮",
    layout="wide",
)
st.title("📑 WHAT IS THE OVERCATCH?")
st.subheader("Let me introduce our project📢")
with st.sidebar :
    code = '''
import random

members = [
'장규현😎',
'곽태영👻',
'김가연🕊️',
]

def hello():
    print("Hello, World!")
    print("We're TEAM BLUESCREEN")

    for i in range(0, 3):
        print(f'{i+1}번 감자 
            {random.randint(20000000, 
            20221026)} {members[i]}')
        if i == 2:
            print("번호 끝!")

hello()
-------------------------------------
>> Hello, World!
   We're TEAM BLUESCREEN
   1번 감자 20171119 장규현😎
   2번 감자 20181457 곽태영👻
   3번 감자 20191012 김가연🕊️
   번호 끝!
        '''
    st.code(code, language='python')

# load character images
ana = Image.open('ow_characters/ana.png')
bastion = Image.open('ow_characters/bastion.png')
cassidy = Image.open('ow_characters/cassidy.png')
lucio = Image.open('ow_characters/lucio.png')
mei = Image.open('ow_characters/mei.png')
reaper = Image.open('ow_characters/reaper.png')
roadhog = Image.open('ow_characters/roadhog.png')
soldier = Image.open('ow_characters/soldier-76.png')
sombra = Image.open('ow_characters/sombra.png')
torbjorn = Image.open('ow_characters/torbjorn.png')
zarya = Image.open('ow_characters/zarya.png')
zenyata = Image.open('ow_characters/zenyata.png')

# st.markdown("#### FPS 게임의 핵(Hack, Cheating)이란?")
st.text("\n\n")
st.markdown("##### ✨ FPS 게임의 핵(Hack, Cheat)이란?")
st.text("게임핵이란 게임에서 사용되는 부정행위 프로그램입니다. 게임핵을 사용하는 유저는 플레이 능력이 비정상적으로 향상되고, 이는 불공정한 보상과 재미 저하를 유발하며\n결국 유저 이탈로까지 이어집니다. 게임핵 사용은 건강한 게임 문화를 저해할 뿐 아니라, 보안 문제까지 야기합니다. 게임핵으로 인한 문제가 대두된지 오래지만,\n게임핵 사용유무를 구별해내는 기술과 인력의 한계로 아직도 많은 유저와 개발사 및 유통사가 게임핵으로 인해 발생한 피해를 고스란히 감당하고 있는 현실입니다. \n2018년 게임물관리위원회가 실시한 [2018 불법 프로그램 피해 실태 조사 연구]에 따르면 국내 게임업계 매출 12조 중 피해액이 2.4조로 집계됐습니다. 즉, 불법\n프로그램으로 인한 피해가 전체 매출 규모 중 1/6 이상 차지하므로 결코 무시할 수 없는 수준임을 확인할 수 있습니다.")
st.text("\n")

st.markdown("##### ✨ OVERCATCH와 기존 안티 치트(Anti-Cheat) 프로그램의 차이점")
st.text("기존 시스템 대부분은 확보부터 분석까지 완료된 해킹 툴의 핵심 코드나 패턴 자체를 등록하는 방식으로 동작합니다. 하지만 해킹툴을 우회하거나, 서버와 클라이언트 \n사이에서 주고 받는 패킷을 하이재킹(Hijacking)하는 방식의 게임핵 사용에는 취약합니다.\n본 프로젝트 <OVERCATCH>는 기존의 시스템적인 한계를 극복하도록 고안됐습니다. OVERCATCH는 게임 플레이 영상으로 에임핵(FPS게임에서 총의 조준점을 조작하는\n게임핵의 일종)을 영상처리와 딥러닝을 통해 검출합니다. 킬캠(killcam, 캐릭터가 사망하기 직전 20~30초 가량의 플레이 영상)은 유저가 게임사 측에 핵 의심 유저를\n리포트할 때 함께 전송하는 데이터입니다. 현시점에서 핵유저를 구별하는 작업에 활발히 사용되고 있는 킬캠 영상 데이터를 분석해서 핵 사용 여부를 추론합니다.")
st.text("\n")

st.markdown("##### ✨ 캐릭터 제한")
st.text("이펙트와 파티클이 난무하는 화려한 게임 그래픽 특성상 유의미한 객체 검출 정확도를 내려면 평균치보다 훨씬 다변형적이고 고품질인 다량의 학습 데이터가 필요합니다.\n제한된 기간 이내에 YOLOv5의 유의미한 정확도를 확보하기 위해서 오버워치 전체 캐릭터 35명 중 아래 12명만 모델 학습에 사용했습니다. 핵 판별을 위한 파트 단위 \n분리에 사용된 킬사인(kill-sign) 클래스까지 도합 13개 클래스의 데이터셋을 전부 직접 제작했습니다.\nTEAM BLUESCREEN에서 제작한 OVERWATCH Characters Custom Datasets(public)은 총 13개 클래스와 약 60,000개의 이미지 데이터로 이루어져 있습니다.\n본 데이터셋은 Roboflow를 통해 공식적으로 이용 가능합니다.")

c1, c2, c3 = st.columns(3)
with c1:
    st.image(ana, caption='Ana')
with c2:
    st.image(bastion, caption='Bastion')
with c3:
    st.image(cassidy, caption='Cassidy')
c4, c5, c6 = st.columns(3)
with c4:
    st.image(lucio, caption='Lucio')
with c5:
    st.image(mei, caption='Mei')
with c6:
    st.image(reaper, caption='Reaper')
c7, c8, c9 = st.columns(3)
with c7:
    st.image(roadhog, caption='Roadhog')
with c8:
    st.image(soldier, caption='Slodier-76')
with c9:
    st.image(sombra, caption='Sombra')
c10, c11, c12 = st.columns(3)
with c10:
    st.image(torbjorn, caption='Torbjorn')
with c11:
    st.image(zarya, caption='Zarya')
with c12:
    st.image(zenyata, caption='Zenyata')
st.text("\n")

st.markdown("##### ✨ 에임핵 추론 과정 >> YOLOv5 + LSTM")
st.text("YOLOv5로 오버워치 게임 플레이 영상에서 캐릭터 객체를 검출합니다. 검출된 캐릭터의 머리 부근과 화면 중앙 조준점(에임) 사이 거리를 계산합니다.\n저장된 거리 데이터는 게임핵을 사용한 영상과 사용하지 않은 영상의 차이를 특정할 수 있는 피처로 활용됩니다. 게임핵은 캐릭터 머리 쪽에 조준경을\n강제적으로 위치시키므로, 조준점과 캐릭터 머리 사이 거리가 비교적 일정하게 유지되는 경향을 보이리라 예상할 수 있습니다.\n상대 캐릭터를 제거하면 빨간 해골 그림의 킬사인이 중앙에 나타납니다. 킬사인이 검출된 해당 프레임을 기준으로 직전 30 프레임의 거리 데이터에\n각각 가중치를 부여해서 제거한 타겟으로 추정되는 캐릭터를 특정합니다.\n일반적으로 한 플레이 영상에서 킬 사인 여러 개가 검출되므로, 타겟 캐릭터의 킬사인 직전 30 프레임에서 추출한 피처를 LSTM에 입력합니다.\nLSTM은 30 프레임 단위 거리 피처 각각에 대해 0과 1 사이의 값을 할당합니다. LSTM에서 도출된 결과들의 평균을 구한 뒤, 임계값 0.5를 기준으로\n이상이면 핵, 미만이면 핵이 아님으로 판단합니다.")
