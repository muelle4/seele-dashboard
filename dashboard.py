# import necessary packages
import pandas as pd  
import plotly.express as px  
import streamlit as st
import datetime
from engine import *


# Configurations of Streamlit page
st.set_page_config(
    page_title = "S21 Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

@st.cache_data
def load_data():
    df = format_rcom_data(get_rcom_objects(DOMAIN_NAME, token, CLIENT_ID_SEELE, '067D7718-6C48-4517-AB80-5E6128BAC7C2', None, searchKey=None, searchValue=None, changedFrom=None, changedUntil=None)[KEY], get_rcom_bins(DOMAIN_NAME, token))
    return df

df = load_data()
df = df[df['warenausgang_projekt']=='1796']
df.reset_index(drop=True, inplace=True)


# dashboard title
st.title("S21 - Dashboard")


# create general chart
df_bar = build_frame(df)
fig0 = px.bar(
    df_bar, 
    x='RLA_Nummer',
    y='Material_kg',
    color='Status',
    width=1700,
    height=600
    )
st.write(fig0)

col1, col2 = st.columns(2)

with col1:
    df_bar1796 = bar_1796(df)
    fig1 = px.pie(
    df_bar1796,
    values='lieferscheine',
    names='ziel',
    labels='ziel',
    title='Lieferscheine RLA Projekt 1796',
    width=400
    ).update_traces(textinfo='value')
    st.write(fig1)

with col2:
    df_plz = plz(df)
    fig2 = px.pie(
    df_plz,
    values='counts',
    names='plz',
    labels='plz',
    title='Lieferscheine Standort Projekt 1796'
    ).update_traces(textinfo='value')
    st.write(fig2)

status = st.selectbox('Wähle Status', ['readytoship','shipped','warehouse', 'onsite', 'installed'])

if status == 'installed':
    df_hist = installed(df)
    st.write(
        px.bar(
            df_hist,
            x='week_installed',
            y='anzahl_lieferscheine',
            text='anzahl_lieferscheine',
            title='Anzahl Installationen nach Lieferscheinen & Woche',
            width=1700,
            height=600
            )
    )

elif status == 'onsite':
    df_onsite = onsite(df)
    st.write(
        px.bar(
            df_onsite,
            x='week_onsite',
            y='anzahl_lieferscheine',
            text='anzahl_lieferscheine',
            title='Anzahl onsite-Buchungen nach Lieferscheinen & Woche',
            width=1700,
            height=600
            )
    )
elif status == 'warehouse':
    df_ware = warehouse(df)
    st.write(
        px.bar(
            df_ware,
            x='week_warehouse',
            y='anzahl_lieferscheine',
            text='anzahl_lieferscheine',
            title='Anzahl warehouse-Buchungen nach Lieferscheinen & Woche',
            width=1700,
            height=600
        )
    )

else: None
            

            

