import requests
import random
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

# LINE Notify
line_notify_token = env_vars["LINE_NOTIFY_TOKEN"]
line_notify_url = "https://notify-api.line.me/api/notify"

# Google Form
google_form_url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSejEqgfujXlfICK8GlgUw2Hy6dQ0A5XrOkGdwzB_D8tzmNtew/formResponse"

# Google Form Fields
grade = ["大一", "大二", "大三", "大四", "碩士生"]
city = [
    "台北市",
    "新北市",
    "基隆市",
    "宜蘭縣",
    "桃園市",
    "新竹縣",
    "新竹市",
    "苗栗縣",
    "台中市",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義縣",
    "嘉義市",
    "台南市",
    "高雄市",
    "屏東縣",
    "台東縣",
    "花蓮縣",
    "外島地區",
]
frequency = ["不到一次", "一次", "二次", "三次", "四次", "四次以上"]
weekday = ["禮拜一", "禮拜二", "禮拜三", "禮拜四", "禮拜五", "禮拜六", "禮拜日"]
long_weekend = ["連假前一天", "連假當天", "連假第二天"]
transportation = ["客運", "高鐵", "火車", "公車", "自行開（騎）車", "家人接送"]  # multiple choice
transfer = ["不用轉乘", "1次", "2次", "3次", "3次以上"]
cost = ["20元", "30元", "40元", "50元", "50元以上"]
willingness = ["極高", "偏高", "普通", "偏低"]
reason = [
    "價格太高",
    "原返鄉交通工具就很方便",
    "需要預約覺得麻煩",
    "不確定性高",
    "發車時間可能無法配合行程",
    "可能造成身體不適（如暈車）",
]  # while willingness is "偏低" or "極低"
order_tool = ["自製app", "Line", "行動逢甲", "TBS(台北轉運站app)"]  # multiple choice

# Randomly select fields
selected_transportation = random.sample(
    transportation, k=random.randint(1, len(transportation))
)
transportation_field = (
    selected_transportation[0]
    if len(selected_transportation) == 1
    else selected_transportation
)
selected_order_tool = random.sample(order_tool, k=random.randint(1, len(order_tool)))
order_tool_field = (
    selected_order_tool[0] if len(selected_order_tool) == 1 else selected_order_tool
)

# Payload
payload = {
    "entry.569757960": random.choice(grade),
    "entry.153529343": random.choice(city),
    "entry.349660221": random.choice(frequency),
    "entry.1672787802": random.choice(weekday),
    "entry.1714558885": random.choice(long_weekend),
    "entry.826912473": transportation_field,
    "entry.1520536960": random.choice(transfer),
    "entry.1049499527": random.choice(cost),
    "entry.1119577828": random.choice(willingness),
    "entry.1154674286": order_tool_field,
}

# If willingness is "偏低" or "極低", randomly select reason
if payload["entry.1119577828"] == "偏低" or payload["entry.1119577828"] == "極低":
    selected_reason = random.sample(reason, k=random.randint(1, len(reason)))
    reason_field = selected_reason[0] if len(selected_reason) == 1 else selected_reason

    payload["entry.1720765411"] = reason_field
else:
    payload["entry.1720765411"] = ""

# Send POST request
response = requests.post(google_form_url, data=payload)


# Send LINE Notify
def send_line_notify():
    message = (
        f"\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n已成功填寫表單，填寫內容如下：\n"
    )
    for v in payload.values():
        message += f"{v}\n"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {"message": message}
    response = requests.post(line_notify_url, headers=headers, data=data)


# Check response status code
if response.status_code == 200:
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 填寫成功：", response.status_code)
    send_line_notify()
else:
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 發生錯誤，錯誤代碼：", response.status_code)
