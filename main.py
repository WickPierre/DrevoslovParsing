from parsers import parser_for_raw_dictionary, parser_for_articles, parser_for_trees, parser_for_trees_img


def main():
    parser_for_raw_dictionary.parse_dictionary()
    parser_for_articles.parse_all_articles()
    parser_for_trees.parse_and_union_trees_and_articles()
    parser_for_trees_img.get_img_of_trees()


if __name__ == "__main__":
    main()
