from aip import AipOcr

APP_ID = "15183682"
API_KEY = "yQUAhIN2Hb3brKTh8gzUyFKG"
SECRET_KEY = "9wZw7pSihrN9s89m7LzmAB2NmGADPf1C"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


class Ocr():

    def get_Bytesresult(self, bytesobj, accur=False):
        if accur:
            self.result = client.basicAccurate(bytesobj)
        else:
            self.result = client.basicGeneral(bytesobj)

    def get_Fileresult(self, filepath, accur=False):
        image = get_file_content(filepath)
        if accur:
            self.result = client.basicAccurate(image)
        else:
            self.result = client.basicGeneral(image)

    def get_Urlresult(self, url):
        self.result = client.webImageUrl(url)

    def result_strings(self):
        if self.result['words_result_num'] != 0:
            words = []
            for item in self.result['words_result']:
                words.append(item['words'])
            return '\n'.join(words)


if __name__ == '__main__':
    t = Ocr()
    t.get_Fileresult(r'F:\temp_py\mantis-download\tesslearn\1\captcha14.jpg')
    print(t.result_strings(), len(t.result_strings()))
