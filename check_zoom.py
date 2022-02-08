from optparse import Option
from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os.path
import sys

def main(dns: str, pos: int):
    i = pos
    j = 0
    with open(dns) as input, open("./zoom.txt", "a") as zoom, open("./nozoom.txt", "a") as nozoom, open("./pos.txt", "a") as pos:
        for dns in input:
            j = j + 1
            if j < i:
                continue
            zoom.flush()
            nozoom.flush()
            pos.flush()
            
            pos.writelines(str(i) + "\n")
            if i % 15 == 0:
                print("Restart Tor!")
                system('C:\\TorBrowser\\Tor\\tor.exe --service stop')
                system("taskkill.exe /IM tor.exe /f")
                system('C:\\TorBrowser\\Tor\\tor.exe --service start')
                sleep(20)
            i = i + 1
            is_zoom = False
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
            driver.get("https://duckduckgo.com/?q=site%3Azoominfo.com+" + dns + "&t=h_&ia=web")
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                link = elem.get_attribute("href")
                if link.startswith('https://www.zoominfo.com/c/'):
                    zoom.writelines(dns[:-1] +";"+link+"\n")
                    print(dns[:-1] +";"+link)
                    is_zoom = True
                    break
            if is_zoom == False:
                nozoom.writelines(dns)
                print(dns)
                

if __name__ == "__main__":
    dns = ""
    pos = 0
    try:
        dns = sys.argv[1]
        os.path.isfile(dns)
    except Exception as ex:
        print(ex)
        exit()
    try:
        pos = int(sys.argv[2])
    except:
        pos = 0
    print("Path to dns: " + dns)
    print("Starting position: " + str(pos))
    main(dns, pos)