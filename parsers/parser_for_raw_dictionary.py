from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, Comment
import time
import json


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Удалить MS Office XML, style, script
    for tag in soup.find_all(["xml", "style", "script"]):
        tag.decompose()

    # Удалить комментарии
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Удалить мусорные атрибуты
    for tag in soup.find_all(True):
        attrs_to_delete = []
        for attr, value in tag.attrs.items():
            if attr.startswith("mso") or "mso-" in str(value) or attr.startswith("xmlns"):
                attrs_to_delete.append(attr)
        for attr in attrs_to_delete:
            del tag[attr]

    return str(soup)


def parse_dictionary():
    # Настройка Selenium
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("http://www.drevoslov.ru/dict/dict-2")

    time.sleep(0.5)

    MAX_PAGES = 100

    # Установим количество строк на страницу = 100
    select = driver.find_element(By.NAME, "limit")
    select.send_keys(str(MAX_PAGES))
    time.sleep(0.5)

    # Определим максимальное количество страниц
    last_buttons = driver.find_elements(By.CLASS_NAME, 'hasTooltip')
    pages = int(last_buttons[-1].get_attribute('onclick').split(';')[0].split('=')[1]) // 100 + 1
    time.sleep(0.5)

    all_data = []

    for i in range(pages):
        print(f"\n📄 Страница {i + 1}")

        glossary = driver.find_element(By.ID, "glossarylist")
        words = glossary.find_elements(By.TAG_NAME, "tr")

        for word in words:
            raw_html = word.get_attribute("outerHTML")
            cleaned_html = clean_html(raw_html)
            if '<th class=\"glossary25\">Термин</th>' in cleaned_html:
                continue
            all_data.append({
                "html": cleaned_html
            })
        print(f"✅ Собрано {len(all_data)} слов")

        # Переход на следующую страницу
        try:
            offset = (i + 1) * 100
            driver.execute_script(f"document.getElementsByName('limitstart')[0].value = '{offset}';")
            driver.execute_script("document.adminForm.submit();")

        except Exception as e:
            print("🚫 Не удалось перейти на следующую страницу:", e)
            break

    # Сохранить в JSON
    with open("dictionary.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    driver.quit()


if __name__ == "__main__":
    parse_dictionary()
