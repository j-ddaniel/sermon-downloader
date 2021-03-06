#!Code written by joseph Daniel
'''this code is a based automated music downloader that searchs through the
naijasermons website and download all sermons from naijasermon website there. Please note
this may take time. I will upgrade the program to be multithreaded later
3
ReadMe
How to usea:
1. go to www.naijasermons.com.ng
2. Search for the preacher all messages.
3. Copy the link
4. Open cmd enter python joshua_selman.py
5. Wait patiently for all the messages to download
'''
import sys, os, requests,time, subprocess,logging, pyperclip
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from threading import Thread
import traceback
logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s -%(levelname)s - %(message)s')
def get_music_links(url):
    '''Get the url String given by the user from naija sermon
       return the links of all available sermon for the message of the url
    '''
    try:
        resp = requests.get(url)
        l = []
        logging.debug(resp)
        elem =bs(resp.text)
        link = elem.select('ol li a')
        logging.debug(type(link))
        for links in link:
            l.append(links.get('href'))
        return l
    except:
        errorMsg = 'Something went wrong... '
        error_to_log(traceback.format_exc(), errorMsg)
        

def error_to_log(error, errorMsg):
    '''
    Open a file called Log and write the error generated by the program to log
    '''
    with open('errorLog.txt', 'a') as log:
        log.write('----------------------------------------------------\n')
        log.write('%s \n %s \n'%(time.asctime(), error))
    print(errorMsg)
    print('Opening errorLog....')
    subprocess.Popen(['start', 'errorLog.txt'], shell=True)
    

def get_total_download(links):
    '''Get links String.
       Return the int toal length of the links string and also its int length divided by 10'''   
    logging.debug('Length: %d \n ThreadNum: %d'%(len(links), len(links)//10))
    return len(links), (len(links)//10)

def download_music(links):
    '''Get links string and the download the music storing them to file'''
    try:
        print(os.getcwd())
        os.makedirs('Music_download', exist_ok =True)
        for link in links:
            block_size =100000
            file_path = os.path.join('Music_download', os.path.basename(link))
            logging.debug('File Path : %s'%(file_path))
            print('Downloading to .... %s'%(file_path))
            download = requests.get(link, stream=True)
            total_size = int(download.headers.get('content-length', 0))
            progress = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open(file_path, 'wb') as file:
                      for chunks in download.iter_content(block_size):
                          file.write(chunks)
                          progress.update(len(chunks))
            print('%s downloaded'%(os.path.basename(link)))
    except:
        errorMsg = '%s cannot be downloaded due to unknown reason'%(os.path.basename(link))        
        error_to_log(traceback.format_exc(), errorMsg)
                  

def sermon(url):
    '''The main function of the program. Accept string url and initialize the progranm to download the music. Print done whne all music are completed'''
    try:
        links = get_music_links(url)
        length, threadNum = get_total_download(links)
        downloadThreads = []
        for i in range(0, length, threadNum):
            if i+threadNum < length:
                i_end = i+threadNum
            else:
                i_end =i + (length -i)
            logging.debug('%d : %d'%(i, i_end))
            argu = list(links[i: i_end])
            downloadthread = Thread(target=download_music, args = ((argu),))
            downloadThreads.append(downloadthread)
            downloadthread.start()
        for i in downloadThreads:
            i.join()
        print('Done Downloading all Music')
    except:
        errorMsg = 'Sorry this program can\'t be run'
        error_to_log(traceback.format_exc(), errorMsg)
def get_url():
     url = input('Enter Sermon Url: ')
     return url
#Text value
def main():
    if len(sys.argv) > 1:
        print('Downloading Sermon with Url: %s...'%(sys.argv[1]))
        url = sys.argv[1]
        sermon(url)
##    elif pyperclip.paste():
##        prompt = input('Is the sermon Url %s (Yes/No) '%(pyperclip.paste()))
##        if prompt.lower() == 'yes':
##           sermon(url)
##        else:
##            url = get_url()
##            sermon(url)
    else:
       sermon(get_url())

#Calling the main
main()
