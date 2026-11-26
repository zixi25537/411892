import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang TC', 'Microsoft JhengHei', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

FILE = 'records.json'

def load_records():
    if not os.path.exists(FILE):
        return []
    with open(FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_records(records):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

st.title('💰 我的零用錢記帳本')

records = load_records()

# ---- 三個分頁 ----
tab1, tab2, tab3 = st.tabs(['✏️ 記一筆', '📋 明細', '📊 統計'])

with tab1:
    with st.form('add_form', clear_on_submit=True):
        date = st.date_input('日期')
        kind = st.radio('收入還是支出？', ['支出', '收入'], horizontal=True)
        category = st.selectbox('類別', ['飲食', '交通', '娛樂', '文具', '零用錢', '其他'])
        item = st.text_input('項目', placeholder='例如：珍奶')
        amount = st.number_input('金額', min_value=0, step=10)
        submitted = st.form_submit_button('記下來')

    if submitted:
        if item == '' or amount == 0:
            st.error('項目和金額都要填喔！')
        else:
            records.append({'日期': str(date), '收支': kind, '類別': category,
                            '項目': item, '金額': amount})
            save_records(records)
            st.success(f'已記下：{item} {amount} 元')

# ---- 側邊欄：選月份（放在存檔之後，剛記的那筆才會算進去）----
months = []
for r in records:
    m = r['日期'][:7]   # '2026-11-19' 取前 7 個字 → '2026-11'
    if m not in months:
        months.append(m)
months.sort()

month = st.sidebar.selectbox('要看哪個月？', ['全部'] + months)
if month == '全部':
    shown = records
else:
    shown = [r for r in records if r['日期'][:7] == month]

with tab2:
    income = 0
    expense = 0
    for r in shown:
        if r['收支'] == '收入':
            income += r['金額']
        else:
            expense += r['金額']

    col1, col2, col3 = st.columns(3)
    col1.metric('總收入', f'{income} 元')
    col2.metric('總支出', f'{expense} 元')
    col3.metric('餘額', f'{income - expense} 元')

    st.dataframe(shown)

    # ---- 刪除記錯的那一筆 ----
    if records:
        st.subheader('刪除一筆')
        labels = []
        for r in records:
            labels.append(f"{r['日期']} {r['項目']} {r['金額']} 元")
        i = st.selectbox('選擇要刪除的記錄', range(len(records)),
                         format_func=lambda i: labels[i])
        if st.button('刪除'):
            records.pop(i)
            save_records(records)
            st.rerun()   # 立刻重跑，讓畫面跟著更新

    # ---- 下載備份 ----
    st.download_button('下載備份 (records.json)',
                       json.dumps(records, ensure_ascii=False, indent=2),
                       file_name='records.json')

with tab3:
    st.subheader('錢都花到哪裡去了？')
    totals = {}
    for r in shown:
        if r['收支'] == '支出':
            totals[r['類別']] = totals.get(r['類別'], 0) + r['金額']

    if totals:
        fig, ax = plt.subplots()
        ax.pie(list(totals.values()), labels=list(totals.keys()), autopct='%1.0f%%')
        st.pyplot(fig)
    else:
        st.info('還沒有支出記錄')

    st.subheader('餘額變化')
    if shown:
        shown_sorted = sorted(shown, key=lambda r: r['日期'])
        changes = []
        for r in shown_sorted:
            if r['收支'] == '收入':
                changes.append(r['金額'])
            else:
                changes.append(-r['金額'])
        balance = np.cumsum(changes)

        fig, ax = plt.subplots()
        ax.plot(range(1, len(balance) + 1), balance, marker='o')
        ax.axhline(0, color='red', linewidth=1)
        ax.set_xlabel('第幾筆')
        ax.set_ylabel('餘額（元）')
        st.pyplot(fig)
