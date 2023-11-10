from PIL import Image
from PIL.ExifTags import TAGS
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.pdfgen import canvas
import tempfile, os
import sys
import pillow_heif
# 

# フォルダ内のJPEGファイルを列挙
root = os.path.dirname(sys.argv[0])
image_folder = os.path.join(root, 'pdf-in')
output_pdf = os.path.join(root, 'images.pdf')

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
    image = Image.new('RGB', (max_width, max_height), (0,0,0))
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

def convert():
    print('* 以下のパスにある画像ファイルを貼り付けます:')
    print(image_folder)
    image_files = [
        f for f in os.listdir(image_folder)
        if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.heic')]
    image_files.sort()

    # PDFファイルの作成と設定(A4縦向きにする) --- (*2)
    c = canvas.Canvas(output_pdf, pagesize=portrait(A4))
    width, height = portrait(A4)
    print(f'PageSize={width:.1f},{height:.1f}')

    # A4に縦向き6枚(2x3)で配置するように計算 --- (*3)
    margin_x, margin_y = 10, 60
    image_width = (width - 3 * margin_x) // 2
    image_height = (height - 4 * margin_y) // 3

    # 画像をリサイズ、回転してPDFに貼り付け --- (*6)
    for idx, image_file in enumerate(image_files):
        # 一時ファイルをスキップ
        if image_file == '': continue
        if len(image_file) > 3 and image_file[0:3] == '___': continue
        print(f' - {idx:03d}: {image_file}')
        if (idx % 6 == 0) and (idx > 0):
            c.showPage()  # 新しいページを開始
        i = idx % 6
        # 写真の座標を計算 --- (*7)
        x = (i // 3) * (image_width + margin_x) + margin_x
        y = (i % 3) * (image_height + margin_y) + margin_y
        # 画像を読み込んでリサイズ
        if image_file.endswith('.heic'):
            image_file_jpg = '___tmp___' + image_file + '.jpg'
            heic_jpg(os.path.join(image_folder, image_file), os.path.join(image_folder, image_file_jpg))
            image_file = image_file_jpg
        img = Image.open(os.path.join(image_folder, image_file))
        img = change_image_rotation(img)
        img = resize_image(img, int(image_width * 4), int(image_height * 4))
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        img.save(temp_file.name, format='JPEG')
        # PDFのキャンバスに画像を貼り付け
        c.drawImage(temp_file.name, x, height - y - image_height, image_width, image_height)
        temp_file.close()
    # PDFファイルを保存
    c.save()
    print('* 以下のパスに保存しました:')
    print(output_pdf)
    print('* ご利用頂きましてありがとうございました。(^o^)')

if __name__ == '__main__':
    convert()
