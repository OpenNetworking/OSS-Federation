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

from django.core.exceptions import ObjectDoesNotExist
from oss.apps.chart.models import Tx


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
        
        self.since_time = 0
        self.page_queue = Queue.LifoQueue() 

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
