import json
import sqlite3

# Путь к JSON-файлу и создаваемой базе данных
JSON_PATH = 'new_parsed_articles2.json'
DB_PATH = 'dictionary.db'

# Загрузка JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Создание базы данных
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        text TEXT,
        author TEXT,
        tree_link TEXT,
        article_link TEXT,
        tree_title TEXT,
        tree_img TEXT,
        full_article_text TEXT
    );
''')

# Индекс для быстрого поиска по title
cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON articles(title);')

# Очистка таблицы перед вставкой
cursor.execute('DELETE FROM articles;')

# Вставка данных
for entry in data:
    cursor.execute('''
        INSERT INTO articles (
            title, date, text, author,
            tree_link, article_link, tree_title, tree_img, full_article_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry.get('title', ''),
        entry.get('date', ''),
        entry.get('text', ''),
        entry.get('author', ''),
        entry.get('tree_link', ''),
        entry.get('article_link', ''),
        entry.get('tree_title', ''),
        entry.get('tree_img', ''),
        entry.get('full_article_text', '')
    ))

conn.commit()
conn.close()

print(f'✅ База данных сохранена как {DB_PATH}')