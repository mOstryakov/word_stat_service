# Word Frequency Analysis Service

## 1. Clone repository
``` bash
git clone https://github.com/mOstryakov/word_stat_service.git
cd word_stat_service
```

## 2. Install Poetry
```bash
pip install poetry
```

## 3. Install dependencies
```bash
poetry install
```
If poetry command is not found (common on Windows), use:
```bash
python -m poetry install
```

## 4. Starting the service

```bash
poetry run python -m app.main
```
After launch, the server will be available at: http://127.0.0.1:8000/docs