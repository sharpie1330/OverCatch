import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
from pathlib import Path
from overcatch import OverCatch
import sys, os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# local path
filepath = ROOT
# 'C:/Python/repos_python/streamlit_bluescreen/bluescreen/'
# colab path
# filepath ='/content/streamlit_bluescreen/'

# set page
st.set_page_config(
    page_title="OVERCATCH",
    page_icon="🎮",
    layout="wide",
)
st.title("🎮 OVERCATCH")
# st.header("Let's do this!")
with st.sidebar :
    # st.markdown("## Catch the hack together🤘")
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
    
st.subheader("Step 1️⃣ Upload a video that you want to know")

# 폴더와 파일을 주면, 해당 폴더에 파일을 저장하는 함수
def save_uploaded_file(directory, file):
    # 폴더 확인
    if not os.path.exists(directory):
        os.makedirs(directory)
        # print("done to make directory")
    # 폴더에 파일 저장
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
        # print("done to save original video")
    return st.success('Saved file : {} in {}'.format(file.name, directory))

# 이렇게 해도 웹페이지 새로고침 시 데이터 데이터 초기화 됨 > DB 써야 해결될듯
if 'resultdict' not in st.session_state:
    st.session_state.resultdict = dict()

if 'latestvideo' not in st.session_state:
    st.session_state.latestvideo = ''

if 'seqdict' not in st.session_state:
    st.session_state.seqdict = dict()

if 'targetdict' not in st.session_state:
    st.session_state.targetdict = dict()

uploaded_file = st.file_uploader("Upload Video about a minute long", type=['mp4'])
if uploaded_file is not None:
    save_uploaded_file('original', uploaded_file)
    # print("done to video upload")

    # yolo > lstm 통과
    # result_dict에 file.name, percentage 저장 및 반환
    with st.spinner('YOLO is working pretty hard...'):
        # time.sleep(500)
        oc = OverCatch(uploaded_file.name)
        # float
        per, seq, chr = oc.predict()
        # print("YOLO IS DONE")
        # 모델 통과했다고 가정한 이후 코드. page2의 history gallery에 동일하게 사용
        st.session_state.resultdict[f"{uploaded_file.name}"] = per
        # print(st.session_state.resultdict)
        st.session_state.latestvideo = Path(f"{uploaded_file.name}").stem
        # print(st.session_state.latestvideo)
        st.session_state.seqdict[f'{st.session_state.latestvideo}'] = seq
        # print(st.session_state.seqdict)
        st.session_state.targetdict[f'{st.session_state.latestvideo}'] = chr
        # print(st.session_state.targetdict)
    st.success("YOLO IS DONE!")


if len(st.session_state.resultdict) != 0:
    # make a horizontal line
    st.write("〰️" * 62)
    st.subheader("Step 2️⃣ Watch this video")
    st.markdown("#### We truly created about 60,000 custom datasets for yolov5 model ourselves💦")
    
    # 영상 띄우기
    # st.markdown("### Finished to detect OVERWATCH characters using YOLOv5")
    fp = f"{filepath}/result/{str(Path(st.session_state.latestvideo).stem)}/{st.session_state.latestvideo}.mp4"
    # print("full file path : "+fp)

    st.markdown("<h1 style='text-align: center; color: grey;'>PLAY NOW 👇</h1>", unsafe_allow_html=True)

    video_file = open(fp, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    if uploaded_file is not None:
        with st.spinner('LSTM is working now...'):
            time.sleep(3)
        st.success('LSTM IS DONE!')

    hackper = st.session_state.resultdict[f"{st.session_state.latestvideo}.mp4"]
    df = pd.DataFrame(
        {
            "Normal": [1-hackper],
            "Hack": [hackper],
        }
    )

    st.write("〰️" * 62)
    st.subheader("Step 3️⃣ Lets check the probability of hack")

    left, right = st.columns((7,3))
    with left:
        st.text("\n")
        st.text("\n")
        st.text("\n")
        st.text("\n")
        chart_data = pd.DataFrame(
        data = st.session_state.seqdict[f'{st.session_state.latestvideo}'],
        columns = [st.session_state.targetdict[f'{st.session_state.latestvideo}']])
        st.line_chart(chart_data)
        # st.markdown(f'### It is {int(hackper*100)}% hack')

    with right:
        fig=px.bar(df, labels={'index': ' ', 'value':'percentage'})
        st.plotly_chart(fig, use_container_width=True)
    
    if hackper >= 0.5:
        st.markdown("<h2 style='text-align: center; color: #FF5733;'>☠️ Ohhhh WHAT THE HACK! 👮‍♂️</h2>", unsafe_allow_html=True)
        # st.markdown("## ☠️ _Hmmm.. THIS IS A CHEATER!_ 👮‍♂️")
    else: st.markdown("<h2 style='text-align: center; color: #DAF7A6;'>🍀 Hooooray! SUCH A NICE GAMER 🌞</h2>", unsafe_allow_html=True)
        # st.markdown("## 🍀 _SUCH A NICE GAMER_ 🌞")
    
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.write("〰️" * 62)



    # st.write(st.session_state.resultdict)