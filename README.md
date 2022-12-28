# browser-profile-cookies #

* ***What does it do?*** Retrieves decrypted cookies from your browser.
* ***Which browsers are supported?*** Known Chromium-based browsers.

## Install ##
```bash
pip3 install browser-profile-cookies
```

## Usage ##

```python
from profile_cookies import Profile

Profile.available_browsers() # -> static method, a dict of all local Chromium browser names and paths

profile = Profile() # defaults to the Default profile for Edge Browser

# if Edge isn't installed, profile can be created for any locally installed Chromium-based browser
profile = Profile(browser="chrome")

profile.browser = "vivaldi" # the browser can be reassigned with cascading changes
profile.available_profiles() # -> dict of all browser profiles and paths

profile.profile = "profile 1" # profile can be reassigned with cascading changes
profile.cookiejar() # -> http.cookiejar.Cookiejar of all stored cookies for 'Profile 1'

domain = "msn"
profile.cookie(domain) # -> http.cookiejar.Cookiejar for the requested domain and profile

domain = "msn.com"
profile.cookiestring(domain) # -> string formatted cookies for the requested domain and profile
```
Retrieved cookies can be used when making requests via urllib or through a package like requests.
