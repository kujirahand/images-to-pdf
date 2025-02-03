from PIL import Image
from PIL.ExifTags import TAGS
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.pdfgen import canvas
import tempfile
import os
import sys
import pillow_heif

# 画像をリサイズする関数
def resize_image(image, max_width, max_height):
    width, height = image.size
    # 新しいサイズを計算
    resize_ratio =  max_width / width
    if width < height:
        resize_ratio = max_height / height
    new_width = int(width * resize_ratio)
    new_height = int(height * resize_ratio)
    # 画像をリサイズ(LANCZOSを利用)
    image_r = image.resize((new_width, new_height), Image.LANCZOS)
    # (max_width, max_height)に貼り付ける
    image = Image.new('RGB', (max_width, max_height), (255,255,255))
    x = (max_width - new_width) // 2
    y = (max_height - new_height) // 2
    image.paste(image_r, (x, y))
    return image

# Exifを利用して画像の向きを回転
def change_image_rotation(img):
    exif_data = img._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            if TAGS.get(tag) == 'Orientation':
                if value == 3:
                    img = img.rotate(180, expand=True)
                elif value == 6:
                    img = img.rotate(-90, expand=True)
                elif value == 8:
                    img = img.rotate(90, expand=True)
    return img

def heic_jpg(image_path, save_path):
    heif_file = pillow_heif.read_heif(image_path)
    for img in heif_file: 
        image = Image.frombytes(
            img.mode,
            img.size,
            img.data,
            'raw',
            img.mode,
            img.stride,
        )
    image.save(save_path, "JPEG")

def open_image(image_file):
    if image_file.endswith('.heic') or image_file.endswith('.HEIC'): # .heic形式ならJPEGに変換
        base_dir = os.path.dirname(image_file)
        base_name = os.path.basename(image_file)
        image_file_jpg = os.path.join(base_dir, '___tmp___' + base_name + '.jpg')
        heic_jpg(image_file, image_file_jpg)
        image_file = image_file_jpg
    img = Image.open(image_file) # 画像をメモリに読む
    img = change_image_rotation(img) # 回転
    return img

def avalable_image_filter(f):
    f = f.lower()
    return f.endswith('.jpg') or \
        f.endswith('.jpeg') or f.endswith('.jpe') or \
        f.endswith('.png') or f.endswith('.heic') or \
        f.endswith('.bmp') or f.endswith('.gif')

def convert_to_pdf(image_files, pdf_path, per_page):
    # 画像ファイルのフィルタ
    image_files = list(filter(
        lambda f: not os.path.basename(f).startswith('___'), image_files))
    # 読み込み可能なファイル形式のみ残す
    image_files = list(filter(avalable_image_filter, image_files))
    image_files = list(sorted(image_files))
    # 縦画像が多いか横画像が多いか判定する
    portrait_nums = 0
    landscape_nums = 0
    for f in image_files:
        print(' - check: ', f)
        img = open_image(f)
        w, h = img.size
        if w > h:
            portrait_nums += 1
        else:
            landscape_nums += 1
    is_portrait = portrait_nums > landscape_nums
    if is_portrait:
        print('横向きの画像が多いです')
    else:
        print('縦向きの画像が多いです')
    # PDFファイルの作成と設定(A4)
    pagesize = portrait(A4)
    #      [0,1,2,3,4,5,6,7,8]
    rows = [0,1,2,0,2,0,3,0,4]
    cols = [0,1,1,0,2,0,2,0,2]
    revs = [0,1,0,0,1,0,0,0,0] # 縦横の個数を反転するか？
    if revs[per_page] == 1:
        is_portrait = not is_portrait
    if not is_portrait:
        pagesize = landscape(A4)
        rows, cols = cols, rows
    page = canvas.Canvas(pdf_path, pagesize=pagesize)
    width, height = pagesize
    image_rows = rows[per_page]
    image_cols = cols[per_page]
    print(f'PageSize={width:.1f},{height:.1f}')
    # A4に縦向き6枚(2x3)で配置するように計算
    margin_x, margin_y = 15, 15
    print("image_cols, image_rows=", image_cols, image_rows)
    image_width = (width - (image_cols+1) * margin_x) // image_cols
    image_height = (height - (image_rows+1) * margin_y) // image_rows
    # 画像をリサイズ、回転してPDFに貼り付け --- (*6)
    for idx, image_file in enumerate(image_files):
        if (idx % per_page == 0) and (idx > 0):
            page.showPage()  # 新しいページを開始
            print(' --- 改ページ ---')
        print(f' - {idx:03d}: {image_file}')
        i = idx % per_page
        # 写真の座標を計算 --- (*7)
        x = (i // image_rows) * (image_width + margin_x) + margin_x
        y = (i % image_rows) * (image_height + margin_y) + margin_y
        # 画像を読み込んでリサイズ
        img = open_image(image_file)
        img = resize_image(img, int(image_width * 4), int(image_height * 4))
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        img.save(temp_file.name, format='JPEG')
        # PDFのキャンバスに画像を貼り付け
        page.drawImage(temp_file.name, x, height - y - image_height, image_width, image_height)
        temp_file.close()
    # PDFファイルを保存
    page.save()
    print('* 以下のパスに保存しました:')
    print(pdf_path)
    print('* ご利用頂きましてありがとうございました。(^o^)')

def proc_cur_files():
    # フォルダ内のJPEGファイルを列挙
    root = os.path.dirname(sys.argv[0])
    image_folder = os.path.join(root, 'pdf-in')
    output_pdf = os.path.join(root, 'images.pdf')
    print('* 以下のパスにある画像ファイルを貼り付けます:')
    print(image_folder)
    image_files = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if avalable_image_filter(f)
    ]
    image_files.sort()
    convert_to_pdf(image_files, output_pdf, 4)

if __name__ == '__main__':
    proc_cur_files()
