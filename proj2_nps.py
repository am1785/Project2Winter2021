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
        state_url_dict[i.text.lower()] = "https://www.nps.gov" + i.get('href')
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
    page = requests.get(state_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    parks_soup = soup.find('ul', {'id': 'list_parks'}).find_all('div', {"class": "col-md-9 col-sm-9 col-xs-12 table-cell list_left"})

    site_urls = []
    for park in parks_soup:
        site_urls.append("https://www.nps.gov" + park.find('a').get('href'))
        print("FETCHING")

    national_sites = []
    for url in site_urls:
        national_sites.append(get_site_instance(url))
    return national_sites

def print_national_sites(national_sites):
    '''Format and print a list of national sites

    Parameters
    ----------
    national_sites: list
        a list of NationalSite objects to display

    Returns
    -------
    None
    '''
    for idx, site in enumerate(national_sites):
        print(f"[{idx + 1}] {site.info()}")

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
    base_url = "http://www.mapquestapi.com/search/v2/radius"
    params = {"key": secrets.API_KEY, "origin": site_object.zipcode, "radius": 10,
    "maxMatches": 10, "ambiguities": "ignore", "outFormat": "json"}
    response = requests.get(base_url, params=params)
    return response.json()


def print_nearby_places(mapquest_obj):
    '''Format the 10 nearby places return by the API as a list of strings
    following the convention of: <name> (<category>): <street address>, <city name>,
    and print it.

    Parameters
    ----------
    mapquest_obj: dict
        dictionary representation of MapQuest API's returned JSON object

    Returns
    -------
    None
    '''

    for idx, place in enumerate(mapquest_obj['searchResults']):
        name = place['fields']["name"] if (place['fields']["name"]) else "no name"
        category = place['fields']["group_sic_code_name"] if (place['fields']["group_sic_code_name"]) else "no category"
        address = place['fields']["address"] if (place['fields']["address"]) else "no address"
        city = place['fields']["city"] if (place['fields']["city"]) else "no city"
        print(f"{[idx+1]} {name} ({category}): {address}, {city}")



if __name__ == "__main__":

    #az_sites = get_sites_for_state('https://www.nps.gov/state/az/index.htm')
#    for i in az_sites:
#        print(i.info())
    #print(get_nearby_places(az_sites[0]))
    #print(print_nearby_places(get_nearby_places(az_sites[0])))
    res = ""

    us_states = {
    'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ',
    'Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT',
    'Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA',
    'Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN',
    'Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME',
    'Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN',
    'Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV',
    'New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
    'North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands':'MP',
    'Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR',
    'Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN',
    'Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA',
    'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
    }
    us_states = dict((k.lower(), v.lower()) for k,v in us_states.items())

    while res.lower().strip() != "exit":
        res = input('Enter a State Name: (e.g. Michigan or michigan)\n')
        if res.lower().strip() == 'exit':
            break
        while us_states.get(res.lower()) is None:
            print("That is not a state, try entering a state name like `michigan`! (type `exit` to quit)")
            res = input('Enter a State Name: ')
            if res.lower().strip() == 'exit':
                break
        if res.lower().strip() == 'exit':
            break
        print(f"\nListing the National Parks available for ({res})")
        print('-----------------------------------------')
        state_sites = get_sites_for_state(f"https://www.nps.gov/{res.lower()}/index.htm")
        print_national_sites(state_sites)
        print("-----------------------------------------")
        print("Type `back` to return to state selection, `exit` to exit program")
        res = input("\nTo view a site's nearby facilities, enter the number (e.g. 5) that corresponds to it!\n")
        if res.lower().strip() == 'back':
            continue
        if res.lower().strip() == 'exit':
            break
        while res.isnumeric() is False or int(res) > len(state_sites):
            print('\nInvalid input, please enter a number that is within the range of national sites displayed above!')
            print('`back` to return to state selection, `exit` to exit')
            res = input('Enter a number: ')
            if res.lower().strip() == 'back' or res.lower().strip() == 'exit':
                break
        if res.lower().strip() == 'back':
            continue
        if res.lower().strip() == 'exit':
            break

        print(f"Finding nearby places for {state_sites[int(res)-1].name}")
        print('-----------------------------------------')
        nearby_places = get_nearby_places(state_sites[int(res)-1])
        print_nearby_places(nearby_places)
        print('-----------------------------------------')

    print("End of program, bye-bye!")