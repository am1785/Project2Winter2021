#################################
##### Name: Allen Mo
##### Uniqname: allenmo
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key


class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.

    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category="no category", name="no name", address="no address",
    zipcode="no zip", phone="no phone"):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        ''' Returns short summary of an instance of NationalSite

        Prarmeters
        ----------
        None

        Returns
        -------
        string
            a string following the convention specified below:
            <name> (<category>): <address> <zip>
        '''
        return f"{self.name} ({self.category}): {self.address} {self.zipcode}"


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    page = requests.get('https://www.nps.gov/index.htm')
    soup = BeautifulSoup(page.text, 'html.parser')
    state_url_soup = soup.find(class_='dropdown-menu SearchBar-keywordSearch').find_all('a')
    state_url_dict = {}
    for i in state_url_soup:
        state_url_dict[i.text] = "https://www.nps.gov" + i.get('href')
    return (state_url_dict)

def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    page = requests.get(site_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    name = soup.find('a',{'class':"Hero-title"}).text
    category = soup.find('span', {'class': 'Hero-designation'}).text
    address_local = soup.find('span', {'itemprop': "addressLocality"}).text
    address_region = soup.find('span', {'itemprop': "addressRegion"}).text
    address = address_local + ', ' + address_region
    zipcode = soup.find('span', {'itemprop': "postalCode"}).text[:5]
    phone = soup.find('span', {'itemprop': "telephone"}).text
    site = NationalSite(category= category, name=name, address=address, zipcode=zipcode, phone=phone)
    return site

def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    pass


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    pass
    

if __name__ == "__main__":
    print(get_site_instance("https://www.nps.gov/yell/index.htm").info())