#! python

import requests
import bs4
import logging
import sys
#logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(message)s')
base_site_url = 'https://xkcd.com/'
images_to_download = 1
logging.debug('%s', sys.argv)

def help_string():
    print('''Digite o número de páginas a se baixar \
como último argumento.
Exemplo: python arquivo.py 3''')
    
def get_response(base_site_url):
    try:
        response = requests.get(base_site_url)
        print('Downloading Page...')
        response.raise_for_status()
        print(response.status_code)
    except Exception as erro:
        print('Não foi possível realizar o pedido. Erro:', erro)
    return response

def download_image(response, comic_number):
    
    bs4_base = bs4.BeautifulSoup(response.text, features='html.parser')
    previus_comic_url = 'https://xkcd.com' + bs4_base.find('a', rel='prev').get('href')
    comic_image_url = 'https:' + bs4_base.find_all('img')[2].get('src')
 
    image_downloaded = requests.get(comic_image_url)
    with open(comic_number+'comic.png', 'wb') as image:
        image.write(image_downloaded.content)
    return get_response(previus_comic_url) 
    

if len(sys.argv) > 1 and sys.argv[1].isnumeric():
    temporary_argv = int(sys.argv[1])
    logging.debug(':%s',temporary_argv)
    images_to_download =  temporary_argv if temporary_argv > 0 else None
    if images_to_download is None:
        raise Exception('0 ou menor, inválido.')
elif len(sys.argv) > 1 and sys.argv[1] == '-h':
    help_string()
    sys.exit()
else:
    print('Uma imagem será baixada...')
        

response = get_response(base_site_url)


for i in range(images_to_download):
    response = download_image(response, str(i))
    if images_to_download == 1:
        sys.exit()





