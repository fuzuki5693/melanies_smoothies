# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # INSERT文に NAME_ON_ORDER カラムを追加
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        # 注文成功メッセージに名前を含める
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # --- APIの代わりにダミーデータを設定（forループ内で実行） ---
        dummy_data = {
            "family": "Cucurbitaceae",
            "genus": "Citrullus",
            "id": 25,
            "name": "Watermelon",
            "nutrition": {
                "carbs": 7.55,
                "fat": 0.15,
                "protein": 0.61,
                "sugar": 6.2
            },
            "order": "Cucurbitales"
        }
        
        # 選択されたフルーツごとにデータフレームを表示
        sf_df = st.dataframe(data=dummy_data, use_container_width=True)
