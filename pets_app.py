import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

new_item_df = pd.read_csv("new_item_csv")
food_item_df = pd.read_csv("food_item_csv")
trimming_item_df = pd.read_csv("trimming_item_csv")
accessory_item_df = pd.read_csv("accessory_item_csv")
life_item_df = pd.read_csv("life_item_csv")
bird_item_df = pd.read_csv("bird_item_csv")

st.title("ペットショップサイトスクレイピングアプリ")
option = st.sidebar.selectbox(
    "表示するcsvファイルを選択してください",
    ("新商品", "フード・おやつ", "ケア・トリミングアイテム",
    "首輪・ウェア・アクセサリーアイテム", "生活用品アイテム",
    "小鳥・小動物アイテム"))

# new_item
if option == "新商品":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        new_item_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text1"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search1"
        )
    if new_item_query:
        if search_option == "先頭一致":
            bird_item_df = new_item_df[new_item_df["title"].str.startswith(new_item_query)]
        elif search_option == "部分一致":
            new_item_df = new_item_df[new_item_df["title"].str.contains(new_item_query, regex=False)]
        else:
            new_item_df = new_item_df
    st.write("## 新商品")
    st.write(new_item_df)

# food_item
if option == "フード・おやつ":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        food_item_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text2"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search2"
        )
    if food_item_query:
        if search_option == "先頭一致":
            food_item_df = food_item_df[food_item_df["title"].str.startswith(food_item_query)]
        elif search_option == "部分一致":
            food_item_df = food_item_df[food_item_df["title"].str.contains(food_item_query, regex=False)]
        else:
            food_item_df = food_item_df
    st.write("## フード・おやつ")
    st.write(food_item_df)

# trimming_item
if option == "ケア・トリミングアイテム":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        trimming_item_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text3"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search3"
        )
    if trimming_item_query:
        if search_option == "先頭一致":
            trimming_item_df = trimming_item_df[trimming_item_df["title"].str.startswith(trimming_item_query)]
        elif search_option == "部分一致":
            trimming_item_df = trimming_item_df[trimming_item_df["title"].str.contains(trimming_item_query, regex=False)]
        else:
            trimming_item_df = trimming_item_df
    st.write("## ケア・トリミングアイテム")
    st.write(trimming_item_df)

# accessory_item
if option == "首輪・ウェア・アクセサリーアイテム":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        accessory_item_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text4"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search4"
        )
    if accessory_item_query:
        if search_option == "先頭一致":
            accessory_item_df = accessory_item_df[accessory_item_df["title"].str.startswith(accessory_item_query)]
        elif search_option == "部分一致":
            accessory_item_df = accessory_item_df[accessory_item_df["title"].str.contains(accessory_item_query, regex=False)]
        else:
            accessory_item_df = accessory_item_df
    st.write("## 首輪・ウェア・アクセサリーアイテム")
    st.write(accessory_item_df)

# life_item
if option == "生活用品アイテム":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        life_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text5"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search5"
        )
    if life_query:
        if search_option == "先頭一致":
            life_item_df = life_item_df[life_item_df["title"].str.startswith(life_query)]
        elif search_option == "部分一致":
            life_item_df = life_item_df[life_item_df["title"].str.contains(life_query, regex=False)]
        else:
            life_item_df = life_item_df
    st.write("## 生活用品アイテム")
    st.write(life_item_df)

# bird_item_df
if option == "小鳥・小動物アイテム":
    col1, col2 = st.columns([3, 2])
    # col1
    with col1:
        bird_query = st.text_input(
            label="タイトル",
            help="商品名を入力してください",
            key="text6"
        )
        
    # col2
    with col2:
        search_option = st.selectbox(
            "検索方法",
            ("部分一致", "先頭一致"),
            key="search6"
        )
    if bird_query:
        if search_option == "先頭一致":
            bird_item_df = bird_item_df[bird_item_df["title"].str.startswith(bird_query)]
        elif search_option == "部分一致":
            bird_item_df = bird_item_df[bird_item_df["title"].str.contains(bird_query, regex=False)]
        else:
            bird_item_df = bird_item_df
    st.write("## 小鳥・小動物アイテム")
    st.write(bird_item_df)
