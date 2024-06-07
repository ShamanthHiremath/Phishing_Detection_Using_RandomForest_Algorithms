# -*- coding: utf-8 -*-

'''
1) Complete undone function definitions
2) Remove all unnecessary email related functions

return -1 #legitimate
return 0 #suspicious
return 1 #phishing

'''

import regex
from tldextract import extract
import ssl
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib.request
import whois
import datetime
import ipaddress
import dns.resolver

# Feature 1
# URL having IP address
def url_having_ip(url):
    try:
        ipaddress.ip_address(url)
        return(-1)
    except:
        return(1)

# Feature 2
# URL length
def url_length(url):
    length=len(url)
    if(length<54):
        return -1
    elif(54<=length<=75):
        return 0
    else:
        return 1

# Feature 3
#  URL shortening service
def url_short(url):
    match=regex.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
    if match:
       return(-1)
    else:
        return(1)

# Feature 4
def having_at_symbol(url):
    symbol=regex.findall(r'@',url)
    if(len(symbol)==0):
        return -1
    else:
        return 1

# Feature 5
def doubleSlash(url):
  list=[x.start(0) for x in regex.finditer('//', url)]
  if list[len(list)-1]>6:
        return(-1)
  else:
        return(1)

# Feature 6
def prefix_suffix(url):
    subDomain, domain, suffix = extract(url)
    if(domain.count('-')):
        return 1
    else:
        return -1

# Feature 7
def sub_domain(url):
    subDomain, domain, suffix = extract(url)
    if(subDomain.count('.')==0):
        return -1
    elif(subDomain.count('.')==1):
        return 0
    else:
        return 1

# Feature 8
def SSLfinal_State(url):
    try:
#check wheather contains https
        if(regex.search('^https',url)):
            usehttps = 1
        else:
            usehttps = 0
#getting the certificate issuer to later compare with trusted issuer
        #getting host name
        subDomain, domain, suffix = extract(url)
        host_name = domain + "." + suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(), server_hostname = host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['commonName'])
        certificate_Auth = certificate_Auth.split()
        if(certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
            certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
        else:
            certificate_Auth = certificate_Auth[0]
        trusted_Auth = ['Comodo','Symantec','GoDaddy','GlobalSign','DigiCert','StartCom','Entrust','Verizon','Trustwave','Unizeto','Buypass','QuoVadis','Deutsche Telekom','Network Solutions','SwissSign','IdenTrust','Secom','TWCA','GeoTrust','Thawte','Doster','VeriSign']
#getting age of certificate
        startingDate = str(certificate['notBefore'])
        endingDate = str(certificate['notAfter'])
        startingYear = int(startingDate.split()[3])
        endingYear = int(endingDate.split()[3])
        Age_of_certificate = endingYear-startingYear

#checking final conditions
        if((usehttps==1) and (certificate_Auth in trusted_Auth) and (Age_of_certificate>=1) ):
            return -1 #legitimate
        elif((usehttps==1) and (certificate_Auth not in trusted_Auth)):
            return 0 #suspicious
        else:
            return 1 #phishing

    except Exception as e:

        return 1

# Feature 9
def domain_registration(url):
    try:
        w = whois.whois(url)
        updated = w.updated_date
        exp = w.expiration_date
        length = (exp[0]-updated[0]).days
        if(length<=365):
            return 1
        else:
            return -1
    except:
        return 0

# Feature 10
def favicon(url):
    #ongoing
    return 0

# Feature 11
def port(url):
    domain = regex.findall(r"://([^/]+)/?", url)[0]
    if regex.match(r"^www.",domain):
        domain = domain.replace("www.","")
    try:
        port = domain.split(":")[1]
        if port:
                return(-1)
        else:
                return(1)
    except:
          return(1)

# Feature 12
def https_token(url):
    subDomain, domain, suffix = extract(url)
    host =subDomain +'.' + domain + '.' + suffix
    if(host.count('https')): #attacker can trick by putting https in domain part
        return 1
    else:
        return -1

# Feature 13
def request_url(url):
    try:
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain

        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        imgs = soup.findAll('img', src=True)
        total = len(imgs)

        linked_to_same = 0
        avg =0
        for image in imgs:
            subDomain, domain, suffix = extract(image['src'])
            imageDomain = domain
            if(websiteDomain==imageDomain or imageDomain==''):
                linked_to_same = linked_to_same + 1
        vids = soup.findAll('video', src=True)
        total = total + len(vids)

        for video in vids:
            subDomain, domain, suffix = extract(video['src'])
            vidDomain = domain
            if(websiteDomain==vidDomain or vidDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total

        if(avg<0.22):
            return -1
        elif(0.22<=avg<=0.61):
            return 0
        else:
            return 1
    except:
        return 0

# Feature 14
def url_of_anchor(url):
    try:
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain

        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        anchors = soup.findAll('a', href=True)
        total = len(anchors)
        linked_to_same = 0
        avg = 0
        for anchor in anchors:
            subDomain, domain, suffix = extract(anchor['href'])
            anchorDomain = domain
            if(websiteDomain==anchorDomain or anchorDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total

        if(avg<0.31):
            return -1
        elif(0.31<=avg<=0.67):
            return 0
        else:
            return 1
    except:
        return 0
    
# Feature 15
def Links_in_tags(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')

        no_of_meta =0
        no_of_link =0
        no_of_script =0
        anchors=0
        avg =0
        for meta in soup.find_all('meta'):
            no_of_meta = no_of_meta+1
        for link in soup.find_all('link'):
            no_of_link = no_of_link +1
        for script in soup.find_all('script'):
            no_of_script = no_of_script+1
        for anchor in soup.find_all('a'):
            anchors = anchors+1
        total = no_of_meta + no_of_link + no_of_script+anchors
        tags = no_of_meta + no_of_link + no_of_script
        if(total!=0):
            avg = tags/total

        if(avg<0.25):
            return -1
        elif(0.25<=avg<=0.81):
            return 0
        else:
            return 1
    except:
        return 0

# Feature 16
def sfh(url):
    # fetch HTML content of a URL
    response = requests.get(url)
    response.raise_for_status() # Ensure we notice bad responses
    html = response.text
    
    # Extract the form action URL and its domain
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form')
    # Not phishy if no form is found in the HTML
    if not form:
        print("No form found in the HTML")
        return -1
    
    action = form.get('action')
    if not action:
        print("No action attribute found in the form")
        return -1
    
    # Join the action URL with the base URL if it's a relative URL
    full_url = urljoin(url, action)
    action_domain = urlparse(full_url).netloc
    if action_domain:
        url_domain = urlparse(url).netloc # Extract domain from the URL
        # If the form data is submitted to the same domain, it's not phishy
        if(url_domain == action_domain):
            return -1
        print(f"Form data is submitted to domain: {action_domain}")
        x1 = url_having_ip(url) # -1 if IP address is present in URL, 1 otherwise
        x2 = domain_registration(url) # -1 if domain is registered for more than a year, 1 otherwise
        x3 = https_token(url) # -1 if https is not present in URL, 1 otherwise
        x4 = SSLfinal_State(url) # -1 if certificate is valid and trusted, 1 otherwise
        

# Feature 17
def email_submit(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        if(soup.find('mailto:')):
            return 1
        else:
            return -1
    except:
        return 0

# Feature 18
def abnormal_url(url):
    #ongoing
    return 0

# Feature 19
import requests

def url_length(url):
    # Example logic: consider URLs longer than 100 characters as suspicious
    return len(url) > 100

def SSLfinal_State(url):
    try:
        response = requests.get(url, timeout=10)
        # Check if the URL uses HTTPS
        return url.startswith("https")
    except requests.RequestException as e:
        print(f"An error occurred when checking SSL state: {e}")
        return False

def redirect(url):
    try:
        # Send a GET request
        response = requests.get(url, allow_redirects=True)
        
        # Check if the URL was redirected
        if response.history:
            print("Redirection history:")
            for resp in response.history:
                # print(f" - {resp.status_code} {resp.url}")
                # Check for specific redirection status codes
                if resp.status_code in [301, 302, 303, 307, 308]:
                    return 1
                
            # Final URL after all redirections
            final_url = response.url
            if url_length(final_url) or SSLfinal_State(final_url):
                return 1
        else:
            print(f"The URL '{url}' was not redirected.")
            return -1
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return -1
    
# Feature 20
def on_mouseover(url):
    #ongoing
    return 0

# Feature 21
def rightClick(url):
    #ongoing
    return 0

# Feature 22
def popup(url):
    #ongoing
    return 0

# Feature 23
def iframe(url):
    #ongoing
    return 0

# Feature 24
def age_of_domain(url):
    try:
        w = whois.whois(url)
        start_date = w.creation_date
        current_date = datetime.datetime.now()
        age =(current_date-start_date[0]).days
        if(age>=180):
            return -1
        else:
            return 1
    except Exception as e:
        #print(e)
        return 0

# Feature 25
def dns(domain):
    # List of common DNSBL services
    dnsbl_services = [
        "zen.spamhaus.org",
        "bl.spamcop.net",
        "dnsbl.sorbs.net",
        "b.barracudacentral.org",
        "cbl.abuseat.org"
    ]
    
    # Get the IP address of the domain
    try:
        answers = dns.resolver.resolve(domain, 'A')
        ip_address = answers[0].to_text()
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        print(f"Unable to resolve domain: {domain}")
        return -1

    # Reverse the IP address for DNSBL query
    reversed_ip = '.'.join(reversed(ip_address.split('.')))
    
    # Check the IP address against each DNSBL service
    for service in dnsbl_services:
        query = f"{reversed_ip}.{service}"
        try:
            response = dns.resolver.resolve(query, 'A')
            if response:
                # Domain is blacklisted by {service}
                return 1
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            # The IP address is not listed in this DNSBL
            continue

    # Domain is not blacklisted
    return 0

# Feature 26
def web_traffic(url):
    #ongoing
    # If high traffic is present at a site it's legitimate, then return -1 or else 0
    return 0

# Feature 27
def page_rank(url):
    #ongoing
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    query = url.replace(' ', '+')
    google_search_url = f"https://www.google.com/search?q={query}&num=100"

    try:
        response = requests.get(google_search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.find_all('div', class_='g')

            for i, result in enumerate(search_results):
                link = result.find('a', href=True)
                if link and url in link['href']:
                    return -1

            return 1  # URL not found in top results
        else:
            print(f"Failed to retrieve search results: {response.status_code}")
            return 0
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return 0

# Feature 28
def google_index(url):
    #ongoing
    return 0

# Feature 29
def links_pointing(url):
    #ongoing
    return 0

# Feature 30
def statistical(url):
    
    features = {}
    # Length of URL
    features['url_length'] = len(url)
    # Number of dots
    features['num_dots'] = url.count('.')
    # Number of hyphens
    features['num_hyphens'] = url.count('-')
    # Number of digits
    features['num_digits'] = sum(c.isdigit() for c in url)
    # Number of special characters
    special_characters = r'[@&%=?]'
    features['num_special_chars'] = len(re.findall(special_characters, url))
    # Determine if URL is phishy, not phishy, or suspicious
    if (features['url_length'] > 54 or features['num_dots'] > 5 or
        features['num_hyphens'] > 3 or features['num_digits'] > 10 or
        features['num_special_chars'] > 5):
        return 1  # Phishy
    elif (features['url_length'] < 25 and features['num_dots'] < 3 and
          features['num_hyphens'] < 2 and features['num_digits'] < 5 and
          features['num_special_chars'] < 2):
        return -1  # Not phishy
    else:
        return 0  # Suspicious


# Takes URL as input and returns the features as a list
def extract_url_features(url):
    # Converts the given URL into standard format
    if not regex.match(r"^https?", url):
        url = "http://" + url


    url_features = [[url_having_ip(url),url_length(url),url_short(url),having_at_symbol(url),
             doubleSlash(url),prefix_suffix(url),sub_domain(url),SSLfinal_State(url),
              domain_registration(url),favicon(url),port(url),https_token(url),request_url(url),
              url_of_anchor(url),Links_in_tags(url),sfh(url),email_submit(url),abnormal_url(url),
              redirect(url),on_mouseover(url),rightClick(url),popup(url),iframe(url),
              age_of_domain(url),dns(url),web_traffic(url),page_rank(url),google_index(url),
              links_pointing(url),statistical(url)]]


    print(url_features)
    return url_features
