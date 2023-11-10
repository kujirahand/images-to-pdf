# images-to-pdf

大量の画像を1ページ6枚に割り付けてPDFに変換するプログラム。

【使い方】

1. プログラムをダウンロードしてZIPを解凍します。
2. 「pdf-in」というフォルダにPDFに変換したい画像ファイル(JPEG)をコピーします。
3. 「images-to-pdf.exe」を実行します。
4. すると、images.pdfというファイルが作成されます。

もし、iPhoneの拡張子がHEICの画像ファイルがあるなら、最初に「heic-to-jpeg.exe」を実行してから「images-to-pdf.exe」を実行してください。

なお、pdf-inにある全ての画像ファイルを対象にするので、最初から入っているサンプル画像は削除してから使ってください。


## How to install

Pythonから実行する場合、以下のようにしてパッケージをインストールします。

```sh
python3 -m pip install -r requirements.txt
```

実行ファイルに変換する場合:

```sh
pyinstaller heic-to-jpeg.py --onefile
pyinstaller images-to-pdf.py --onefile
```

