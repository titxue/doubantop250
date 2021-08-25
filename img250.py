from urllib import request
import re
import os


class PosterSpider(object):
    def __init__(self, path='./'):
        # 保存路径
        self.path = path
        # 设置 User-Agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

    def start(self, url):
        # 入口函数
        page = self.requestPage(url)
        page = page.decode('utf-8')
        mvinfo = self.getMvInfo(page)
        for mvname, mvurl in mvinfo:
            self.save2Img(mvname, mvurl)
            print(mvname)
        nexturl = self.getNextPage(page)
        if nexturl:
            self.start(nexturl)

    def requestPage(self, url):
        # 请求页面信息
        if url:
            # 设置headers
            req = request.Request(url=url, headers=self.headers)
            res = request.urlopen(req)
            if res.code == 200:
                return res.read()

    def getMvInfo(self, page):
        # 解析数据 ，返回电影名称与海报地址
        if page:
            listinfo = re.findall(r'<img.*alt="(.*?)".*?src="(.*?)"', page)
            return listinfo
        return []

    def getNextPage(self, page):
        # 获取下一页url，没有返回None
        headurl = 'https://movie.douban.com/top250'
        if page:
            url = re.findall(r'<link rel="next" href="(.*?)"', page)
            if url:
                return headurl+url[0]

    def save2Img(self, fname, url):
        # 保存图片
        img = self.requestPage(url)
        # 文件名和后缀
        fname = "{aname}.{bname}".format(
            aname=fname, bname=url.rsplit('.', 1)[-1])
        # 文件路径
        fpath = os.path.join(self.path, fname)
        # 保存图片
        with open(fpath, 'wb') as f:
            f.write(img)


if __name__ == '__main__':
    os.mkdir("img")
    url = 'https://movie.douban.com/top250'
    spider = PosterSpider('img')
    spider.start(url)
