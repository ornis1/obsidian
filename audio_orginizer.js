const fs = require('fs').promises;
const path = require('path');

// Список расширений аудиофайлов
const audioExtensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus'];

// Папка для обработки
const sourceFolder = process.argv[2] || './Kosorukov/1. Баланс';
let processedCount = 0;

async function processAudioFiles() {
  try {
    console.log(`🔍 Рекурсивно сканирую папку: ${sourceFolder}\n`);

    // Рекурсивно проходим по всем папкам
    await processFolder(sourceFolder);

    if (processedCount === 0) {
      console.log('❌ Аудиофайлы не найдены!');
    } else {
      console.log(`\n🎉 Обработано файлов: ${processedCount}`);
    }
  } catch (error) {
    console.error('❌ Ошибка:', error.message);
    process.exit(1);
  }
}

// Рекурсивная функция для обхода папок
async function processFolder(folderPath) {
  try {
    const items = await fs.readdir(folderPath);
    const audioFiles = [];

    // Разделяем файлы и папки
    for (const item of items) {
      const itemPath = path.join(folderPath, item);
      try {
        const stats = await fs.stat(itemPath);

        if (stats.isDirectory()) {
          // Если это папка, рекурсивно обрабатываем её
          await processFolder(itemPath);
        } else if (stats.isFile()) {
          // Если это файл и это аудио, добавляем в очередь
          const ext = path.extname(item).toLowerCase();
          if (audioExtensions.includes(ext)) {
            audioFiles.push(itemPath);
          }
        }
      } catch (error) {
        console.error(`⚠️  Ошибка при проверке ${itemPath}:`, error.message);
      }
    }

    // Обрабатываем аудиофайлы параллельно (до 5 одновременно)
    if (audioFiles.length > 0) {
      const chunkSize = 5;
      for (let i = 0; i < audioFiles.length; i += chunkSize) {
        const chunk = audioFiles.slice(i, i + chunkSize);
        await Promise.all(chunk.map(processAudioFile));
      }
    }
  } catch (error) {
    console.error(`❌ Ошибка при чтении папки ${folderPath}:`, error.message);
  }
}

// Функция для поиска .md файла с названием аудиофайла
async function findMatchingMdFile(folderPath, audioFileName) {
  try {
    const items = await fs.readdir(folderPath);

    for (const item of items) {
      const ext = path.extname(item).toLowerCase();
      
      // Ищем только .md файлы
      if (ext === '.md') {
        const filePath = path.join(folderPath, item);
        try {
          const content = await fs.readFile(filePath, 'utf-8');
          
          // Проверяем, содержит ли .md файл имя аудиофайла
          if (content.includes(audioFileName)) {
            return filePath; // Возвращаем путь к найденному .md файлу
          }
        } catch (error) {
          console.error(`⚠️  Ошибка при чтении ${filePath}:`, error.message);
        }
      }
    }

    return null; // .md файл не найден
  } catch (error) {
    console.error(`❌ Ошибка при поиске .md файла в ${folderPath}:`, error.message);
    return null;
  }
}

// Функция для обработки одного аудиофайла
async function processAudioFile(filePath) {
  try {
    const fileName = path.parse(filePath).name; // Имя без расширения
    const fileExt = path.extname(filePath); // Расширение с точкой
    const parentFolder = path.dirname(filePath); // Папка, где находится файл
    const folderPath = path.join(parentFolder, fileName); // Путь новой папки
    const newAudioFileName = `audio${fileExt}`;
    const newAudioFilePath = path.join(folderPath, newAudioFileName);

    // Ищем .md файл с названием аудиофайла
    const mdFilePath = await findMatchingMdFile(parentFolder, fileName);

    if (!mdFilePath) {
      console.log(`⏭️  Пропущен (нет .md файла): ${filePath}`);
      return;
    }

    const mdFileName = path.basename(mdFilePath);
    const newMdFilePath = path.join(folderPath, mdFileName);

    // Создаем папку если её нет
    try {
      await fs.mkdir(folderPath, { recursive: true });
      console.log(`📁 Создана папка: ${folderPath}`);
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      console.log(`⚠️  Папка уже существует: ${folderPath}`);
    }

    // Проверяем, есть ли уже файлы в папке
    try {
      await fs.access(newAudioFilePath);
      console.log(`⚠️  Аудиофайл уже существует: ${newAudioFilePath}`);
      return;
    } catch {
      // Файл не существует - это хорошо, продолжаем
    }

    try {
      await fs.access(newMdFilePath);
      console.log(`⚠️  .md файл уже существует: ${newMdFilePath}`);
      return;
    } catch {
      // Файл не существует - это хорошо, продолжаем
    }

    // Перемещаем аудиофайл в папку с переименованием
    await fs.rename(filePath, newAudioFilePath);
    console.log(`🎵 Перемещен аудиофайл: ${filePath}`);
    console.log(`   → ${newAudioFilePath}`);

    // Перемещаем .md файл в папку
    await fs.rename(mdFilePath, newMdFilePath);
    console.log(`📄 Перемещен .md файл: ${mdFileName}`);
    console.log(`   → ${newMdFilePath}`);

    console.log(`✨ Готово!\n`);
    processedCount++;

  } catch (error) {
    console.error(`❌ Ошибка при обработке ${filePath}:`, error.message);
  }
}

// Запускаем скрипт
processAudioFiles();