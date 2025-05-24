import json
from bs4 import BeautifulSoup


def parse_article(html):
    soup = BeautifulSoup(html, 'html.parser')

    result = {
        'title': None,
        'date': None,
        'text': None,
        'author': None,
        'tree_link': None,
        'article_link': None
    }

    first_td = soup.find('td')
    if first_td:
        title_link = first_td.find('a')
        if title_link:
            result['title'] = title_link.get_text(strip=True)
            result['article_link'] = 'http://www.drevoslov.ru' + title_link['href']

        tree_p = first_td.find_all('p')
        for p in tree_p:
            a = p.find('a')
            if a and 'древ' in a.get_text(strip=True).lower():
                result['tree_link'] = 'http://www.drevoslov.ru' + a['href']
                break

    second_td = soup.find_all('td')[1] if len(soup.find_all('td')) > 1 else None
    if second_td:
        # Дата
        date_span = second_td.find('span', string=lambda t: t and 'Дата размещения' in t)
        if date_span:
            result['date'] = date_span.get_text(strip=True)

        # Форматированный текст
        text_blocks = []
        for p in second_td.find_all('p'):
            if not p.find_parent('div', class_='authorblock'):
                html = p.decode_contents().strip()
                if html and 'Дата размещения' not in html:
                    text_blocks.append(f"<p>{html}</p>")
        result['text'] = '\n'.join(text_blocks)

        # Автор
        author_div = second_td.find('div', class_='authorblock')
        if author_div:
            result['author'] = author_div.get_text(strip=True).replace('Автор', '').replace(':', '').strip()

    return result


def parse_all_articles():
    # Загрузка данных
    with open('dictionary.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка всех статей
    parsed_data = []
    for item in data:
        parsed = parse_article(item['html'])
        parsed_data.append(parsed)

    # Сохранение результата
    with open('parsed_articles.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

    print('Обработано статей:', len(parsed_data))


if __name__ == '__main__':
    parse_all_articles()
