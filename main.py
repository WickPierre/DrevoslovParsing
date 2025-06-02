from parsers import (parser_for_raw_dictionary, parser_for_articles,
                     parser_for_trees, parser_for_trees_img, parser_for_extended_articles)


def main():
    parser_for_raw_dictionary.parse_dictionary()
    parser_for_articles.parse_all_articles()
    parser_for_trees.parse_and_union_trees_and_articles()
    parser_for_trees_img.get_img_of_trees()

    parser_for_extended_articles.parse_all_articles(
        json_path_in='../new_parsed_articles.json',
        json_path_out='../extended_articles.json',
        max_workers=20
    )
    parser_for_extended_articles.parse_all_distinct_articles(
        json_path_in='../extended_articles.json',
        json_path_out='../extended_articles.json'
    )


if __name__ == "__main__":
    main()
