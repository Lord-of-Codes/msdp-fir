from bs4 import BeautifulSoup as bs
import requests
import os
from pathlib import Path
from requests.structures import CaseInsensitiveDict
import time

stations = [
    "Beldanga Police Station",                
    "Berhampore Police Station",                
    "Daulatabad Police Station",               
    "Harihapara Police Station",                 
    "Nowda Police Station",          
    "Rejinagar Police Station", 
    "Saktipur Police Station",                  
    "Berhampore Women Police Station", 
    "Bhagawangola Police Station", 
    "Jiaganj Police Station",                 
    "Lalgola Police Station",                 
    "Murshidabad Police Station", 
    "Nabagram Police Station",                 
    "Ranitala Police Station",                
    "Bharatpur Police Station", 
    "Burwan Police Station",                  
    "Kandi Police Station",                  
    "Khargram Police Station",              
    "Salar Police Station",                 
    "Domkal Police Station",                 
    "Islampur Police Station",                
    "Jalangi Police Station",                 
    "Raninagar Police Station", 
    "Sagarpara Police Station", 
    "Cyber Crime Police Station" 
    ]

url = "http://mspdfir.co.in/view/index.php"

for station in  stations:
    file = {
        'date': (None, '2000-01-01'),
        "date1": (None, '2022-12-31'),
        "psname": (None, station),
        "save": (None, "")
    }

    # print(requests.Request('POST', url, files=dict(file)).prepare().body.decode('utf8'))
    resp = requests.post(url, files=dict(file))
    page = bs(resp.content, features="html.parser")
    print("\n\n"+station +" main page fetched\n")

    a = page.find_all("a")
    for link in a:

        if "/file_fir/" in link.get("href"):
            pdf_url = "http://mspdfir.co.in" + link.get("href").replace("..", "")

            path = Path.cwd().joinpath("data", station)
            path.mkdir(parents=True, exist_ok=True)

            try:
                filename =  path.joinpath(pdf_url[pdf_url.rfind('/')+1:])
            except:
                continue

            if os.path.exists(filename):
                print("\033[93m" + pdf_url + "\tfile already present")
                continue

            try:
                start = time.perf_counter()
                pdfx = requests.get(pdf_url, timeout=10)
                request_time = time.perf_counter() - start
            except Exception as e:
                print("\033[91m" + pdf_url + "\tget request exception")
                continue

            filename.write_bytes(pdfx.content)
            print("\033[32m"+ pdf_url + "\tdownloaded\t" + str(request_time) +" secs")
 



