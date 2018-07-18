# _*_ coding:utf-8 _*_

from scrapy import cmdline

def main():
    # 使用解决pycharm运行不了scrapy问题
    cmdline.execute("scrapy crawl txhr".split())

if __name__ == '__main__':
    main()