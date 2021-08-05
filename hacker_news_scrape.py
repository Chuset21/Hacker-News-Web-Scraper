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


def main():
    response = requests.get('https://news.ycombinator.com/news')
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')

    print(pretty_string_of_hacker_news_list(create_custom_hacker_news(links, subtext)))


if __name__ == '__main__':
    main()
