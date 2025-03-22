from PIL import Image
import img2pdf
import os
import shutil

# Проверка и создание необходимых папок
def ensure_directories():
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "output")
    done_dir = os.path.join(current_dir, "done")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Создана папка: {output_dir}")
    
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)
        print(f"Создана папка: {done_dir}")

# Функция для разделения изображения на части
def split_image(image_path, chunk_height):
    img = Image.open(image_path)
    width, height = img.size
    
    # Создаем папку для chunk-ов этого скриншота
    chunk_dir = f"chunk_{os.path.basename(image_path)}"
    os.makedirs(chunk_dir, exist_ok=True)
    
    chunks = []
    for i in range(0, height, chunk_height):
        top = i
        bottom = min(i + chunk_height, height)
        # Проверяем, что высота куска >= 3
        chunk_height_actual = bottom - top
        if chunk_height_actual < 3:
            continue  # Пропускаем слишком маленькие куски
        
        chunk = img.crop((0, top, width, bottom))
        chunk_filename = os.path.join(chunk_dir, f"chunk_{i}.png")
        chunk.save(chunk_filename)
        chunks.append(chunk_filename)
    
    return chunks, chunk_dir

# Функция конвертации одного PNG в PDF
def convert_png_to_pdf(input_png, page_height=842):
    # Создаем имя выходного PDF файла на основе входного имени
    output_pdf = os.path.join("output", f"{os.path.splitext(input_png)[0]}.pdf")
    
    # Делим изображение на части и получаем список файлов и имя папки
    chunk_files, chunk_dir = split_image(input_png, page_height)
    
    # Проверяем, есть ли вообще валидные куски
    if not chunk_files:
        print(f"Ошибка: нет валидных кусков для {input_png} (слишком маленькое изображение)")
        shutil.rmtree(chunk_dir)
        return
    
    # Преобразуем все части в один PDF
    try:
        with open(output_pdf, "wb") as file:
            file.write(img2pdf.convert(chunk_files))
    except ValueError as e:
        print(f"Ошибка при создании PDF для {input_png}: {str(e)}")
        shutil.rmtree(chunk_dir)
        return
    
    # Удаляем временную папку с chunk-ами
    shutil.rmtree(chunk_dir)
    
    # Перемещаем оригинальный файл в папку done с добавлением "+"
    done_filename = os.path.join("done", f"+{input_png}")
    shutil.move(input_png, done_filename)
    
    print(f"PDF успешно сохранен как {output_pdf}")
    print(f"Оригинал перемещен в {done_filename}")

# Основной код для обработки всех PNG в текущей директории
def process_all_screenshots():
    # Проверяем и создаем папки
    ensure_directories()
    
    # Получаем текущую директорию
    current_dir = os.getcwd()
    
    # Поддерживаемые расширения изображений
    image_extensions = ('.png', '.PNG')
    
    # Список всех PNG файлов в текущей папке
    png_files = [f for f in os.listdir(current_dir) if f.endswith(image_extensions)]
    
    if not png_files:
        print("В текущей папке нет PNG файлов!")
        return
    
    print(f"Найдено {len(png_files)} скриншотов для обработки")
    
    # Обрабатываем каждый PNG файл
    for png_file in png_files:
        print(f"Обработка {png_file}...")
        convert_png_to_pdf(png_file)

# Запускаем обработку
if __name__ == "__main__":
    process_all_screenshots()