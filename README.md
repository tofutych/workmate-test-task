# Workmate Reporting Tool

Инструмент для чтения CSV-файлов с данными сотрудников и генерации отчётов (например, по выплатам), сгруппированных по отделам.

## 📦 Возможности

- Обработка **нескольких CSV-файлов** за один запуск
- Поддержка различных типов отчётов (например, `payout`)
- Группировка данных по отделам
- Вывод в формате JSON
- CLI-интерфейс

## 🚀 Использование

> [!IMPORTANT]
> Перед запуском убедитесь, что входные CSV-файлы находятся в директории res/

```bash
git clone https://github.com/tofutych/workmate-test-task.git
cd workmate-test-task
python3 main.py data1.csv data2.csv data3.csv --report payout
