import urllib
from urllib import request
from html.parser import HTMLParser

class Parse(HTMLParser):
    usd_rub_exchange_rate = ''
    def __init__(self):
    #Since Python 3, we need to call the __init__() function of the parent class
        super().__init__()
        self.reset()
    #Defining what the method should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "input":
            # print(attrs)
            try:
                if attrs[1][0] == 'id' and attrs[1][1] == 'course_3':
                    Parse.usd_rub_exchange_rate = float(attrs[2][1].replace(',', '.'))
            except:
                pass
           # for key,value in attrs:
           #     if key == 'id' and value == 'course_3':
           #         if key == "value":
           #             Parse.usd_rub_exchange_rate = float(value.replace(',','.'))



#ресурс - https://moskva.vbr.ru/banki/kurs-valut/prodaja-usd/
#искомый тэг - '<input type="hidden" id="course_3" value="73,7" name="course">'
response = urllib.request.urlopen("https://moskva.vbr.ru/banki/kurs-valut/prodaja-usd/")
html = response.read()
html = html.decode()
# print(html)

p = Parse()
# html = '<input type="hidden" id="course_3" value="73,7" name="course">'
p.feed(html)
result = p.usd_rub_exchange_rate
print(result)

from html.parser import HTMLParser

def get_exchange_rate():
    p = Parse()
    # html = '<input type="hidden" id="course_3" value="73,7" name="course">'
    p.feed(html)
    result = p.usd_rub_exchange_rate
    return result
