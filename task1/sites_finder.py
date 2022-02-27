import requests


class Generator:
    def __init__(self):
        self.requests = 5
        self.request_url = 'https://www.liveinternet.ru/rating//education/month.tsv?;search=программирование'

    def generate(self):
        links = open("input.txt", 'a', encoding='utf-8')
        for i in range(self.requests):
            request = requests.get(self.request_url + ';page=' + str(i))
            data = request.text.split("\n")
            for row in data[1:30]:
                url = row.split("\t")[1].replace("/", "")
                print(url + '\n', end='')
                links.write(url + "\n")
        links.close()


if __name__ == '__main__':
    g = Generator()
    g.generate()
