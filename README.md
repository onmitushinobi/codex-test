# 画像一括変換ツール（最小構成）

`images/` 内の JPG/JPEG を読み込み、`out/` に **1536x1024 の JPG** として連番保存する Python スクリプトです。

- 元画像は変更しません（読み取りのみ）
- 削除処理はありません
- まず `--dry-run` で実行予定一覧を確認できます

## 1) Python がない場合（Windows）

### 方法A: 公式インストーラー
1. https://www.python.org/downloads/windows/ から最新版をダウンロード
2. インストール時に **Add Python to PATH** にチェック
3. PowerShell で確認:

```powershell
python --version
```

### 方法B: winget

```powershell
winget install Python.Python.3.12
python --version
```

## 2) セットアップ

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3) 使い方

### 3-1. dry-run（実行せず一覧表示）

```powershell
python process_images.py --input images --output out --dry-run
```

### 3-2. 本実行

```powershell
python process_images.py --input images --output out
```

## 出力仕様

- 出力サイズ: `1536x1024`
- 形式: JPEG
- ファイル名: `0001.jpg`, `0002.jpg`, ...（連番）
- 並び順: ファイル名のアルファベット順

## オプション

```powershell
python process_images.py --help
```

主なオプション:
- `--input` 入力フォルダ（既定: `images`）
- `--output` 出力フォルダ（既定: `out`）
- `--width` / `--height` 出力サイズ変更（既定: `1536x1024`）
- `--start-number` 連番開始番号（既定: `1`）
- `--dry-run` 実行予定のみ表示（保存しない）

## 失敗時の見方

スクリプトは失敗時に以下の順で表示します。

1. `[ERROR]` 何が失敗したか
2. `[CAUSE]` 原因の詳細
3. `[FIX]` 修正案

例:
- 入力フォルダがない
- JPG/JPEG が1枚もない
- 画像ファイルが壊れている / 他アプリがロックしている
