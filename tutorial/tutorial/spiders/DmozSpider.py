from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import TutorialItem
from commands import getstatusoutput
import MySQLdb
import Image
import os
import types
ALL_URLS = set()
ALL_IMGS = set()

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["haibao.com"]
    start_urls = ["http://www.haibao.com" ]

    #try:
   #except:
    #    print "Could not connect to MySQL server."
    #    exit( 0 ) 
    def parse(self, response):
        #filename = response.url.split(".com")[-1]
        conn = MySQLdb.connect(user="zq",passwd="1234",host="localhost",db="image", port=3306)
        cur=conn.cursor()
           
        open('zqtest.txt', 'wb').write(response.body)
        print '*'
        items = []
	print '**'
        hxs = HtmlXPathSelector(response)
	print '***'
        sites = hxs.select('//a') 
        for site in sites:
            item = TutorialItem()
            item['link'] = site.select('@href').extract()
            item['pageLink'] = site.select('img/@src').extract()
            for linkStrTmp in item['link']:
                if linkStrTmp.find('http://www.haibao')>=0:
                    if not linkStrTmp in ALL_URLS:
                        ALL_URLS.add(linkStrTmp)
                        yield Request(linkStrTmp,callback=self.parse)
                        print '**** send ',linkStrTmp
                    else:
                        print '**** duplicate'
           
            if(len(item['link'])>0 and len(item['pageLink'])>0):
               #print 'link:', item['link']
               #print 'pagelink:', item['pageLink']
                
                linkStr = item['link'][0].encode('gbk')
                for plink in item['pageLink']:
		    plinkStr = plink.encode('gbk')
                   # print 'plinkStr:  ',plinkStr
                    if not plinkStr.split('/')[-1] in ALL_IMGS:
                        ALL_IMGS.add(plinkStr.split('/')[-1])
                        cmd = 'wget "%s"'%plinkStr
                        (exit_code, console_output) = getstatusoutput(cmd)
                      
                        splitLink=plinkStr.split('/')
                        print splitLink[-1]
                        cmdput = 'tftp localhost -c put %s'%(splitLink[-1])
                        print 'command: ', cmdput
                        (exit_code, console_output) = getstatusoutput(cmdput)
                        im = Image.open(splitLink[-1])
                        width,height = im.size
                        del im 
                        cmdrm = 'rm %s'%(splitLink[-1])
                        print cmdrm
                        (exit_code, console_output) = getstatusoutput(cmdrm)
                        print width,height
                        if width < 500 or height < 500:
                            continue
                        sql = 'insert into imageTest (link,pageLink) values(\"%s\",\"%s\")'%(linkStr,plinkStr)
                        print "sql:",sql
                        cur.execute(sql)
                    else:
                        print '********** duplicate image'
            #if (site.select('@href') is not None and len(site.select('@href'))>0):
            #    for linkStr in item['link']
            #        print linkStr
                    
            # if (site.select('//diiv/img/@src') is not None and len(site.select('//div/img/@src'))>0):
            #    for count2 in item['pageLink']                 
            #       pageLinkStr = site.select('//div/img/@src').extract()[count2].encode('gbk')
            #pageLinkStr= site.select('//div/img/@src').extract()
            #pageLinkStr2= site.select('//div/img/@src').extract()[0].encode['gbk']
            #print 'linkStr : ', linkStr
            #print 'pageLinkStr : ', pageLinkStr
            #for link in item['pageLink']
            #for link in item[]:
	            #open('zqitem.txt','wb').write("link : "+linkStr)
                #    print 'type of linkStr is :', type(linkStr)
                #    print linkStr
		    #cur.executemany('insert into imageTest values(%s,%s)',%(linkStr,))
		#for pagelinkStr in item['pageLink']:
        	    #cur.executemany('insert into imageTest values(%s,%s)',pagelink
	
        conn.commit()
        cur.close()
        conn.close()
        items.append(item)
	#open('zqitem.txt','wb').write(items)
	#return items
