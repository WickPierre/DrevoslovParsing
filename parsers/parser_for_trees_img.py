import json
import requests


def get_img_of_trees():
    # Куки в виде словаря
    cookies = {
        "_ga": "GA1.2.1157037236.1747747109",
        "_gid": "GA1.2.1480063021.1748021830",
        "a36b0618cc9908f40392078a88749331": "si2is1d7a0g0oljnd190avrq35",
        "_ga_Q630J9CD6X": "GS2.2.s1748088368$o4$g1$t1748088394$j0$l0$h0"
    }

    # Заголовки
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Referer": "http://www.drevoslov.ru/azbukatree",
        "Accept-Language": "en-US,en;q=0.9",
    }

    with open('../trees.json', 'r', encoding='utf-8') as f:
        trees = json.load(f)

    for tree in trees:
        print('✅' if tree['tree_img'] else '❌', tree['tree_title'])
        if tree['tree_img']:
            img_data = requests.get(tree['tree_img'], headers=headers, cookies=cookies).content
            with open('trees/' + tree['img_name'], 'wb') as handler:
                handler.write(img_data)

    print('Успешно!')


if __name__ == '__main__':
    get_img_of_trees()
