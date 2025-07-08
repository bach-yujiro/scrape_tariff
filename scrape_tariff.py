import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3
import time

BASE_URL = "https://www.customs.go.jp/tariff/2025_04_01/data/"
all_rows = []
columns = None

for i in range(1, 98):  # 01～97類
    fname = f"j_{i:02}.htm"
    url = BASE_URL + fname
    r = requests.get(url)
    r.encoding = "shift_jis"
    soup = BeautifulSoup(r.text, features="html.parser")
    tables = soup.find_all("table")
    if len(tables) < 5:
        print(f"{fname}：本体table見つからずスキップ")
        continue
    table = tables[4]
    trs = table.find_all("tr")
    if len(trs) < 3:
        print(f"{fname}：データ行少なくスキップ")
        continue

    header_tr = trs[1]
    header = [td.get_text(strip=True) for td in header_tr.find_all(['td', 'th'])]
    if columns is None:
        columns = ["hscode", "品名"] + header[2:-2]
        expected_colnum = len(columns)

    data_rows = trs[2:]
    last_names = {}
    prev_main_code = ""

    for tr in data_rows:
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue

        main_code = tds[0].get_text(strip=True).replace(".", "")
        sub_code = tds[1].get_text(strip=True).replace(".", "")
        if main_code == "":
            main_code = prev_main_code
        else:
            prev_main_code = main_code
        name_td = tds[2]
        name = name_td.get_text(strip=True)
        style = name_td.get("style") or ""
        match = re.search(r'padding-left\s*:\s*([0-9\.]+)em', style)
        em_level = int(float(match.group(1))) if match else 0
        hyphen_match = re.match(r'^(−+)', name)
        hyphen_level = len(hyphen_match.group(1)) if hyphen_match else 0
        level = em_level + hyphen_level
        last_names[level] = name
        full_name = '/'.join([last_names[l] for l in range(level+1) if l in last_names])
        rates = [td.get_text(strip=True) for td in tds[3:len(header)-2]]
        hscode = main_code + sub_code
        row = [hscode, full_name] + rates
        if len(row) < expected_colnum:
            row += [''] * (expected_colnum - len(row))
        all_rows.append(row)
    print(f"{fname} done ({len(data_rows)} data rows)")
    time.sleep(1)  # polite crawling

df = pd.DataFrame(all_rows, columns=columns)

# 3～8列目（Pythonではindex2～7）を順番に伝播処理
for col in df.columns[2:8]:
    current_hs6 = None
    current_val = None
    for idx, row in df.iterrows():
        hscode = str(row["hscode"])
        hs6 = hscode[:6]
        # 6,7,8,9桁のみが伝播対象
        if not (6 <= len(hscode) <= 9):
            continue
        cell_val = row[col]
        # 6桁の行で値があればソースを更新
        if len(hscode) == 6 and cell_val not in [None, ""]:
            current_hs6 = hs6
            current_val = cell_val
        # 6桁の行で空欄→埋める
        elif len(hscode) == 6 and cell_val in [None, ""] and current_hs6 == hs6 and current_val not in [None, ""]:
            df.at[idx, col] = current_val
        # 7-9桁で空欄→同じ6桁のソースがあれば埋める
        elif 7 <= len(hscode) <= 9 and current_hs6 == hs6 and cell_val in [None, ""] and current_val not in [None, ""]:
            df.at[idx, col] = current_val
        # 7-9桁でデータが入っていたら→絶対にそれをソースにはしない（スルー）

# 最後に7桁以上のhscodeのみ抽出
df = df[df["hscode"].str.len() > 6]

# CSVとSQLite出力
df.to_csv("import_tariff_all_filled.csv", index=False, encoding="utf-8-sig")
with sqlite3.connect("import_tariff.db") as conn:
    df.to_sql("import_tariff", conn, if_exists="replace", index=False)
print(df.head())
print(f"全{len(df)}件を出力しました。")
