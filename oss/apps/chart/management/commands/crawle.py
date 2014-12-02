#!usr/bin/env python 
import sys
import math
import time
import json
import Queue
import threading
import urllib2

from bs4 import BeautifulSoup
from pyquery import PyQuery

from django.core.management.base import BaseCommand, CommandError

from django.core.exceptions import ObjectDoesNotExist
from oss.apps.chart.models import Tx
from oss.apps.chart.models import Block



class BaseCrawler(object):
    def __init__(self):
        # need to override self.url for crawling different ginfo's api
        self.url = "ginfo@apiserver"
        self.threads = []
        self.concurrency = 0
        self.max_outstanding = 16
        self.concurrency_lock = threading.Lock()
        
        self.since_time = 0
        self.page_queue = Queue.LifoQueue() 
    
    #@abstractmethod
    def init_queue(self):
        # get the newest model object in db
        raise NotImplementedError("Please Implement this method")



    # entry point for the crawler
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
   

    # first-phase job for each worker
    #@abstractmethod
    def get_soup_by(self, page_id):
        raise NotImplementedError("Please Implement this method")
   

    # second-phase job for each worker
    #@abstractmethod
    def grab_into_db(self,  soup):
        raise NotImplementedError("Please Implement this method")
   

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


class TxCrawler(BaseCrawler):
    def __init__(self):
        super(TxCrawler, self).__init__()
        self.url = "http://140.112.29.198:8080/api/v1/tx-chart?type=longest"

    
    def init_queue(self):
        # get the newest tx_time in DB
        try:
            last_tx = Tx.objects.using('chart_db').latest('tx_ntime')
            self.since_time = last_tx.tx_ntime
        except ObjectDoesNotExist:
            print 'DB have no data, try to initialize'
        
        url = self.url + '&since=%s&verbose=%s' % (self.since_time, 0)
        doc = PyQuery(url)
        
        total_pages = json.loads(doc('p').text())['data']['num_pages']
        for idx in range(int(total_pages)):
            self.page_queue.put(idx+1)

    # first-phase job
    def get_soup_by(self, page_id):
        url = self.url + '&since=%s&page=%s' % (self.since_time, page_id)
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



class BlockCrawler(BaseCrawler):
    def __init__(self):
        super(BlockCrawler, self).__init__()
        self.url = "http://140.112.29.198:8080/api/v1/blk-chart"
    
    def init_queue(self):
        # get the newest block_ntime in DB
        try:
            last_block = Block.objects.using('chart_db').latest('block_ntime')
            self.since_time = last_block.block_ntime
        except ObjectDoesNotExist:
            print 'DB have no data, try to initialize'
        
        url = self.url + '?verbose=%s&since=%s' % (0, self.since_time)
        doc = PyQuery(url)
         
        total_count = json.loads(doc('p').text())['data']['total_count']
        total_pages = math.ceil(total_count /500.0) 
        for idx in range(int(total_pages)):
            self.page_queue.put(idx+1)

    # first-phase job
    def get_soup_by(self, page_id):
        url = self.url + '?since=%s&page=%s' % (self.since_time, page_id)
        page = urllib2.urlopen(url)
        
        soup = BeautifulSoup(page.read())
        return soup 

    # second-phase job
    def grab_into_db(self,  soup):
        rows = json.loads(soup.get_text())['data']['block']
        
        for row in rows:
            block = Block(block_id = row['block_index'],
                    block_hash = row['hash'],
                    block_miner = row['miner'],
                    block_hashmerkleroot = row['mrklroot'],
                    block_ntime = row['time'],
                    block_height = row['height']
                    )
            block.save(using='chart_db')

def blk_worker():
    bc = BlockCrawler()
    bc.start()

def tx_worker():
    tc = TxCrawler()
    tc.start()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        master_threads = []
        t1 = threading.Thread(target=blk_worker)
        t2 = threading.Thread(target=tx_worker)
        master_threads.append(t1)       
        master_threads.append(t2)
        t1.daemon = True
        t2.daemon = True
        
        t1.start()
        t2.start()
        while master_threads:
            try:
                for t in master_threads:
                    t.join(1)
                    if not t.isAlive():
                        master_threads.remove(t)
            except KeyboardInterrupt, e:
                sys.exit(1)


if __name__ =='__main__':
    bc = BlockCrawler()
    bc.start()
