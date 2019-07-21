# coding: utf-8
import requests
import threading
import queue


class Crawler(object):
    def __init__(self, token, uid):
        self.headers = {
            "referer": "https://servicewechat.com/wx3a0dd0d2034a7b9a/6/page-frame.html",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.101 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/appbrand2",
            "Host": "smart.welearn.biz",
            "Connection": "close"
        }
        # token need captured in wechat
        self._host = "https://smart.welearn.biz"
        self._words_api = "/api/words/getWordsList"
        self._words_type_detail_api = "/api/words/getWordstypeDetail"
        self._token = token
        self._uid = uid
        # the code in we learn app
        self.word_type_id_dict = {
            "托福词书": 6,
            "考研词书": 5,
            "六级词书": 4,
            "四级词书": 3,
            "大学英语四六级": 2,
            "大学英语必备词汇": 1
        }

    def get_word(self, words_type_id, page):
        data = {
            "words_type_id": words_type_id,
            "page": page,
            "token": self._token,
            "uid": self._uid
        }
        proxy = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        # debug by burp suite
        # r = requests.post(self._host + self._words_api, headers=self.headers, json=data, proxies=proxy, verify=False)
        r = requests.post(self._host + self._words_api, headers=self.headers, json=data)
        return r.json()

    def get_word_thread(self, data_queue: queue.Queue, response_queue: queue.Queue):
        while not data_queue.empty():
            data = data_queue.get()
            res = self.get_word(**data)
            print(res)
            response_queue.put(res)

    def get_words_type_detail(self, words_type_id):
        data = {
            "words_type_id": words_type_id,
            "token": self._token,
            "uid": self._uid
        }
        try:
            r = requests.post(self._host + self._words_type_detail_api, headers=self.headers, json=data)
            return r.json().get("data")
        except Exception as e:
            print(e)
            return None

    def get_all_words(self, words_type_id, thread_count=10):
        # init 2 queue
        words_info = self.get_words_type_detail(words_type_id)
        if not words_info:
            print("get words type detail error, default crawl 2000 words")
            word_count = 2000
        else:
            name = words_info.get("name")
            word_count = words_info.get("count")
            print(
                "name: {}\ncount: {}".format(name, word_count)
            )
        data_queue = queue.Queue()
        response_queue = queue.Queue()
        for i in range(1, word_count + 1):
            data = {
                "words_type_id": words_type_id,
                "page": i
            }
            data_queue.put(data)

        for _ in range(thread_count):
            t = threading.Thread(target=self.get_word_thread, args=(data_queue, response_queue))
            t.start()

        while not response_queue.empty() or threading.active_count() > 1:
            if response_queue.empty():
                continue
            with open("data", "a+") as f:
                f.write(str(response_queue.get()) + "\n")


if __name__ == '__main__':
    token = ""
    uid = ""
    c = Crawler(token, uid)
    c.get_all_words(5)

