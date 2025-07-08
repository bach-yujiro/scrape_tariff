<div align="center">
  <!-- 使用技術シールド -->
  <p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge" alt="Python">
    <img src="https://img.shields.io/badge/-requests-000000.svg?logo=requests&style=for-the-badge" alt="requests">
    <img src="https://img.shields.io/badge/-BeautifulSoup4-FF5733.svg?logo=beautifulsoup&style=for-the-badge" alt="BeautifulSoup4">
    <img src="https://img.shields.io/badge/-pandas-150458.svg?logo=pandas&style=for-the-badge" alt="pandas">
    <img src="https://img.shields.io/badge/-SQLite-003B57.svg?logo=sqlite&style=for-the-badge" alt="SQLite">
  </p>
</div>

---

## 目次

1. [プロジェクト概要](#プロジェクト概要)  
2. [スクレイピング対象サイト](#スクレイピング対象サイト)  
3. [特徴](#特徴)  
4. [環境](#環境)  
5. [インストール](#インストール)  
6. [使い方](#使い方)  
7. [ディレクトリ構成](#ディレクトリ構成)  
8. [トラブルシューティング](#トラブルシューティング)  
---

## プロジェクト概要

日本税関のHSコード（品目分類番号）および対応関税率を自動スクレイピングし、  
CSV および SQLite データベースにまとめるCLIツールです。  
ポライトクロールでサーバーへの負荷を軽減しつつ、9桁までの細分類コードを含む全データを取得します。

---

## スクレイピング対象サイト

- ベースURL: [https://www.customs.go.jp/tariff/2025_04_01/index.htm](https://www.customs.go.jp/tariff/2025_04_01/index.htm)  
- HTMLテーブル（第5番目の`<table>`要素）をパースし、HSコード階層と関税率情報を抽出  

---

## 特徴

- **全97類の自動取得**  
  - 1〜97類までのURLを動的生成し、順次クロール  
- **多階層コードの伝播補完**  
  - 6桁行の最終非空値を保持し、7〜9桁行へ自動補完  
- **CSV & SQLite 出力**  
  - `import_tariff_all_filled.csv`  
  - `import_tariff.db`（SQLite）  
- **ポライトクロール**  
  - リクエスト間に1秒スリープを挿入  
- **拡張性**  
  - 将来的にJSON出力やPostgreSQL連携、コマンドライン引数対応可能  

---

## 環境

| 言語・ライブラリ       | バージョン     |
| ---------------------- | -------------- |
| Python                 | 3.8 以上       |
| requests               | 最新           |
| BeautifulSoup4         | 最新           |
| pandas                 | 最新           |
| sqlite3（標準ライブラリ） | —            |

---

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/<yourname>/tariff-scraper.git
cd tariff-scraper

# 仮想環境作成・有効化（例: venv）
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt
````

---

## 使い方

```bash
# カレントディレクトリで実行
python scrape_tariff.py
```

* 実行後、以下が生成されます：

  * `import_tariff_all_filled.csv`
  * `import_tariff.db`

### オプション例（未実装・拡張案）

```bash
python scrape_tariff.py \
  --sections 1 2 3 \
  --output-format json \
  --db-url postgresql://user:pass@localhost:5432/tariff_db \
  --verbose
```

---

## ディレクトリ構成

```
.
├── .gitignore
├── README.md
├── requirements.txt
├── scrape_tariff.py
├── import_tariff_all_filled.csv   # 実行後に生成
└── import_tariff.db               # 実行後に生成
```

---

## トラブルシューティング

* **テーブルが見つからない**

  * サイト構造が変わった場合、`scrape_tariff.py` 内の `tables[4]` インデックスを見直してください。
* **文字化け**

  * `r.encoding = "shift_jis"` が効かない場合、取得時のエンコーディング指定を手動で調整してください。
* **SQLite接続エラー**

  * ファイルパスやデータベース権限、`sqlite3` のバージョンを確認してください。
