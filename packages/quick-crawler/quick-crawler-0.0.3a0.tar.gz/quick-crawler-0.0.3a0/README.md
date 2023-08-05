# Quick Crawler

A toolkit for quickly performing crawler functions

## Installation
```pip
pip install quick-crawler
```

## Functions
1. get a html page and can save the file if the file path is assigned.
2. get a json object from html string
3. get or download a series of url with similar format, like a page list
4. remove unicode str
5. get json object online
6. read a series of obj from a json list online
7. quick save csv file from a list of json objects
8. quick read csv file to a list of fields
9. quick download a file

## Let Codes Speak
Example 1: 
```python
from quick_crawler.page import *

if __name__=="__main__":
    # get a html page and can save the file if the file path is assigned.
    url="https://learnersdictionary.com/3000-words/alpha/a"
    html_str=quick_html_page(url)
    print(html_str)

    # get a json object from html string
    html_obj=quick_html_object(html_str)
    word_list=html_obj.find("ul",{"class":"a_words"}).findAll("li")
    print("word list: ")
    for word in word_list:
        print(word.find("a").text.replace("  ","").strip())

    # get or download a series of url with similar format, like a page list
    url_range="https://learnersdictionary.com/3000-words/alpha/a/{pi}"
    list_html_str=quick_html_page_range(url_range,min_page=1,max_page=10)
    for idx,html in enumerate(list_html_str):
        html_obj = quick_html_object(html)
        word_list = html_obj.find("ul", {"class": "a_words"}).findAll("li")
        list_w=[]
        for word in word_list:
            list_w.append(word.find("a").text.replace("  ", "").strip())
        print(f"Page {idx+1}: ", ','.join(list_w))



```

Example 2: 
```python
from quick_crawler.page import *

if __name__=="__main__":
    # remove unicode str
    u_str = 'aà\xb9'
    u_str_removed = quick_remove_unicode(u_str)
    print("Removed str: ", u_str_removed)

    # get json object online
    json_url="http://soundcloud.com/oembed?url=http%3A//soundcloud.com/forss/flickermood&format=json"
    json_obj=quick_json_obj(json_url)
    print(json_obj)
    for k in json_obj:
        print(k,json_obj[k])

    # read a series of obj from a json list online
    json_list_url = "https://jsonplaceholder.typicode.com/posts"
    json_list = quick_json_obj(json_list_url)
    print(json_list)
    for obj in json_list:
        userId = obj["userId"]
        title = obj["title"]
        body = obj["body"]
        print(obj)

    # quick save csv file from a list of json objects
    quick_save_csv("news_list.csv",['userId','id','title','body'],json_list)

    # quick read csv file to a list of fields
    list_result=quick_read_csv("news_list.csv",fields=['userId','title'])
    print(list_result)

    # quick download a file
    quick_download_file("https://www.englishclub.com/images/english-club-C90.png",save_file_path="logo.png")


```

## License
The `quick-crawler` project is provided by [Donghua Chen](https://github.com/dhchenx). 

