# images-to-pdf

大量の画像を1ページ4/6/8枚に割り付けてPDFに変換するプログラムです。

## 実行ファイルを使う方法

実行ファイルを使う場合、以下の手順で利用してください。

1. [release](https://github.com/kujirahand/images-to-pdf/releases)からZIPファイルをダウンロード
2. ZIPファイルを解凍して、`images-to-pdf.exe`を実行する

## コマンドラインから利用する場合

コマンドラインから利用する場合、Pythonをインストールしてある必要があります。

### 必要なライブラリのインストール

下記のコマンドを実行して、必要なPythonライブラリをインストールします。

```sh
# --- Windowsの場合 ---
python -m pip install -r requirements.txt
# --- macOS/Linuxの場合 ---
python3 -m pip install -r requirements.txt
```
### プログラムを実行する

以下のコマンドを実行します。

```sh
# --- Windowsの場合 ---
python images-to-pdf.py
# --- macOS/Linuxの場合 ---
python3 images-to-pdf.py
```
