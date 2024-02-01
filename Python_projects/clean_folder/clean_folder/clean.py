import sys
import os
import shutil
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Потрібно вказати шлях до папки.")
        return

    source_folder = sys.argv[1]
    
    if not os.path.exists(source_folder):
        print("Зазначений шлях не існує.")
        return

    # Створюємо папку Files, куди будуть переміщені файли
    destination_folder = os.path.join(source_folder, "Files")
    os.makedirs(destination_folder, exist_ok=True)

    # Викликаємо функцію для сортування файлів у папці та її вкладених папках,
    # результат -  словник зі списками файлів по групам, відомі та невідомі скрипту розширення
    dict_files, extensions, unknown_extensions = sort_files(source_folder, destination_folder)
    print('Словник зі списками файлів по групам:')
    for key, value in dict_files.items():
        print(key, value)

    extensions = list(extensions)
    unknown_extensions = list(unknown_extensions)
    print('Розширення, відомі скрипту:    ', extensions)
    print('Розширення, невідомі скрипту:  ', unknown_extensions)

    print("Файли були відсортовані в папку 'Files'.")


def sort_files(source_folder, destination_folder):

    # Ініціалізуємо необхідні множини
    images, documents, audio, video, archives = set(), set(), set(), set(), set()
    extensions, unknown_extensions = set(), set()


    for root, dirs, files in os.walk(source_folder):
        # Метод walk() генерує імена файлів у дереві каталогів, проходячи по дереву зверху вниз або знизу вгору

        # Щоб не чіпати вже відсортовані файли, перевіримо на входження рядка 'Files' в рядок шляху до файлу
        if 'Files' not in root:

            for file in files:
                # Отримуємо шлях до файлу
                source_path = os.path.join(root, file) 
                        
                # Отримуємо розширення файлу
                file_extension = Path(file).suffix.upper()

                # Перевіряємо розширення
                if file_extension in ('.JPEG', '.PNG', '.JPG', '.SVG'):
                    # Переміщуємо файл згідно з розширенням у необхідну папку
                    move_file(source_path, destination_folder, 'images')
                    # Додаємо до необхідної колекції назву файлу
                    images.add(os.path.basename(source_path))
                    # Додаємо до колекції розширень  відоме скрипту розширення
                    extensions.add(file_extension)

                elif file_extension in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'):
                    move_file(source_path, destination_folder, 'documents')
                    documents.add(os.path.basename(source_path))
                    extensions.add(file_extension)

                elif file_extension in ('.MP3', '.OGG', '.WAV', '.AMR'):
                    move_file(source_path, destination_folder, 'audio')
                    audio.add(os.path.basename(source_path))
                    extensions.add(file_extension)

                elif file_extension in ('.AVI', '.MP4', '.MOV', '.MKV'):
                    move_file(source_path, destination_folder, 'video')
                    video.add(os.path.basename(source_path))
                    extensions.add(file_extension)

                elif file_extension in ('.ZIP', '.GZ', '.TAR'):
                    unpack_archive(source_path, destination_folder, 'archives')
                    archives.add(os.path.basename(source_path))
                    extensions.add(file_extension)
                else:
                    # Додаємо до колекції розширень  невідоме скрипту розширення
                    unknown_extensions.add(file_extension)

    # Перейменуємо папки за допомогою process_directory і файли за допомогою функції normalize
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            os.rename(source_path, normalize(source_path))

        for directory in dirs:
                if directory not in ('archives', 'video', 'audio', 'documents', 'images'):
                    process_directory(os.path.join(root, directory))

    # Створюємо словник з списками файлів по групам
    dict_files = {'images': list(images), 'documents': list(documents), 'audio': list(audio), 
                  'video': list(video),   'archives': list(archives)}
    
    return dict_files, extensions, unknown_extensions


def process_directory(directory_path):
    directory_name = os.path.basename(directory_path)
    normalized_name = normalize(directory_name)
    new_directory_path = os.path.join(os.path.dirname(directory_path), normalized_name)

    if new_directory_path != directory_path:
        # Перейменовуємо папку згідно функції normalize
        os.rename(directory_path, new_directory_path)

    if not os.listdir(new_directory_path):
        # Видаляємо шлях до каталогу
        os.rmdir(new_directory_path)


def move_file(source_path, destination_folder, category_folder):
    category_path = os.path.join(destination_folder, category_folder)
    os.makedirs(category_path, exist_ok=True)

    # Отримуємо ім'я файлу без шляху
    filename = os.path.basename(source_path)
    destination_path = os.path.join(category_path, filename)

    # Перевіряємо, чи файл вже знаходиться у відповідній папці, 
    # якщо ні то переміщуємо його у відповідну папку
    if not os.path.exists(destination_path):
        shutil.move(source_path, destination_path)


def unpack_archive(archive_path, destination_folder, category_folder):
    # Шлях куди розпаковуємо архів + створення папки
    category_path = os.path.join(destination_folder, category_folder)
    os.makedirs(category_path, exist_ok=True)
    
    # Отримуємо ім'я файлу без шляху
    filename = os.path.basename(archive_path)
    # Отримуємо ім'я файлу без розширення
    filename = str(filename).replace(Path(filename).suffix, '')
    # Кінцевий шлях куди розпаковуємо архів
    destination_path = os.path.join(category_path, filename)

    # Перевіряємо, чи файл вже знаходиться у відповідній папці
    if not os.path.exists(destination_path):
        # Розпаковуємо архів
        shutil.unpack_archive(archive_path, category_path) 
        # Видаляємо архів, який вже розпакували
        os.remove(archive_path)
        
        
def normalize(string):
    # Символи кирилиці, які треба замінити
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ "
    # Замінюємо на ці символи
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_")
    
    # Словник для перекладу
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION): 
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    
    # Транслітеруємо всі символи згідно зі вказаним словником 
    word = ""
    for ch in string:
        word += ch.translate(TRANS)

    return word


if __name__ == "__main__":
    main()
