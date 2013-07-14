from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import TutorialItem
import MySQLdb
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
            if(len(item['link'])>0 and len(item['pageLink'])>0):
                print 'link:', item['link']
                print 'pagelink:', item['pageLink']
                linkStr = item['link'][0].encode('gbk')
                for plink in item['pageLink']:
		    plinkStr = plink.encode('gbk')
                    sql = 'insert into imageTest (link,pageLink) values(\"%s\",\"%s\")'%(linkStr,plinkStr)
                    print "sql:",sql
                    cur.execute(sql)
            #if (site.select('@href') is not None and len(site.select('@href'))>0):
            #    for linkStr in item['link']
            #        print linkStr
                    
            # if (site.select('//div/img/@src') is not None and len(site.select('//div/img/@src'))>0):
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
	return items
