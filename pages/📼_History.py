import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys, os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# local path
filepath = ROOT
# colab path
# filepath ='/content/streamlit-gallery/'

# set page
st.set_page_config(
    page_title="OVERCATCH",
    page_icon="🎮",
    layout="wide",
)
st.title("📼 OVERCATCH HISTORY")
st.subheader("Watch other cases 👀")
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

rd = st.session_state["resultdict"]
# st.write(rd)

sd = st.session_state["seqdict"]
# st.write(sd)

td = st.session_state["targetdict"]

keylist=[]
for key in rd:
    keylist.append(key)
# st.write(keylist)

valuelist=[]
for key in rd:
    valuelist.append(rd[key])
# st.write(valuelist)

seqkey=[]
for key in sd:
    seqkey.append(key)

seqlist=[]
for key in sd:
    # print(sd[key])
    seqlist.append(sd[key])
# st.write(seqlist)

targetlist=[]
for k in sd:
    targetlist.append(td[key])

keyindex=0
len = len(st.session_state["resultdict"])

def make_grid():
    global keyindex
    global len

    if len%2 == 0 :
        rows = int(len/2)
    else :
        rows = int(len/2)+1

    for i in range(0, rows):
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                tab1, tab2, tab3 = st.tabs(["🎬 video", "📊 hack percent", "📉 distance chart"])
            
                with tab1:
                    video_file = open(f'{filepath}/result/{str(Path(keylist[keyindex]).stem)}/{keylist[keyindex]}', 'rb')
                    #video_file = open(f'{filepath}/result/{str(os.path.splitext(keylist[keyindex])[0])}/{keylist[keyindex]}', 'rb')
                    video_bytes = video_file.read()
                    st.video(video_bytes)

                with tab2:
                    hackper = valuelist[keyindex]
                    df = pd.DataFrame(
                        {
                            "Normal": [1-hackper],
                            "Hack": [hackper],
                        }
                    )
                    if hackper >= 0.5:
                        st.markdown(f"HACK👎 by {(hackper*100):.2f} %")
                    else:
                        st.markdown(f"NORMAL👍by {((1-hackper)*100):.2f} %")
                    fig=px.bar(df, labels={'index': ' ', 'value':'percentage'})
                    st.plotly_chart(fig, use_container_width=True)

                with tab3:
                    chart_data = pd.DataFrame(
                    data = sd[seqkey[keyindex]],
                    columns = [targetlist[keyindex]])

                    st.line_chart(chart_data)
                    
                keyindex += 1
            
            with col2:
                if (i == rows-1) and (len%2 != 0):
                    st.empty()
                else:
                    tab4, tab5, tab6 = st.tabs(["🎬 video", "📊 hack percent", "📉 distance chart"])
            
                    with tab4:
                        video_file = open(f'{filepath}/result/{str(Path(keylist[keyindex]).stem)}/{keylist[keyindex]}', 'rb')
                        video_bytes = video_file.read()
                        st.video(video_bytes)

                    with tab5:
                        hackper = valuelist[keyindex]
                        df = pd.DataFrame(
                            {
                                "Normal": [1-hackper],
                                "Hack": [hackper],
                            }
                        )
                        if hackper >= 0.5:
                            st.markdown(f"HACK👎 by {(hackper*100):.2f} %")
                        else:
                            st.markdown(f"NORMAL👍by {((1-hackper)*100):.2f} %")
                        fig=px.bar(df, labels={'index': ' ', 'value':'percentage'})
                        st.plotly_chart(fig, use_container_width=True)  
                 
                    with tab6:
                        chart_data = pd.DataFrame(
                        data = sd[seqkey[keyindex]],
                        columns = [targetlist[keyindex]])

                        st.line_chart(chart_data)
                                
                    keyindex += 1

if len > 0:
    make_grid()