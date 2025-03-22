from PIL import Image
import os

def split_png_to_a4(input_path, output_dir):
    img = Image.open(input_path)
    width, height = img.size
    a4_width = 2480
    a4_height = 3508
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pages = (height + a4_height - 1) // a4_height
    temp_files = []
    for i in range(pages):
        top = i * a4_height
        bottom = min((i + 1) * a4_height, height)
        cropped = img.crop((0, top, width, bottom))
        a4_img = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
        paste_x = (a4_width - width) // 2
        paste_y = 0
        a4_img.paste(cropped, (paste_x, paste_y))
        temp_path = os.path.join(output_dir, f'page_{i+1}.png')
        a4_img.save(temp_path, 'PNG')
        temp_files.append(temp_path)
    pdf_path = os.path.splitext(input_path)[0] + '_split.pdf'
    first_page = Image.open(temp_files[0])
    first_page.save(
        pdf_path,
        'PDF',
        resolution=300.0,
        save_all=True,
        append_images=[Image.open(f) for f in temp_files[1:]]
    )
    for temp_file in temp_files:
        os.remove(temp_file)
    return pdf_path

if __name__ == "__main__":
    input_file = "screenshot.png"
    output_directory = "output"
    try:
        result = split_png_to_a4(input_file, output_directory)
        print(f"PDF успешно создан: {result}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
