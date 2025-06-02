import requests
from bs4 import BeautifulSoup, Comment
from concurrent.futures import ThreadPoolExecutor, as_completed
from parser_for_raw_dictionary import clean_html
import json
import time


def parse_article(link):
    """Парсит div[itemprop=articleBody] с подстановкой заголовков."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Referer": "http://www.drevoslov.ru/"
        }
        response = requests.get(link, headers=headers, timeout=100)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('div', itemprop='articleBody')

        return clean_html(body.decode_contents()) if body else ''
    except Exception as e:
        print(f"❌ Ошибка при парсинге {link}: {e}")
        return ''


def parse_entry(item):
    """Обрабатывает одну запись с ссылкой."""
    link = item['article_link']
    print(f"🔗 Обработка: {link}")
    html = parse_article(link)
    return {
        "article_link": link,
        "html": html
    }


def parse_all_articles(json_path_in, json_path_out, max_workers=8):
    with open(json_path_in, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_entry, item) for item in data]

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(f"✅ Готово [{i}/{len(data)}]")

    with open(json_path_out, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Парсинг завершён. Обработано: {len(results)} записей.")
    print(f"⏱ Затрачено времени: {time.time() - start:.2f} сек")


def parse_all_distinct_articles(json_path_in, json_path_out):
    with open(json_path_in, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        if item['html'] == '':
            item['html'] = parse_entry(item)['html']
            print(item['html'])

    with open(json_path_out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def concate_jsons(json1, json2):
    with open(json1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    with open(json2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    for item in data1:
        item['full_article_text'] = [clean_html(i['html']) for i in data2 if i['article_link'] == item['article_link']][0]

    with open('../new_parsed_articles2.json', 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=2)

    print('Done!!')


if __name__ == '__main__':
    # parse_all_articles(
    #     json_path_in='../new_parsed_articles.json',
    #     json_path_out='../extended_articles.json',
    #     max_workers=20  # Можно попробовать 8–12, но без фанатизма
    # )
    # parse_all_distinct_articles(
    #     json_path_in='../extended_articles.json',
    #     json_path_out='../extended_articles.json'
    # )
    concate_jsons(
        '../new_parsed_articles.json',
        '../extended_articles.json'
    )