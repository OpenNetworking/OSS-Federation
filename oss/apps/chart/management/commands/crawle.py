#!usr/bin/env python 
import sys
import time
import json
import Queue
import threading
import urllib2

from bs4 import BeautifulSoup
from pyquery import PyQuery

from django.core.management.base import BaseCommand, CommandError
from oss.apps.chart.models import Tx

'''
def Paginator(num_pages):
    for page in range(num_pages):
        yield page+1

def get_num_page(url):
    url = url + '&verbose=0'
    doc = PyQuery(url)

    total_page = json.loads(doc('p').text())['data']['num_pages']
    return total_page

class BaseThread(threading.Thread):
    def __init__(self, url, crawlDepth, pa):
        self.url = url
        self.paginator = pa

        self.threads = []
        self.concurrency = 0
        self.max_outstanding = crawlDepth
        self.binary_semaphore = threading.Semaphore(1)
        self.write_lock = threading.Semaphore(1)
        threading.Thread.__init__(self)
    
    # override run() method, it's an entry point for a thread 
    def run(self):
        self.spawn_new_worker()
        
        # the thread should wait until all its worker done
        while self.threads:
            try:
                for t in self.threads:
                    t.join(1)
                    if not t.isAlive():
                        self.threads.remove(t)
            except KeyboardInterrupt, e:
                sys.exit(1)
    
    def spawn_new_worker(self):
        self.binary_semaphore.acquire()
        self.concurrency +=1
        
        try:
            page_id = self.paginator.next()
            print '* Starting thread %d' % self.concurrency
            t = threading.Thread(target=self.consumer, args=(self.concurrency, page_id,))
            t.daemon = True
            t.start()
            self.threads.append(t)
        except StopIteration:
            # all pages have been dispatched to diff threads
            # you don't need to start a new worker
            self.concurrency -=1
        finally:
            self.binary_semaphore.release()

    # first-phase job, 
    # a common procedure for different api crawler
    def get_soup_by(self, page_id):
        url = self.url + '&page=%s' % page_id
        page = urllib2.urlopen(url)
        
        soup = BeautifulSoup(page.read())
        return soup 
    
    # second-phase job
    # should be implemented for different api crawler
    def grab_into_db(self, tid, soup):
        raise NotImplementedError("Please Implement this method")
    
    
    
    def consumer(self, tid, page_id):
        print '*** %s ***: working on page: %s' % (tid, page_id) 
        # first-phase Job: crawl website
        soup = self.get_soup_by(page_id)
        
        # check whether meet max_outstanding threads or not
        if self.concurrency < self.max_outstanding:
            self.spawn_new_worker()
        
        # second-phase Job: insert Data into DB
        self.grab_into_db(tid, soup)
        
        print '*** %s *** : finish page: %s' % (tid, page_id) 
        
        # Actively querying remainder pages
        self.binary_semaphore.acquire()
        while True:
            try:
                page_id = self.paginator.next()
                self.binary_semaphore.release()
                
                print '*** %s ***: working on page: %s' % (tid, page_id) 
                soup = self.get_soup_by(page_id)
                
                if self.concurrency < self.max_outstanding:
                    self.spawn_new_worker()
                
                self.grab_into_db(tid, soup)
                print '*** %s *** : finish page: %s' % (tid, page_id) 
           
            except StopIteration:
                self.binary_semaphore.release()
                break

        self.binary_semaphore.acquire()
        self.concurrency -= 1
        self.binary_semaphore.release()



class TxThread(BaseThread):
    def __init__(self, url, crawlDepth, pa):
        BaseThread.__init__(self, url, crawlDepth, pa)

    # implement the method for second-phase job
    def grab_into_db(self, tid, soup):
        rows = json.loads(soup.get_text())['data']['transaction']
        
#        self.write_lock.acquire()
        for row in rows:
            print '[%s]: tx_id %s ' %(tid, row['tx_index'])
            tx = Tx(tx_id = row['tx_index'],
                    tx_hash = row['hash'],
                    tx_type = row['type'],
                    tx_color = row['color'],
                    total_in = row['total_in'],
                    total_out = row['total_out'],
                    tx_ntime = row['time']
                    )
            tx.save(using='chart_db')
#        self.write_lock.release()
'''

def get_soup_by(self, page_id):
    url = self.url + '&page=%s' % page_id
    page = urllib2.urlopen(url)
    
    soup = BeautifulSoup(page.read())
    return soup 


class GinfoCrawler(object):
    def __init__(self):
        self.url = "http://140.112.29.198:8080/api/v1/tx-chart?type=longest"
        self.threads = []
        self.concurrency = 0
        self.max_outstanding = 32
        self.concurrency_lock = threading.Lock()
        
        self.page_queue = Queue.LifoQueue() 

    def init_queue(self):
        url = self.url + '&verbose=0'
        doc = PyQuery(url)
        
        total_pages = json.loads(doc('p').text())['data']['num_pages']
        for idx in range(int(total_pages)):
            self.page_queue.put(idx+1)


    def start(self):
        self.init_queue()
        self.spawn_new_worker()
        
        # main thread should wait until all its childs done
        while self.threads:
            try:
                for t in self.threads:
                    t.join(1)
                    if not t.isAlive():
                        self.threads.remove(t)
            except KeyboardInterrupt, e:
                sys.exit(1)
    
    # first-phase job
    def get_soup_by(self, page_id):
        url = self.url + '&page=%s' % page_id
        page = urllib2.urlopen(url)
        
        soup = BeautifulSoup(page.read())
        return soup 
    
    # second-phase job
    def grab_into_db(self,  soup):
        rows = json.loads(soup.get_text())['data']['transaction']
        
        for row in rows:
            tx = Tx(tx_id = row['tx_index'],
                    tx_hash = row['hash'],
                    tx_type = row['type'],
                    tx_color = row['color'],
                    total_in = row['total_in'],
                    total_out = row['total_out'],
                    tx_ntime = row['time']
                    )
            tx.save(using='chart_db')
    
    
    def spawn_new_worker(self):
        self.concurrency_lock.acquire()
        self.concurrency += 1
        t = threading.Thread(target=self.consumer, args=(self.concurrency,))
        t.daemon = True
        self.threads.append(t)
        t.start()
        self.concurrency_lock.release()

    def consumer(self, tid):
        while not self.page_queue.empty():
            try:
                print '* Starting thread %d' % tid
                page = self.page_queue.get()
                print '[%s]: page %s' %(tid, page)
                
                soup = self.get_soup_by(page)
                if self.concurrency < self.max_outstanding:
                    self.spawn_new_worker()
                
                self.grab_into_db(soup)
                
            except Queue.Empty, e:
                print 'All pages have been queried'
                

        self.concurrency_lock.acquire()
        self.concurrency -= 1
        self.concurrency_lock.release()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        gc = GinfoCrawler()
        gc.start()



if __name__ =='__main__':
    gc = GinfoCrawler()
    gc.start()
