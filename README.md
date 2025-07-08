<div align="center">
  <!-- 使用技術シールド -->
  <p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge" alt="Python">
    <img src="https://img.shields.io/badge/-requests-000000.svg?logo=requests&style=for-the-badge" alt="requests">
    <img src="https://img.shields.io/badge/-BeautifulSoup-FF5733.svg?logo=beautifulsoup&style=for-the-badge" alt="BeautifulSoup">
    <img src="https://img.shields.io/badge/-pandas-150458.svg?logo=pandas&style=for-the-badge" alt="pandas">
    <img src="https://img.shields.io/badge/-SQLite-003B57.svg?logo=sqlite&style=for-the-badge" alt="SQLite">
  </p>
</div>

---

## 目次

1. [プロジェクト概要](#プロジェクト概要)  
2. [特徴](#特徴)  
3. [環境](#環境)  
4. [インストール](#インストール)  
5. [使い方](#使い方)  
6. [ディレクトリ構成](#ディレクトリ構成)  
7. [トラブルシューティング](#トラブルシューティング)  
8. [貢献方法](#貢献方法)  
9. [ライセンス](#ライセンス)  

---

## プロジェクト概要

日本税関のHＳコード（品目分類番号）と対応関税率をスクレイピングし、CSV および SQLite データベースにまとめるCLIツールです。  
9桁までの細分類コードを含む全データを自動取得し、空欄を上位コードの値で埋める伝播処理を実装しています。 :contentReference[oaicite:4]{index=4}

---

## 特徴

- **全97類の自動取得**  
  1類～97類までのHTMLテーブルを順次クロールします。  
- **多階層コードの値伝播**  
  6～9桁のコードで欠損する関税率を、同じ6桁の上位レコードから自動補完。  
- **CSV & SQLite 出力**  
  `import_tariff_all_filled.csv` と `import_tariff.db` を生成。  
- **ポライトクロール**  
  1リクエストごとに 1秒待機し、サーバー負荷を軽減。  

---

## 環境

| 言語・ライブラリ       | バージョン     |
| ---------------------- | -------------- |
| Python                 | 3.8+           |
| requests               | 最新           |
| BeautifulSoup4         | 最新           |
| pandas                 | 最新           |
| sqlite3（標準ライブラリ） | —            |

> その他の依存は `requirements.txt` をご確認ください。:contentReference[oaicite:1]{index=1}

---

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/<yourname>/tariff-scraper.git
cd tariff-scraper

# 仮想環境の作成（例: venv）
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
````

---

## 使い方

```bash
# カレントディレクトリで実行すると、
# CSV と SQLite ファイルが生成されます。
python scrape_tariff.py
```

* 出力ファイル

  * `import_tariff_all_filled.csv`
  * `import_tariff.db`

---

## ディレクトリ構成

```
.
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ scrape_tariff.py
└─ import_tariff.db         # 実行後に生成
```

---

## トラブルシューティング

* **テーブルが見つからない**
  サイト構造変更時は `scrape_tariff.py` の `tables[4]` インデックスを確認。
* **文字化け**
  `r.encoding = "shift_jis"` が効かない場合は、手動でエンコード指定を見直してください。
* **SQLite接続エラー**
  ファイルパスや権限設定をチェック。

---

## 貢献方法

バグ報告や機能追加のご提案は Issue へ、Pull Request も歓迎します。テストケースやドキュメントの改善もぜひどうぞ。

---

## ライセンス

MIT License
