
import json
import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = "records.json"

st.set_page_config(
    page_title="班級飲料訂購系統",
    page_icon="🥤",
    layout="wide"
)


# 讀取訂購紀錄
def load_records():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            return []

        return records

    except json.JSONDecodeError:
        return []


# 儲存訂購紀錄
def save_records(records):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


# 初始化資料
if "records" not in st.session_state:
    st.session_state.records = load_records()

records = st.session_state.records


# 網頁標題
st.title("🥤 班級飲料訂購系統")
st.caption("Class Drink Order System")

# 側邊欄選單
menu = st.sidebar.radio(
    "功能選單",
    ["新增訂單", "訂購紀錄", "金額統計", "統計圖表"]
)


# 新增訂單
if menu == "新增訂單":

    st.header("新增飲料訂單")

    with st.form("order_form"):

        seat = st.number_input(
            "座號",
            min_value=1,
            step=1
        )

        name = st.text_input("姓名")

        item = st.text_input("飲料品項")

        price = st.number_input(
            "金額（元）",
            min_value=0,
            step=5
        )

        submitted = st.form_submit_button("送出訂單")

        if submitted:

            if not name.strip() or not item.strip():
                st.error("請填寫姓名及飲料品項！")

            elif price <= 0:
                st.error("金額必須大於 0！")

            else:

                order = {
                    "seat": int(seat),
                    "name": name.strip(),
                    "item": item.strip(),
                    "price": float(price)
                }

                records.append(order)

                save_records(records)

                st.success("訂購成功！")


# 查看訂單
elif menu == "訂購紀錄":

    st.header("訂購紀錄")

    if records:

        st.dataframe(
            records,
            use_container_width=True
        )

        st.write(f"目前共有 {len(records)} 筆訂單")

    else:
        st.info("目前沒有訂購紀錄。")


# 金額統計
elif menu == "金額統計":

    st.header("金額統計")

    if records:

        prices = np.array(
            [order["price"] for order in records]
        )

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        col1.metric("訂單數量", len(records))
        col2.metric("總金額", f"{np.sum(prices):.0f} 元")

        col3.metric("平均金額", f"{np.mean(prices):.2f} 元")
        col4.metric("最高金額", f"{np.max(prices):.0f} 元")

        st.write(f"最低金額：{np.min(prices):.0f} 元")

    else:
        st.info("目前沒有訂購紀錄。")


# 統計圖表
elif menu == "統計圖表":

    st.header("個人訂購金額統計")

    if records:

        totals = {}

        for order in records:
            name = order["name"]
            totals[name] = totals.get(name, 0) + order["price"]

        names = list(totals.keys())
        prices = np.array(list(totals.values()))

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(names, prices)

        ax.set_title("Class Drink Order Statistics")
        ax.set_xlabel("Name")
        ax.set_ylabel("Total Price")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    else:
        st.info("目前沒有訂購紀錄。")
