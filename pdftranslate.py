# -*- coding: gbk -*-
import os, sys, urllib2, re, json
def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def textprocess(c):
    for i in ['-\n']:
        c = c.replace(i, '')
    for i in ',.;()\"\'“”:1234567890':
        c = c.replace(i, '')
    c = c.replace('\n', ' ').split(' ')
    return list(set(map(lambda x: x.lower(), c)))

def makedic(threshold):
    f = open(cur_file_dir() + '\wordfrequence.csv', 'r')
    c = f.readlines()
    f.close()
    c = map(lambda x: x.replace('\n', ''), c)
    f = open(cur_file_dir() + '\junior', 'r')
    c2 = f.readlines()
    f.close()
    j = map(lambda x: x.replace('\n', ''), c2)
    return c[:threshold], c[threshold:], j

def translate(word):
    query = word.replace('\n', '%0')
    url = 'http://fanyi.baidu.com/v2transapi'
    req=urllib2.Request(url)
    resp=urllib2.urlopen(url, data='from=en&to=zh&query={0}&transtype=realtime&simple_means_flag=3'.format(word))
    resphtml=resp.read()
    d = json.loads(resphtml)
    l = map(lambda x: (str(x['src']) + ',' + x['dst'].encode('gbk')), d['trans_result']['data'])
    return l
     

def main(filename):
    print 'start process with', filename
    d = makedic(2000)
    txtname = filename[:-3] + 'txt'
    print 'start change PDF to txt.'
    os.system('pdf2txt.py -o \"{0}\" \"{1}\"'.format(txtname, filename))
    f = open(txtname, 'r')
    c = f.read()
    f.close()
    print 'success'
    c = textprocess(c)
    l = []
    for i in c:
        if i in d[1] and (not i in d[0]) and (not i in d[2]):
            l.append(i)
    l.sort()
    print '\nstart to translate.'
    l = translate('\n'.join(l))
    print 'success'
    f = open(txtname[:-3]+'csv', 'w')
    map(lambda x:f.write(x + '\n'), l)
    f.close()
    os.remove(txtname)
    
main(sys.argv[1])
#main('2016-3-7/PNAS-2014.pdf')


