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
'''
IP Address in the URL

Checks for the presence of IP address in the URL. URLs may have IP address instead of domain name. If an IP address is used as an alternative of the domain name in the URL, we can be sure that someone is trying to steal personal information with this URL.

If the domain part of URL has IP address, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''
def url_having_ip(url):
    try:
        ipaddress.ip_address(url)
        return(-1)
    except:
        return(1)


# Feature 2
'''
Length of URL

Computes the length of the URL. Phishers can use long URL to hide the doubtful part in the address bar. In this project, if the length of the URL is greater than or equal 54 characters then the URL classified as phishing otherwise legitimate.

If the length of URL >= 54 , the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''

def url_length(url):
    length=len(url)
    if(length<54):
        return -1
    elif(54<=length<=75):
        return 0
    else:
        return 1

# Feature 3
'''
Using URL Shortening Services “TinyURL”

URL shortening is a method on the “World Wide Web” in which a URL may be made considerably smaller in length and still lead to the required webpage. This is accomplished by means of an “HTTP Redirect” on a domain name that is short, which links to the webpage that has a long URL. 

If the URL is using Shortening Services, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''
def url_short(url):
    re = regex.compile(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                       r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                       r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                       r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                       r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                       r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                       r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net')
    match = re.search(url)
    if match:
       return -1
    else:
        return 1
 
# Feature 4
'''
"@" Symbol in URL

Checks for the presence of '@' symbol in the URL. Using “@” symbol in the URL leads the browser to ignore everything preceding the “@” symbol and the real address often follows the “@” symbol. 

If the URL has '@' symbol, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''

def having_at_symbol(url):
    symbol=regex.findall(r'@',url)
    if(len(symbol)==0):
        return -1
    else:
        return 1

# Feature 5
'''

Checking the presence of '-' in the domain part of URL. The dash symbol is rarely used in legitimate URLs. Phishers tend to add prefixes or suffixes separated by (-) to the domain name so that users feel that they are dealing with a legitimate webpage. 

If the URL has '-' symbol in the domain part of the URL, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''
def doubleSlash(url):
  list=[x.start(0) for x in regex.finditer('//', url)]
  if list[len(list)-1]>6:
        return(-1)
  else:
        return(1)

# Feature 6
'''

Prefix or Suffix "-" in Domain

Checking the presence of '-' in the domain part of URL. The dash symbol is rarely used in legitimate URLs. Phishers tend to add prefixes or suffixes separated by (-) to the domain name so that users feel that they are dealing with a legitimate webpage. 

If the URL has '-' symbol in the domain part of the URL, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''

def prefix_suffix(url):
    subDomain, domain, suffix = extract(url)
    if(domain.count('-')):
        return 1
    else:
        return -1
    # if '-' in urlparse(url).netloc:
    #     return 1            # phishing
    # else:
    #     return 0            # legitimate



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
'''
Redirection "//" in URL

Checks the presence of "//" in the URL. The existence of “//” within the URL path means that the user will be redirected to another website. The location of the “//” in URL is computed. We find that if the URL starts with “HTTP”, that means the “//” should appear in the sixth position. However, if the URL employs “HTTPS” then the “//” should appear in seventh position.

If the "//" is anywhere in the URL apart from after the protocal, thee value assigned to this feature is 1 (phishing) or else 0 (legitimate).


# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0
'''

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
'''

Checks the effect of mouse over on status bar (Mouse_Over)

Phishers may use JavaScript to show a fake URL in the status bar to users. To extract this feature, we must dig-out the webpage source code, particularly the “onMouseOver” event, and check if it makes any changes on the status bar

If the response is empty or onmouseover is found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''
def on_mouseover(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.text.strip() == "":
                return 1  # Empty response, likely phishing
            else:
                if regex.findall(r"<script>.*?onmouseover.*?</script>", response.text, regex.IGNORECASE):
                    return 1  # Contains onmouseover script, likely phishing
                else:
                    return 0  # No onmouseover script found, likely legitimate
        else:
            return 1  # Non-200 status code, likely phishing
    except Exception as e:
        print("Error:", e)
        return 1  # Error occurred, treat as likely phishing

# Feature 21
'''
Disabling Right Click

Phishers use JavaScript to disable the right-click function, so that users cannot view and save the webpage source code. This feature is treated exactly as “Using onMouseOver to hide the Link”. Nonetheless, for this feature, we will search for event “event.button==2” in the webpage source code and check if the right click is disabled.

If the response is empty or onmouseover is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''

def rightClick(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.text.strip() == "":
                return 1  # Empty response, likely phishing
            else:
                # Check for JavaScript code that disables right-click
                if regex.findall(r"event\.button ?== ?2", response.text):
                    return 1  # Contains right-click disabling code, likely phishing
                else:
                    return 0  # No right-click disabling code found, likely legitimate
        else:
            return 1  # Non-200 status code, likely phishing
    except Exception as e:
        print("Error:", e)
        return 1  # Error occurred, treat as likely phishing


# Feature 23
'''
IFrame is an HTML tag used to display an additional webpage into one that is currently shown. Phishers can make use of the “iframe” tag and make it invisible i.e. without frame borders. In this regard, phishers make use of the “frameBorder” attribute which causes the browser to render a visual delineation. 

If the iframe is empty or repsonse is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
'''
def iframe(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.text.strip() == "":
                return 1  # Empty response, likely phishing
            else:
                if regex.findall(r"<iframe>|<frameBorder>", response.text):
                    return 0  # Contains iframe or frameborder, likely legitimate
                else:
                    return 1  # No iframe or frameborder found, likely phishing
        else:
            return 1  # Non-200 status code, likely phishing
    except Exception as e:
        print("Error:", e)
        return 1  # Error occurred, treat as likely phishing

# Feature 24
'''

Age of Domain

This feature can be extracted from WHOIS database. Most phishing websites live for a short period of time. The minimum age of the legitimate domain is considered to be 12 months for this project. Age here is nothing but different between creation and expiration time.

If age of domain > 12 months, the vlaue of this feature is 1 (phishing) else 0 (legitimate).

'''

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
'''
DNS Record

For phishing websites, either the claimed identity is not recognized by the WHOIS database or no records founded for the hostname. 
If the DNS record is empty or not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).

'''

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
'''
Web Traffic

If high traffic is present at a site it's legitimate, then return -1 or else 0

This feature measures the popularity of the website by determining the number of visitors and the number of pages they visit. However, since phishing websites live for a short period of time, they may not be recognized by the Alexa database (Alexa the Web Information Company., 1996). By reviewing our dataset, we find that in worst scenarios, legitimate websites ranked among the top 100,000. Furthermore, if the domain has no traffic or is not recognized by the Alexa database, it is classified as “Phishing”.

If the rank of the domain < 100000, the value of this feature is 1 (phishing) else 0 (legitimate).

'''
def web_traffic(url):
    #ongoing
   
    try:
    #Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
            "REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1
    if rank <100000:
        return 1
    else:
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
    features['num_special_chars'] = len(regex.findall(special_characters, url))
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
    
# Feature 28
def google_index(url):
    #ongoing
    return 0

# Feature 29
def links_pointing(url):
    #ongoing
    return 0

# Feature 22
def popup(url):
    #ongoing
    return 0

# Feature 10
def favicon(url):
    #ongoing
    return 0


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

print(extract_url_features("https://www.google.com"))

    
    
    

'''
NEW FEATURES:
'''

# 14.End time of domain: The difference between termination time and current time (Domain_End)
# If end period of domain > 6 months, the value of this feature is 1 (phishing) else 0 (legitimate). 

# def domainEnd(domain_name):
#   expiration_date = domain_name.expiration_date
#   if isinstance(expiration_date,str):
#     try:
#       expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
#     except:
#       return 1
#   if (expiration_date is None):
#       return 1
#   elif (type(expiration_date) is list):
#       return 1
#   else:
#     today = datetime.now()
#     end = abs((expiration_date - today).days)
#     if ((end/30) < 6):
#       end = 0
#     else:
#       end = 1
#   return end


'''
Computes the depth of the URL. This feature calculates the number of sub pages in the given url based on the '/'.

The value of feature is a numerical based on the URL.
'''

# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth


'''
Website Forwarding

The fine line that distinguishes phishing websites from legitimate ones is how many times a website has been redirected. In our dataset, we find that legitimate websites have been redirected one time max. On the other hand, phishing websites containing this feature have been redirected at least 4 times.

'''

# 18.Checks the number of forwardings (Web_Forwards)    
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1
