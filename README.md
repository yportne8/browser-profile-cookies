🍪 # browser-profile-cookies #  🍪

* ***What does it do?*** Retrieves decrypted cookies from your browser.
* ***Which browsers are supported?*** Known Chromium-based browsers.

## Install ##
```bash
pip3 install browser-profile-cookies
```

## Usage ##

```python
from profile_cookies import Profile

# -> static method, a dict of all local Chromium browser names and paths
Profile.available_browsers() 

# defaults to the 'Default' profile for 'Edge' browser
profile = Profile() 

# if Edge isn't installed, profile can be initialized any locally installed Chromium-based browser
profile = Profile(browser="chrome")

# the browser can be reassigned with cascading changes
profile.browser = "vivaldi" 
profile.available_profiles() # -> dict of all browser profiles and paths

# profile can be reassigned with cascading changes
profile.profile = "profile 1" 
profile.cookiejar() # -> http.cookiejar.Cookiejar of all stored cookies for 'Profile 1'

# -> http.cookiejar.Cookiejar for the requested domain and profile
domain = "msn"
profile.cookie(domain)

# -> string formatted cookies for the requested domain and profile
domain = "msn.com"
profile.cookiestring(domain) 
```
Retrieved cookies can be used when making requests via urllib or through a package like requests.
