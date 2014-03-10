#!/usr/bin/env python
# ^-^ coding: utf-8 ^-^
import os
import string
import urllib
import simplejson

'''
Simple class for downloading high quality music randomly from baidu fm.
'''

__author__ = "Libitum@about.me"

class BaiduFmDownloader:
    def __init__(self):
        self.channel_id = ""
        self.music_list = []

    def __get_music_list(self):
        html = urllib.urlopen("http://fm.baidu.com/dev/api/?tn=playlist&format=json&id="+urllib.quote(self.channel_id)).read()
        json = simplejson.loads(html)
        ids = []
        for item in json['list']:
            ids.append(item['id'])

        ids = string.join([str(i) for i in ids], ',')
        html = urllib.urlopen("http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds="+urllib.quote(ids)).read()
        json = simplejson.loads(html)
        data = json['data']['songList']
        for item in data:
            if item['songLink']:
                self.music_list.append((item['songName'], item['songLink']))

        
    def __get_next(self):
        if not self.music_list:
            self.__get_music_list()

        return self.music_list.pop()


    def get_channel_list(self):
        html = urllib.urlopen("http://fm.baidu.com").read()
        start = html.find("{", html.find("rawChannelList"))
        end = html.find(";", start)
        json = html[start:end].strip()
        data = simplejson.loads(json)
        return data["channel_list"]


    def download(self, num):
        if not self.channel_id:
            print "no channel id set."
            return

        os.mkdir("mp3")
        i = 0
        while i < num:

            name, url = self.__get_next()
            file_path = os.path.join("mp3", "%s.mp3" % name)
            if os.path.exists(file_path):
                continue

            print "%d\t%s" % (i, name)
            urllib.urlretrieve(url, file_path)

            i = i+1


if __name__ == '__main__':
    dl = BaiduFmDownloader()
    #dl.channel_id="public_tuijian_suibiantingting"
    #dl.download(50)
    list = dl.get_channel_list()
    for i, item in enumerate(list):
        print "%2d\t%10s\t%10s" % (i, item["channel_name"].strip(), item["cate"].strip())

    index = raw_input("Please input the index of channel: ")
    dl.channel_id = list[int(index)]["channel_id"]
    dl.download(3)

