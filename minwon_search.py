#!/usr/bin/env python
# coding: utf-8

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[74]:


import pandas as pd
import numpy as np
import json
from datetime import datetime
from konlpy.tag import Okt
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib


# 검색어의 토픽을 정하기위해 기존에 fit된 LDA와 CounterVectorizer를 불러온다

# In[8]:


lda = joblib.load('minwon_lda.pkl')
query_tf = joblib.load('minwon_query_tf.pkl')


# In[81]:


def set_query_topic(Q):
    """
    Q: 검색어 (str)
    return : topic번호 (0~14)
    """
    Q_ = [Q]
    query_tf_matrix = query_tf.fit_transform(Q_)
    t = lda.transform(query_tf_matrix)
    tnum=int(np.where(t[0]==max(t[0]))[0][0])
    
    if tnum==0 or tnum==1:
        return 0
    elif tnum==2 or tnum==3 or tnum==8:
        return 1
    elif tnum==4 or tnum==20:
        return 2
    elif tnum==5 or tnum==6 or tnum==7:
        return tnum-2
    elif tnum==9:
        return 6
    elif tnum==10 or tnum==13:
        return 7
    elif tnum==11 or tnum==12:
        return tnum-3
    elif tnum==14 or tnum==19:
        return 10
    else:
        return tnum-4


# In[76]:


def district_stats(data,topic):
    """
    data : DB에서 불러온 1년치데이터로 만들어진 DataFrame
    topic : 검색어가 속한 토픽의 번호(0~14)
    return : 토픽번호(int), 토픽이름(str), 지역구별 해당토픽의 비율(numpy.ndarray)
    """
    
    districtNo = {"강서구":2 , "강남구":3, "강동구":4, "강북구":5,
               "관악구":6, "광진구":7, "구로구":8, "금천구":9,
               "노원구":10, "도봉구":11, "동대문구":12, "동작구":13,
               "마포구":14, "서대문구":15, "서초구":16, "성동구":17,
                "성북구":18, "송파구":19, "양천구":20, "영등포구":21,
                "용산구":22, "은평구":23, "종로구":24, "중구":25, "중랑구":26}
    
    topicNames = {0:"교통", 1:"기타", 2:"건축", 3:"흡연", 4:"서류,등록", 5:"불법,단속",
            6:"주차", 7:"가정,복지,동물", 8:"문화,체육", 9:"쓰레기", 10:"주거,아파트,재건축",
            11:"공사,소음", 12:"고객 응대", 13:"시설물 설치", 14:"위생"}
    
    #지역구별로 데이터프레임 생성.
    districtDataFrames = [data[data.site_no==v] for v in districtNo.values()]
    
    totalResult = []
    for df in districtDataFrames:
        temp=[]
        for i in range(0,15):
            temp.append(len([_ for _ in df.topic if _==i]))
        totalResult.append(tuple(temp))
    topicResult = np.array([_[topic] for _ in totalResult])
    topicName = topicNames[topic]
    
    zipbObj = zip(districtNo.keys(), topicResult/max(topicResult))
    result=dict(zipbObj)
    final =list()
    for i in result.keys():
        temp={"name":i,"rate":result[i]}
        final.append(temp)
    
    result = {"topic":topic,"topicName":topicName,"result":final}
    json_result = json.dumps(result, indent="  ",ensure_ascii=False)    
    return json_result


# In[63]:


def monthly_topic_stats(data,district,topic):
    """
    data : DB에서 불러온 1년치데이터로 만들어진 DataFrame
    district : 사용자가 클릭한 지역이름 ex)'송파구'
    topic : 검색어가 속한 토픽의 번호(0~14)
    return : 선택한 지역에서 1년간 해당토픽의 민원이 발생한 수(list)
    
    """
    
    districtNo = {"강서구":2 , "강남구":3, "강동구":4, "강북구":5,
           "관악구":6, "광진구":7, "구로구":8, "금천구":9,
           "노원구":10, "도봉구":11, "동대문구":12, "동작구":13,
           "마포구":14, "서대문구":15, "서초구":16, "성동구":17,
            "성북구":18, "송파구":19, "양천구":20, "영등포구":21,
            "용산구":22, "은평구":23, "종로구":24, "중구":25, "중랑구":26}
    
    data = data[data.site_no==districtNo[district]]
    
    now = datetime.now()
    dateList = []
    y = now.year
    m = now.month
    
    while len(dateList)<12:
        if m>0:
            dateList.append(str(y)+'-'+'{0:02d}'.format(m%12))
        elif m==0:
            y_ = y-1
            dateList.append(str(y_)+'-'+'{0:02d}'.format(m+12))
        else:
            y_ = y-1
            dateList.append(str(y_)+'-'+'{0:02d}'.format(m%12))
        m -=1
    
    
    monthlyDataFrames=[]    #최근 12개월의 데이터를 각각 1개월씩 데이터프레임으로 만들어 배열에저장
    for m in dateList:
        monthlyDataFrames.append(data[[_.startswith(m) for _ in data.date]])
    totalResult=[]    #최근 12개월의 민원중 해당 토픽의 민원의 갯수를 월별로 저장

    for df in monthlyDataFrames:
        totalResult.append(len([_ for _ in df.topic if _==topic]))

    result = {"date":dateList, "total":totalResult}
    df = pd.DataFrame(result)
    df.date = pd.to_datetime(df.date)
    return df


def set_keyword(Q,M):
    Q_ = [_[0] for _ in M.pos(Q) if _[1].startswith('N') and len(_[0]) > 1]

    return ' '.join(Q_)

