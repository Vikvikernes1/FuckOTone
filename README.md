# FuckOTone

Небольшой кроссплатформенный кликер на Python и Tkinter.

## Запуск

Нужны Python 3.9+ и установленный Pillow. Рекомендуемый безопасный вариант — виртуальное окружение:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

На Linux может понадобиться системный пакет `python3-tk`.

Приложение использует `world.png`, `fuck.gif` и `furry.png` из корня проекта. `fuck.gif` воспроизводится с исходной задержкой кадров, а лицо из `furry.png` накладывается на каждый кадр. Интернет для работы не нужен.

## Сборка в отдельное приложение локально

Установите PyInstaller и выполните:

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name FuckOTone --add-data "world.png:." --add-data "fuck.gif:." --add-data "furry.png:." main.py
```

На Windows в `--add-data` используется разделитель `;` вместо `:`. Сборку нужно выполнять отдельно на каждой целевой ОС.

