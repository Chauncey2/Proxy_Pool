import json
import re
from .utils import get_page
from pyquery import  PyQuery as pq

class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count=0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)


class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies=[]
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理",proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili666(self,page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_utrl='http://www.66ip.cn/{}.html'
        urls=[start_utrl.format(page) for page in range(1,page_count+1)] # 列表生成式
        for url in urls:
            print('Crawling',url)
            html=get_page(url)
            if html:
                doc=pq(html)
                trs=doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2').text()
                    yield ':'.join([ip,port]) # string的join，"ip:port"

    # def crawl_ip3366(self):
    #     """
    #     爬取ip3366的代理地址以及ip
    #     :return:
    #     """
    #     for page in range(1,4):
    #         start_url='http://www.ip3366.net/free/?stype=1&page={}'.format(page)
    #         html=get_page(start_url)
    #         ip_address=re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s *匹配空格，起到换行作用
    #         re_ip_address=ip_address.findall(html)
    #         for address,port in re_ip_address:
    #             result=address+":"+port
    #             yield result.replace(' ','')

    def crawl_kuaidaili(self):
        """
        爬取快代理上的代理Ip地址
        :return: 代理ip以及端口
        """
        for i in range(1,4):
            start_url='http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html=get_page(start_url)
            if html:
                ip_address=re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_adress=ip_address.findall(html)
                port=re.compile('<td data-title="PORT">(.*?)</td>')
                re_port=port.findall(html)
                for address,port in zip(re_ip_adress,re_port):
                    address_port=address+":"+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        """
        爬取西刺代理的国内高匿代理IP
        西刺搭理有反爬虫机制，需要伪装请求头
        :return: 代理
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWU3YzdjZDQ1NDBlYTAyZjJlMjRmN2IwMDM'
                      '1ODI1MGVlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWJQUGkwYjlVbzFjZDVWaXJyZnZRWFF1MzFWbkx1ZDBDcXB'
                      'UT3VqcDIvK009BjsARg%3D%3D--dce143751574ee9c6bfa20d6829611d727752037; '
                      'Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1555598069; '
                      'Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1555598069',
            'Referer': 'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests': '1',
        }
        for i in range(1,3):
            start_url='http://www.xocidaili.com/nn/{}'.format(i)
            html=get_page(start_url)
            if html:
                find_trs=re.compile('<tr class.*?>(.*?)</tr>',re.S)
                trs=find_trs.findall(html)
                for tr in trs:
                    find_ip=re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address=find_ip.findall(tr)
                    find_port=re.compile('<td>(\d+)</td>')
                    re_port=find_port.findall(tr)
                    for address,port in zip(re_ip_address,find_port):
                        address_port=address+":"+port
                        yield address_port.replace(' ','')

    def crawl_ip3366(self):
        """
        爬取ip3366中的代理IP
        :return: 代理
        """
        for i in range(1,4):
            start_url='http://www.ip3366.net/?stype=1&page{}'.format(i)
            html=get_page(start_url)
            if html:
                find_tr=re.compile('<tr>(.*?)</tr>', re.S)
                trs=find_tr.findall(html)
                for s in range(1,len(trs)):
                    find_ip=re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address=find_ip.findall(trs[s])
                    find_port=re.compile('<td>(\d+)</td>')
                    re_port=find_port.findall(html)
                    for address,port in zip(re_ip_address,re_port):
                        address_port=address+":"+port
                        yield address_port.replace(' ','')

    def crawl_iphai(self):
        """
        爬取'http://www.iphai.com/'中的代理
        :return:代理
        """
        start_url='http://www.iphail.com/'
        html=get_page(start_url)
        if html:
            find_tr=re.compile('<tr>(.*?)</tr>')
            trs=find_tr.findall(html)
            for s in range(1,len(trs)):
                find_ip=re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address=find_ip.findall(trs[s])
                find_port=re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port=find_port.findall(trs[s])
                for address,port in zip(re_ip_address,re_port):
                    address_port=address+':'+port
                    yield address_port.replace(' ','')

    def crawl_data5u(self):
        """
        'http://www.data5u.com/free/gngn/index.shtml'
        :return:代理
        """
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=24CBCEC9B1E6B7A192C371E1FA083671; '
                      'Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1555600429; '
                      'Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1555600429; '
                      'UM_distinctid=16a3102d2a3260-085605f2070376-b781636-144000-16a3102d2a4517; '
                      'CNZZDATA1260383977=1689752905-1555597201-%7C1555597201',

            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')