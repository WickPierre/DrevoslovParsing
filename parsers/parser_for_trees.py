from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

def get_html(link, driver):
    driver.get(link)

    com_glossary = driver.find_element(By.ID, "com_glossary")
    title = com_glossary.find_element(By.TAG_NAME, "h1").text
    if 'class=\"cloud-zoom\"' in com_glossary.get_attribute("outerHTML"):
        tree_link = com_glossary.find_element(By.CLASS_NAME, "cloud-zoom").get_attribute("href")
    else:
        tree_link = None

    return title, tree_link

def join_jsons(articles, trees):
    print('Конкатенация...')
    new_data = []

    for entry in articles:
        tree_title, tree_img = [(tree['tree_title'], tree['tree_img']) for tree in trees if tree['tree_link'] == entry['tree_link']][0]
        entry['tree_title'], entry['tree_img'] = tree_title, tree_img

        new_data.append(entry)

    # Сохранить в JSON
    with open("new_parsed_articles.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print('Успешно!')

def parse_and_union_trees_and_articles():
    # Настройка Selenium
    options = Options()

    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Загрузка исходного JSON
    with open('parsed_articles.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    raw_trees = list(set(i.get("tree_link", "") for i in raw_data))

    trees = []
    c = 1
    print('Сбор данных о деревьях')
    for tree in raw_trees:
        print(c, tree)
        title, tree_img = get_html(tree, driver)

        trees.append({
            "tree_link": tree,
            "tree_title": title,
            "tree_img": tree_img,
            "img_name": tree_img.split('/')[-1] if tree_img else None
        })
        c += 1

    # Сохранить в JSON
    with open("trees.json", "w", encoding="utf-8") as f:
        json.dump(trees, f, ensure_ascii=False, indent=2)

    driver.quit()
    join_jsons(raw_data, trees)


if __name__ == '__main__':
    parse_and_union_trees_and_articles()