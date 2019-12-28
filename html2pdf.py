import pdfkit
from bs4 import BeautifulSoup
import requests
import os
import re


class Html2pdf:
    def __init__(self, url):
        self.url = url
        self.req = requests.get(self.url)
        self.title = self.get_title()

    def download_html(self):
        """
        将html保存成文件
        @return:
        """
        filename = self.title + '.html'
        with open(filename, 'wb') as f:
            f.write(self.req.content)

    def get_title(self):
        """
        获取标题
        var msg_title = "科研成果快报第123期：金沙江流域极端降雨遭遇概率评估";
        @return: title
        """
        pattern = 'var msg_title = "(.*?)";'
        obj = re.search(pattern, self.req.text)
        title = obj.group(1)
        return title

    def download_image(self):
        """
        下载所有图片，并置换路径
        @return:
        """
        soup = BeautifulSoup(self.req.content, 'lxml')
        imgs = soup.find_all('img')
        urls = []
        paths = []
        for img in imgs:
            if 'data-src' in str(img):
                urls.append(img['data-src'])
        i = 0
        for url in urls:
            r = requests.get(url)
            img_path = os.path.join(str(i) + '.jpg')
            paths.append(img_path)
            with open(img_path, 'wb') as f:
                f.write(r.content)
            i = 1 + i
        self.replace_path(urls, paths)

    def replace_path(self, urls, paths):
        """
        将html文件中的图片路径转换为本地图片路径
        @param urls: 图片src 列表
        @param paths: 本地图片路径 列表
        @return:
        """
        filename = self.title + '.html'
        with open(filename, 'r', encoding='utf-8') as f, open('temp.html', 'w', encoding='utf-8') as fw:
            temp = f.read()
            for url, path in zip(urls, paths):
                temp = temp.replace(url, path)
            temp = temp.replace('data-src', 'src')
            fw.write(temp)
        os.remove(filename)
        os.rename('temp.html', filename)

    def save_pdf(self, html, file_name):
        """
        把所有html文件保存到pdf文件
        :param html:  html文件列表
        :param file_name: pdf文件名
        :return:
        """
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        try:
            pdfkit.from_file(html, file_name, options=options)
        except BaseException:
            pass

    def start(self):
        self.download_html()
        self.download_image()
        self.save_pdf(self.title + '.html', self.title + '.pdf')


if __name__ == '__main__':
    urls = ['https://mp.weixin.qq.com/s/bAXuJxMeKs2cyJ0kp7SHpw']
    for url in urls:
        test = Html2pdf(url)
        test.start()
