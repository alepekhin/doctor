# Doctor — AI Medical Data Analyzer

**Doctor** — CLI инструмент для анализа медицинских лабораторных данных с использованием локальной LLM Ollama.

## 🎯 Назначение

Анализирует медицинские лабораторные анализы (биохимия, печёночные ферменты, почечные функции и т.д.) и предоставляет клиническую интерпретацию.

## 🧰 Технологии

- **Python 3.8+**
- **Ollama** с моделью `carstenuhlig/omnicoder-2-9b:latest`
- **Стандартные библиотеки** (requests)

## 📦 Требования

```bash
# Виртуальное окружение (рекомендуется)
python3 -m venv venv
source venv/bin/activate  #Linux/macOS
source venv/Scripts/activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

## 🚀 Запуск

### Базовый запуск

```bash
cat blud.json | python3 doctor
```

### Интерактивный режим

```bash
python3 doctor
# Вставьте JSON с данными анализов (Ctrl+D для завершения)
```

### Пайплайн

```bash
cat input.json | python3 doctor | less
```

### Ссылка на модель

```bash
pip install -r requirements.txt
ollama pull carstenuhlig/omnicoder-2-9b:latest
ollama serve &  # Запуск Ollama в фоне
```

## 📊 Формат входных данных

```json
{
  "report_section": "Биохимия",
  "description": "Лабораторные показатели",
  "results": [
    {
      "test_name_russian": "АЛТ",
      "test_name_english": "ALT",
      "result": 48.45,
      "unit": "Ед/л",
      "reference_interval": "0 - 41"
    }
  ]
}
```

## 🧪 Тестирование

### Успешный анализ

```bash
cat blud.json | python3 doctor
# Ожидается клиническая интерпретация на русском языке
```

### Проверка подключения Ollama

```bash
# Если ошибка подключения:
python3 doctor << EOF 2>&1 | grep -i "error\|ollama"
EOF
```

### Запуск теста (любой вход)

```bash
# Простой JSON для проверки
echo '{"test_name_english": "Креатинин", "result": 105, "unit": "мкмоль/л"}' | python3 doctor
```

### Стресс-тест (много результатов)

```bash
# Для тестирования производительности
cat blud.json | python3 doctor | head -100
```

## 📁 Файлы проекта

```
├── doctor                    # CLI входная точка
├── ollama_client.py          # Ollama API клиент
├── requirements.txt          # Зависимости
└── AGENTS.md                 # Документ для AI агентов
```

## 🤝 Совместимость

- ✅ Linux
- ✅ macOS
- ✅ Windows (PowerShell/bash)

## 📝 Выходные данные

Инструмент генерирует на русском языке:

- ⚠️ Клиническое резюме
- 📋 Список аномальных показателей
- 🔍 Детальный анализ
- 💊 Рекомендации

## ⚠️ Важно

Это ИИ-инструмент, а не медицинский диагноз.
**Все результаты требуют подтверждения врачом.**

---

**Лицензия**: MIT
