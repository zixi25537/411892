
import json
import os
import streamlit as st
import numpy as np

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

    except (json.JSONDecodeError, FileNotFoundError):
        return []


# 儲存訂購紀錄
def save_records(records):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


# 初始化資料
if "records" not in st.session_state:
    st.session_state.records = load_records()

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

records = st.session_state.records


# 網頁標題
st.title("班級飲料訂購系統")
st.caption("Class Drink Order System")


# 側邊欄選單
menu = st.sidebar.radio(
    "功能選單",
    ["新增訂單", "訂購紀錄", "金額統計"]
)


# ==========================
# 新增訂單
# ==========================

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

                st.session_state.records.append(order)

                save_records(st.session_state.records)

                st.success("訂購成功！")


# ==========================
# 查看訂單
# ==========================

elif menu == "訂購紀錄":

    st.header("訂購紀錄")

    if records:

        st.dataframe(
            records,
            use_container_width=True
        )

        st.write(f"目前共有 {len(records)} 筆訂單")

        # 清空訂單
        if st.button("清空所有訂單", type="primary"):

            st.session_state.confirm_delete = True

        # 二次確認
        if st.session_state.confirm_delete:

            st.warning("確定要清空所有訂單嗎？此操作無法復原！")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("確定清空"):

                    st.session_state.records = []
                    st.session_state.confirm_delete = False

                    save_records([])

                    st.success("所有訂單已清空！")
                    st.rerun()

            with col2:
                if st.button("取消"):

                    st.session_state.confirm_delete = False
                    st.rerun()

    else:
        st.info("目前沒有訂購紀錄。")


# ==========================
# 金額統計
# ==========================

elif menu == "金額統計":

    st.header("金額統計")

    if records:

        prices = np.array(
            [order["price"] for order in records]
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "訂單數量",
            len(records)
        )

        col2.metric(
            "總金額",
            f"{np.sum(prices):.0f} 元"
        )

        col3, col4 = st.columns(2)

        col3.metric(
            "平均金額",
            f"{np.mean(prices):.2f} 元"
        )

        col4.metric(
            "最高金額",
            f"{np.max(prices):.0f} 元"
        )

        st.write(
            f"最低金額：{np.min(prices):.0f} 元"
        )

    else:
        st.info("目前沒有訂購紀錄。")
