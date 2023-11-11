import PySimpleGUI as sg
import os, sys
import convert_image_pdf

# 実行ファイルのパス
ROOT = os.path.dirname(sys.argv[0])
if ROOT == '': ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PDF_PATH = os.path.join(ROOT, 'images.pdf')
IMAGE_TYPES = '*.jpg;*.jpeg;*.jpe;*.heic'
# デフォルトパスにある画像をリストに追加
IMAGE_DIR = os.path.join(ROOT, 'pdf-in')
DEFAULT_IMAGES = []
if os.path.exists(IMAGE_DIR): # パスがあれば収集
    DEFAULT_IMAGES = [
        os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)
        if f.endswith('.jpeg') or f.endswith('.jpg') or 
            f.endswith('.heic') or f.endswith('.png')]
# 画面レイアウトを定義
frame_pdf_path = [
    [
        sg.InputText(DEFAULT_PDF_PATH, enable_events=True, key='-OUT-', size=(90,10)),
        sg.FileSaveAs('保存先の変更', file_types=(('PDFファイル', '*.pdf'),), target='-OUT-'),
    ]
]
frame_images = [
    [ sg.Listbox(DEFAULT_IMAGES, size=(100,10), enable_events=True, key='-LIST-') ],
    [
        sg.Button('画像を追加'),
        sg.Button('画像をクリア'),
    ],
]
frame_per_page = [
    [ sg.Combo(['2', '4', '6', '8'], default_value='6', key='-PERPAGE-')],
]
layout = [
    [ sg.Frame('画像の一覧', frame_images) ],
    [ sg.Frame('1ページに割付ける枚数', frame_per_page) ],
    [ sg.Frame('PDFの保存先', frame_pdf_path) ],
    [ sg.Button('PDF作成'), sg.Button('終了') ],
]
window = sg.Window('画像一覧からPDF作成ツール', layout)

# イベントループ
image_files = DEFAULT_IMAGES
while True:
    event, values = window.read()
    # print(f'event={event}, values={values}')
    if event in (None, '終了'):
        break
    if event == '保存先の変更':
        pass
    if event == '画像を追加':
        files = sg.popup_get_file(
            '画像を選択してください', 
            no_window=True, 
            file_types=(('画像ファイル', IMAGE_TYPES),),
            multiple_files=True)
        if files != None:
            image_files.extend(files)
            window['-LIST-'].update(image_files)
    if event == '画像をクリア':
        window['-LIST-'].update([])
        image_files = []
        continue
    if event == 'PDF作成':
        if image_files == []:
            sg.popup('画像を指定してください')
            continue
        pdf_path = values['-OUT-']
        per_page = int(values['-PERPAGE-'])
        print(f'PDF={pdf_path}')
        print(f'FILES={image_files}')
        print(f'PERPAGE={per_page}')
        sg.popup('PDFを作成します。少々お待ちください。')
        convert_image_pdf.convert_to_pdf(image_files, pdf_path, per_page)
        sg.popup('PDFを作成しました')
        break

window.close()
