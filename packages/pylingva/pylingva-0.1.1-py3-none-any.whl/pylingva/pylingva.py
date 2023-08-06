#! /usr/bin/env python

import requests as req

class pylingva:
    
    def __init__(self):
        self.url_list = ("https://lingva.ml", "https://translate.alefvanoon.xyz", "https://translate.igna.rocks", "https://lingva.pussthecat.org")
        for url in self.url_list:
            check_url = req.get(url)
            status = check_url.status_code
            if status == 200:
                self.url = url + "/api/v1/"
                break
            else:
                self.url = 0

    def languages(self):
        if self.url == 0:
            print("Server Down !")
        else:
            url = self.url + "languages"
            all_languages = req.get(url)
            all_languages = all_languages.json()
            lang = {}
            for x in range(0, len(all_languages['languages'])):
                list_code = all_languages['languages'][x]['code']
                list_name = all_languages['languages'][x]['name']
                lang.update({list_name: list_code})
            return lang

    def translate(self, source, target, text):
        if self.url == 0:
            print("Server Down !")
        else:
            url = f"{self.url}/{source}/{target}/{text}"
            url = url.replace("?", "%3F")
            r = req.get(url)
            r = r.json()
            result = r['translation']
            return result

