
import json
import os
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = "records.json"


# 讀取訂購紀錄
def load_records():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


# 儲存訂購紀錄
def save_records(records):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


# 新增訂單
def add_order(records):
    seat = int(input("請輸入座號："))
    name = input("請輸入姓名：")
    item = input("請輸入飲料品項：")
    price = float(input("請輸入金額："))

    order = {
        "seat": seat,
        "name": name,
        "item": item,
        "price": price
    }

    records.append(order)
    save_records(records)

    print("訂購成功！")


# 顯示所有訂單
def show_records(records):
    if not records:
        print("目前沒有訂購紀錄。")
        return

    print("\n===== 訂購紀錄 =====")

    for order in records:
        print(
            f"座號：{order['seat']} "
            f"姓名：{order['name']} "
            f"品項：{order['item']} "
            f"金額：{order['price']}"
        )


# 統計金額
def statistics(records):
    if not records:
        print("目前沒有訂購紀錄。")
        return

    prices = np.array([order["price"] for order in records])

    print("\n===== 金額統計 =====")
    print(f"訂單數量：{len(records)}")
    print(f"總金額：{np.sum(prices):.0f} 元")
    print(f"平均金額：{np.mean(prices):.2f} 元")
    print(f"最高金額：{np.max(prices):.0f} 元")
    print(f"最低金額：{np.min(prices):.0f} 元")


# 繪製統計圖
def draw_chart(records):
    if not records:
        print("目前沒有訂購紀錄。")
        return

    # 將同一個人的訂單合併
    totals = {}

    for order in records:
        name = order["name"]
        totals[name] = totals.get(name, 0) + order["price"]

    names = list(totals.keys())
    prices = np.array(list(totals.values()))

    plt.figure(figsize=(10, 5))
    plt.bar(names, prices)

    plt.title("Class Drink Order Statistics")
    plt.xlabel("Name")
    plt.ylabel("Total Price")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# 主程式
def main():
    records = load_records()

    while True:
        print("\n===== 班級飲料訂購系統 =====")
        print("1. 新增訂單")
        print("2. 查看訂單")
        print("3. 金額統計")
        print("4. 顯示統計圖")
        print("5. 離開程式")

        choice = input("請選擇功能：")

        if choice == "1":
            add_order(records)

        elif choice == "2":
            show_records(records)

        elif choice == "3":
            statistics(records)

        elif choice == "4":
            draw_chart(records)

        elif choice == "5":
            print("系統已關閉。")
            break

        else:
            print("無效的選項，請重新輸入。")


if __name__ == "__main__":
    main()
