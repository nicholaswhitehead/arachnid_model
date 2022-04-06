import requests
import pandas as pd
import shutil
import os
from bs4 import BeautifulSoup

def scrape():
    page = "https://spiderid.com/locations/united-states/north-carolina/"
    result = requests.get(page)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
    else:
        print("TERMINATED EARLY", flush=True)
        return None

    links = []    
    for link in soup.find_all('a'):
        links.insert(0,link.get('href'))

    species_pages = []
    for link in links:
        if "/pictures/" in link and "https" in link:
            species_pages.insert(0,link)
    # format of link: https://spiderid.com/spider/agelenidae/agelenopsis/naevia/pictures/

    for page in species_pages:
        result = requests.get(page)
        if result.status_code == 200:
            soup = BeautifulSoup(result.content, "html.parser")
        else:
            print("TERMINATED EARLY", flush=True)
            return None

        species_parts = page.split('/')
        # format: [ 'https:', '', 'spiderid.com', 'spider', 'agelenidae', 'agelenopsis', 'naevia', 'pictures', '']
        species_name = species_parts[-4]+"_"+species_parts[-3]
        # format: agelenopsis_naevia

        # Band-aid for previously-aborted run. Use to exclude certain species in future runs.  
        # used = ["agelenopsis_naevia", "amaurobius_ferox", "araneus_bicentenarius", "araneus_marmoreus", "araneus_nordmanni", "araniella_displicata", "argiope_aurantia"]
        # if species_name in used:
        #     continue

        species_directory = "C:/Users/Nicholas/Documents/arachnID/spiderid_images/"+species_name+"/"
        os.makedirs(os.path.dirname(species_directory), exist_ok=True)

        links = []    
        for link in soup.find_all('a'):
            links.insert(0,link.get('href'))
        image_pages = []
        for link in links:
            if "/picture/" in link and "#comments" not in link:
                image_pages.insert(0,"https://spiderid.com"+link)
        image_pages = image_pages[1::2]
        # link of format: https://spiderid.com/picture/4699/

        for image_page in image_pages:
            result = requests.get(image_page)
            if result.status_code == 200:
                soup = BeautifulSoup(result.content, "html.parser")
            else:
                print("TERMINATED EARLY", flush=True)
                return None
            link = soup.find('img', class_="imageFull aligncenter spiderPicture").get('src')
            filename = link.split("/")[-1]

            result = requests.get(link, stream = True)
            if result.status_code == 200:
                result.raw.decode_content = True
                with open(species_directory+filename,'wb') as f:
                    shutil.copyfileobj(result.raw, f)
            else:
                print("TERMINATED EARLY", flush=True)
                return None


if __name__ == "__main__":
    scrape()