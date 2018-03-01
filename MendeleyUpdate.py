# coding: UTF-8
# author: Sun Yongke (sunyongke@gmail.com)
'''
update the meta information by doi from http://dx.doi.org.

更新Mendeley中的文章信息，数据来源为http://dx.doi.org. Mendeley自带的doi更新功能只支持coressref doi的数据查询，
但是很多的中文文章在coressref中查找不到。该脚本可以通过doi.org网站更新文章的信息。

使用方法:
python --doi=10.3969/j.issn.1001-7461.2012.06.33

'''

import argparse
from bs4 import BeautifulSoup
import sqlite3
import re
import sys
import os.path
import traceback

artic={}
def get_DOI(doi):
    import urllib.request
    webpage = "http://dx.doi.org/" + doi
    print(webpage)
    try:
        sock = urllib.request.urlopen(webpage)
    except:
        print("Unable to reach meta data")
        traceback.print_exc(file=sys.stdout)
        sys.exit()
    htmlSource = sock.read()
    sock.close()
    # print(htmlSource)
    soup = BeautifulSoup(htmlSource,"html5lib")
    # print(soup.prettify())
    article=soup.find("div", class_="left_con")
    title=article.select('div.left_con_top div.title')[0].get_text().strip()

    artic["title"]=title.split('\n')[0]
    # print(articleinfo.prettify())

    abstract=article.select('div.abstract textarea')
    # print(abstract[0].get_text())
    artic["abstract"]=abstract[0].get_text().strip()
    info_li=article.select('ul.info li')
    for li in info_li:
        tag_name=li.select('div')[0].get_text().strip()
        if tag_name.startswith("关键词"):
            keywords_tag=li.select('div')[1].select('a')
            keywords=[]
            for k in keywords_tag:
                if len(k.get_text().strip())==0:
                    continue
                keywords.append(k.get_text().strip())
            artic["keywords"]=keywords
        elif tag_name.startswith("作者："):
            authors_tag = li.select('div')[1].select('a')
            authors = []
            for k in authors_tag:
                if len(k.get_text().strip()) == 0:
                    continue
                authors.append(k.get_text().strip())
            artic["authors"]=authors
        elif tag_name.startswith("刊名"):
            artic["publication"]= li.select('div')[1].get_text().strip()
            # print(publisher)
        elif tag_name.startswith("Journal"):
            artic["publication_en"] = li.select('div')[1].get_text().strip()
            # print(publisher_en)
        elif tag_name.startswith("年，卷(期)"):
            y_v_i = li.select('div')[1].get_text().strip().replace(' ','')
            m = re.findall(r'(\d+)', y_v_i)
            artic["year"]='Null'
            artic["volume"]='Null'
            artic["issue"]='Null'
            try:
                artic["year"]=m[0]
                artic["volume"]=m[1]
                artic["issue"]=m[2]
            except:
                pass


        elif tag_name.startswith("页码"):
            artic["pages"] = li.select('div')[1].get_text().strip()

        for(k,v) in artic.items():
            print("{}:{}".format(k,str(v)))


def update_document(sqlite_file,doi):
    # sqlite_file='/Users/syk/Library/Application Support/Mendeley Desktop/sunyongke@gmail.com@www.mendeley.com.sqlite'
    #
    update_str="update Documents set confirmed=1,title='{}',abstract='{}',year={},volume={},issue={},pages='{}',publication='{}' where doi='{}'".format(
        artic["title"],artic["abstract"],artic["year"],artic["volume"],artic["issue"],artic["pages"],artic["publication"],doi
    )
    find_docid="select id from documents where doi='{}'".format(doi)
    print(sqlite_file)
    conn = sqlite3.connect(sqlite_file, isolation_level=None)
    c = conn.cursor()
    c.execute(update_str)
    c.execute(find_docid)
    row = c.fetchone()
    docid=row[0]
    delete_authors="delete from documentcontributors where documentid='{}'".format(docid)
    c.execute(delete_authors)
    for ah in artic["authors"]:
        insert_auth="insert into documentcontributors(documentid,contribution,lastname)values({},'DocumentAuthor','{}');".format(docid,ah)
        c.execute(insert_auth)

    delete_keywords = "delete from documentkeywords where documentid='{}'".format(docid)
    c.execute(delete_keywords)
    for key in artic["keywords"]:
        insert_keyword = "insert into documentkeywords(documentid,keyword)values({},'{}');".format(
            docid, key)
        c.execute(insert_keyword)

    conn.commit()
    c.close()
    conn.close()



def MendeleyDB():
    homedir=os.environ['HOME']
    mendeley_home="{}/Library/Application Support/Mendeley Desktop".format(homedir)
    f_list = os.listdir(mendeley_home)
    for i in f_list:
        if i.endswith("@www.mendeley.com.sqlite"):
            sqlite_file="{}/{}".format(mendeley_home,i)
            return sqlite_file



if __name__ == "__main__":
    description_text = "Mendeley sqlite database named <<yourEmailAddress>>@www.mendeley.com.sqlite, or online.sqlite if no email address used with Mendeley. Mendeley Desktop database file locations: ||Windows Vista/Windows 7: %LOCALAPPDATA%\Mendeley Ltd.\Mendeley Desktop ||Windows XP: C:\Documents and Settings\<<Your Name>>\Local Settings\Application Data\Mendeley Ltd\Mendeley Desktop ||Linux: ~/.local/share/data/Mendeley Ltd./Mendeley Desktop/ ||MacOS: Macintosh HD -> /Users/<<Your Name>>/Library/Application Support/Mendeley Desktop/"
    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument("--doi", help="Updates metaInfor for all chinese article by doi from http://dx.doi.org",required=True)
    args = parser.parse_args()
    if args.doi:
        print("gets DOI")
        dbfile=MendeleyDB()
        get_DOI(args.doi)
        update_document(dbfile,args.doi)
