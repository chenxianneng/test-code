import requests
from lxml import etree
from urllib.request import urlretrieve

url = 'https://www.2717.com'
show_num = 0


for page_num in range(217):
    page = 'https://www.2717.com/ent/meinvtupian/list_11_' + str(page_num+1) + '.html'

    result = requests.get(page)
    html = etree.HTML(result.content)

    # div_list = html.xpath('/html/body/div[2]/div[7]/ul/li[1]/a[1]/i/img')
    # for item in div_list:
    #     print(item.get('src'))
    #     urlretrieve(item.get('src'), './image/test.jpg')

    for i in range(30):
        path = '/html/body/div[2]/div[7]/ul/li[' + str(i+1) + ']/a[1]'
        #print(path)
        div_list = html.xpath(path)
        for item in div_list:
            girl_path = url + item.get('href')
            #print(girl_path)

            html_result = requests.get(girl_path)
            html_detail = etree.HTML(html_result.content)
            elem_list = html_detail.xpath('//*[@id="pageinfo"]')
            for elem in elem_list:
                #print(elem.get('pageinfo'))
                image_count = int(elem.get('pageinfo'))
                for image_num in range(image_count):
                    #print(girl_path)
                    a = girl_path.split('.')
                    image_url = a[0] + '.' + a[1] + '.' + a[2] + '_' + str(image_num + 1) + '.html'
                    print(image_url)

                    try:
                        image_result = requests.get(image_url)
                        html_image = etree.HTML(image_result.content)
                        image = html_image.xpath('//*[@id="picBody"]/p/a[1]/img')
                        for item in image:
                            #print(item.get('src'))
                            if show_num <= 6962:
                                show_num += 1
                                continue

                            urlretrieve(item.get('src'), './image/' + str(show_num) + '.jpg')
                            show_num += 1
                    except Exception as e:
                        pass


#完工，拜拜
