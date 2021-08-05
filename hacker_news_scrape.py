import requests
from bs4 import BeautifulSoup


def sort_stories_by_votes(hacker_news_list: list[dict]) -> list[dict]:
    return sorted(hacker_news_list, key=lambda key: key['votes'], reverse=True)


def create_custom_hacker_news(links, subtext) -> list[dict]:
    hacker_news_list = []
    for index, item in enumerate(links):
        votes = subtext[index].select('.score')
        if len(votes) and (points := int(votes[0].getText().replace(' points', ''))) >= 100:
            title = item.getText()
            link = item.get('href', None)

            hacker_news_list.append({'title': title, 'link': link, 'votes': points})

    return sort_stories_by_votes(hacker_news_list)


def pretty_string_of_hacker_news_list(hacker_news_list: list[dict]) -> str:
    return str(
        hacker_news_list).replace(',', '\n').replace('[', '').replace(']', '').replace('{', '\n').replace('}', '')


class B:
    BASE_LINK = 'https://news.ycombinator.com/news?p='


def get_soup(n: int) -> BeautifulSoup:
    return BeautifulSoup(requests.get(f'{B.BASE_LINK}{n}').text, 'html.parser')


def main():
    first_soup = get_soup(1)
    links = first_soup.select('.storylink')
    subtext = first_soup.select('.subtext')

    for i in range(2, 6):
        soup = get_soup(i)
        links += soup.select('.storylink')
        subtext += soup.select('.subtext')

    print(pretty_string_of_hacker_news_list(create_custom_hacker_news(links, subtext)))


if __name__ == '__main__':
    main()
