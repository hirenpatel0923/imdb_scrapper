import requests, csv, time
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing
import concurrent.futures
from TorCrawler import TorCrawler
from imdb.imdb_movie.imdb_movie import ImdbMovie

def get_title(process_name, page_soup, url):
    all_link = page_soup.find_all('a', href=True)
    with open(process_name + 'title.csv','w') as f:
        lst = []
        for link in all_link:
            if '/title/' in link['href']:
                split_link = link['href'].split('/')

                if split_link[2] not in lst:  #check for duplicate title
                    imdb_title = ImdbMovie(title=split_link[2])
                    lst.append(imdb_title.title)
                    f.write(imdb_title.title + ',' +
                            imdb_title.title_name + ',' +
                            str(imdb_title.ratings) + ',')

                    for director in imdb_title.director:
                        f.write(director + ' ')
                    f.write(',')

                    for genre in imdb_title.genres:
                        f.write(genre + ' ')
                    f.write(',')

                    for cast in imdb_title.get_cast_list():
                        f.write(cast + ' ')
                    f.write(',')

                    for plot_key in imdb_title.get_plot_keywords_list():
                        f.write(plot_key + ' ')

                    f.write('\n')

                    print('process : ' + str(process_name) + ' link : '+ str(len(lst)))


                

def seq(url, crawler, session):
    crawler.rotate()
    r = session.get(url)
    return r.status_code

def worker(workerQueue, session, page_num):
    ip_text = ''
    crawler = TorCrawler()
    url = "https://www.imdb.com/list/ls055462533/?ref_=tt_rls_2&sort=release_date,desc&st_dt=&mode=detail&page="+ str(page_num)
    print('page : ', page_num)
    print('url : ', url)
    with concurrent.futures.ThreadPoolExecutor(5) as thread_ex:
        f_t_u = {thread_ex.submit(seq, url, crawler, session): url}
        for x in concurrent.futures.as_completed(f_t_u):
            code = x.result()
            
            ip = session.get('http://www.httpbin.org/ip')
            if ip.text != ip_text:
                ip_text = ip.text
                print(ip_text)
            
            try:
                if code == 200:
                    page = session.get(f_t_u[x])
                    page_soup = BeautifulSoup(page.text, 'html.parser')
                    get_title(multiprocessing.current_process().name, page_soup, f_t_u[x])
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    session = requests.Session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9150'
    session.proxies['https'] = 'socks5h://localhost:9150'


    start_cpu = time.clock()
    start = time.time()
    workerQueue = multiprocessing.Queue()
    procs = []
    

    for i in range(18):
        p = multiprocessing.Process(target=worker, args=(workerQueue, session, i))
        procs.append(p)
        p.start()
 
    workerQueue.close()
    workerQueue.join_thread()

    for proc in procs:
        proc.join()
    stop = time.time()
    print('CPU time:', time.clock() - start_cpu)
    print('Execution time:', stop - start)