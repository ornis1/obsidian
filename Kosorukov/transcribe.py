#!/usr/bin/env python3
"""
Транскрибация аудиофайлов через mlx_whisper.
Сохраняет .md рядом с каждым .mp3.
Пропускает уже транскрибированные файлы.
"""

import argparse
import sys
from pathlib import Path


DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"


def find_mp3_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.mp3"))


def transcribe(audio_path: Path, model: str) -> str:
    import mlx_whisper
    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=model,
        language="ru",
    )
    return "\n".join(seg["text"].strip() for seg in result.get("segments", [])).strip()


def main():
    parser = argparse.ArgumentParser(description="Транскрибация MP3 через mlx_whisper")
    parser.add_argument("--dir", type=Path, default=Path(__file__).parent,
                        help="Директория с аудиофайлами (по умолчанию: папка скрипта)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Модель mlx_whisper (по умолчанию: {DEFAULT_MODEL})")
    args = parser.parse_args()

    root = args.dir.resolve()
    if not root.is_dir():
        print(f"Ошибка: директория не найдена: {root}", file=sys.stderr)
        sys.exit(1)

    mp3_files = find_mp3_files(root)
    if not mp3_files:
        print("MP3-файлы не найдены.")
        return

    total = len(mp3_files)
    skipped = 0
    done = 0
    errors = []

    print(f"Найдено файлов: {total}")
    print(f"Модель: {args.model}\n")

    for i, audio_path in enumerate(mp3_files, 1):
        md_path = audio_path.with_suffix(".md")
        rel = audio_path.relative_to(root)

        if md_path.exists():
            print(f"[{i}/{total}] Пропуск (уже есть): {rel}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Транскрибирую: {rel} ... ", end="", flush=True)

        try:
            text = transcribe(audio_path, args.model)
            md_path.write_text(text, encoding="utf-8")
            print("готово")
            done += 1
        except Exception as e:
            print(f"ОШИБКА: {e}")
            errors.append((str(rel), str(e)))

    print(f"\n--- Итого ---")
    print(f"Транскрибировано: {done}")
    print(f"Пропущено (уже были): {skipped}")
    if errors:
        print(f"Ошибки ({len(errors)}):")
        for path, err in errors:
            print(f"  {path}: {err}")


if __name__ == "__main__":
    main()
