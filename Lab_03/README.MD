# Lab 03 — Stream Processing (Variant 4: Bank Accounts)

Потокова обробка великих наборів даних у Python: ітератори, генератори,
lazy evaluation, `itertools`, batching та streaming aggregation.

## Мета

Побудувати lazy pipeline для обробки CSV з банківськими операціями без
повного завантаження даних у пам'ять.

## Структура проєкту
lab03_bank/
├── data/ # CSV-датасети (генеруються скриптом)
├── stream_processor/ # основний пакет
│ ├── models.py # NamedTuple-моделі
│ ├── readers.py # streaming reader (yield from file)
│ ├── parsers.py # csv.DictReader
│ ├── filters.py # validation + filtering + apply
│ ├── transformations.py # normalize / mask
│ ├── batches.py # batching через islice
│ ├── analytics.py # aggregation, top-N, пошук
│ └── pipeline.py # складання lazy pipeline
├── examples.py # iterable/iterator/yield/yield from/itertools
├── generate_data.py # генерація тестових CSV
├── experiments.py # eager vs lazy (time + memory)
└── main.py # демонстраційний сценарій


## Швидкий старт

```bash
# 1. Згенерувати тестові дані
python generate_data.py

# 2. Демонстрація мовних конструкцій
python examples.py

# 3. Основний сценарій
python main.py

# 4. Експеримент eager vs lazy
python experiments.py