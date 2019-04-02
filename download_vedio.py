import sys
from you_get import common as you_get

directory = r'D:\1'
url = 'https://v.youku.com/v_show/id_XNDA5MjkxMTAwMA==.html?spm=a2h03.12024492.drawer3.dzj2_1&scm=20140719.rcmd.1694.show_efbfbdebb88eefbfbd25'
sys.argv = ['you-get','-o',directory, url]
you_get.main()
