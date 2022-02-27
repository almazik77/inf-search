import os
import requests


def get_request(url: str):
    request = requests.get(url)
    request.encoding = request.apparent_encoding
    if request.status_code == 200:
        if request.text[request.text.find('<title>') + 7: request.text.find('</title>')] != 'Error':
            return request.text
    return None


class Crawler:
    def __init__(self):
        self.pages_folder_name = os.path.dirname(__file__) + '/pages'
        self.input_file_name = os.path.dirname(__file__) + '/input.txt'
        self.index_file_name = os.path.dirname(__file__) + '/index.txt'
        try:
            os.mkdir(self.pages_folder_name)
        except FileExistsError:
            pass

    def download(self):
        input_file = open(self.input_file_name)
        urls = [line.rstrip('\n') for line in input_file]
        input_file.close()
        unique_urls = list(set(urls))

        index_file = open(self.index_file_name, 'w', encoding='utf-8')
        i = 0

        for url in unique_urls:
            try:
                req_url = "http://" + url
                text = get_request(req_url)
                if text is None:
                    continue
            except Exception as error:
                print(url + " Error " + format(error))
            else:
                i += 1
                filename = self.pages_folder_name + '/выкачка_' + url + '_' + str(i) + ".html"
                page = open(filename, 'w', encoding='utf-8')
                page.write(text)
                page.close()
                index_file.write(str(i) + ' ' + url + '\n')
        index_file.close()


if __name__ == '__main__':
    c = Crawler()
    c.download()
