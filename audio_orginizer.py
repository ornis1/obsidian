import os
import shutil
from pathlib import Path

def organize_audio_files(root_directory):
    """
    Рекурсивно проходит по папкам, находит mp3 файлы,
    ищет соответствующие md файлы и организует их в папки.
    
    Args:
        root_directory (str): Путь к корневой папке для поиска
    """
    
    # Счетчики для статистики
    processed = 0
    not_found = 0
    errors = 0
    
    # Проходим по всем папкам и подпапкам рекурсивно
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Ищем все mp3 файлы в текущей папке
        mp3_files = [f for f in filenames if f.lower().endswith('.mp3')]
        
        for mp3_file in mp3_files:
            try:
                mp3_path = os.path.join(dirpath, mp3_file)
                
                # Получаем имя файла без расширения
                mp3_name = os.path.splitext(mp3_file)[0]
                md_file = f"{mp3_name}.md"
                md_path = os.path.join(dirpath, md_file)
                
                # Проверяем наличие соответствующего md файла в той же папке
                if os.path.exists(md_path):
                    # Создаем папку с названием mp3 файла
                    new_folder = os.path.join(dirpath, mp3_name)
                    
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                        print(f"✓ Создана папка: {mp3_name}")
                    else:
                        print(f"~ Папка уже существует: {mp3_name}")
                    
                    # Перемещаем mp3 файл и переименовываем в audio.mp3
                    new_mp3_path = os.path.join(new_folder, 'audio.mp3')
                    if not os.path.exists(new_mp3_path):
                        shutil.move(mp3_path, new_mp3_path)
                    
                    # Перемещаем md файл и переименовываем в transcribe.md
                    new_md_path = os.path.join(new_folder, 'transcribe.md')
                    if not os.path.exists(new_md_path):
                        shutil.move(md_path, new_md_path)
                    
                    print(f"  → Перемещены файлы в папку '{mp3_name}'")
                    processed += 1
                else:
                    print(f"✗ Не найден md файл для: {mp3_file}")
                    not_found += 1
                    
            except Exception as e:
                print(f"✗ Ошибка при обработке {mp3_file}: {str(e)}")
                errors += 1
    
    # Выводим статистику
    print("\n" + "="*50)
    print("СТАТИСТИКА:")
    print(f"Обработано пар файлов: {processed}")
    print(f"MD файлов не найдено: {not_found}")
    print(f"Ошибок: {errors}")
    print("="*50)


def main():
    """Главная функция для взаимодействия с пользователем"""
    print("Организатор аудиофайлов")
    print("-" * 50)
    
    # Запрашиваем путь к папке
    root_dir = input("Введите путь к папке (или нажмите Enter для текущей папки): ").strip()
    
    # Если не введен путь, используем текущую папку
    if not root_dir:
        root_dir = os.getcwd()
    
    # Проверяем существование папки
    if not os.path.isdir(root_dir):
        print(f"✗ Ошибка: папка '{root_dir}' не существует")
        return
    
    print(f"\nПоиск mp3 файлов в: {os.path.abspath(root_dir)}")
    print("-" * 50)
    
    # Запускаем организацию файлов
    organize_audio_files(root_dir)
    
    print("\n✓ Организация файлов завершена!")


if __name__ == "__main__":
    main()