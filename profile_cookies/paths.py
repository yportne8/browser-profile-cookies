import os
from pathlib import Path


class BrowserDoesNotExist(Exception):
    pass


class Failed2FindLocalState(Exception):
    pass


class Failed2FindUserData(Exception):
    pass


class Failed2FindCookies(Exception):
    pass


class BrowserPathNotAssigned(Exception):
    pass


class Failed2FindProfile(Exception):
    pass


class Browsers:
    """
    _chromium browser paths_
    """

    def __init__(self):
        self.chromium = [
            "Edge", "Edge Beta", "Edge Dev", "Edge Canary",
            "Vivaldi", "Opera", "Opera Next", "Opera Developer",
            "Chrome", "Chrome Beta", "Chrome Dev", "Chrome Canary",
            "Chromium", "Chromium Beta", "Chromium Dev",
            "Chromium Canary", "Brave-Browser", "Brave-Browser-Beta",
            "Brave-Browser-Nightly"]

    @property
    def browsers(self) -> dict:
        browsers = {}
        for path in Path(os.environ["LOCALAPPDATA"]).resolve().glob('**/'):
            for name in self.chromium:
                if path.name == name:
                    browsers[name] = str(path)
        return browsers


class Browser(Browsers):
    """
    _browser paths_
    """

    def __init__(self, browser: str):
        super().__init__()
        self.browser = browser
        
    @property
    def browser(self):
        return self._browser

    @browser.setter
    def browser(self, value):
        name = value.title()
        if not self.browsers.get(name):
            print(self.browsers)
            raise BrowserDoesNotExist
        # [NOTE] Browser path set here.
        setattr(self, "path", Path(self.browsers.get(name)))
        self._browser = name        

    @property
    def userdata(self) -> Path:
        name = "User Data"
        try:
            searchDir = self.path # exception if not assigned.
            for path in Path(searchDir).resolve().glob('**/'):
                if path.name == name:
                    return path
            raise Failed2FindUserData
        except Exception as e:
            if e != Failed2FindUserData:
                raise BrowserPathNotAssigned

    @property
    def localstate(self) -> Path:
        name = "Local State"
        for path in Path(self.userdata).resolve().glob('**/*'):
            if name == path.name:
                return path
        raise Failed2FindLocalState
        
    @property
    def profiles(self) -> dict:
        profiles = {}
        for path in Path(self.userdata).resolve().glob('**/'):
            for name in ["Default", "Profile"]:
                if name in path.name:
                    profiles[path.name] = path
        return profiles


class Profile(Browser):
    """
    _profile and cookies paths_
    """

    def __init__(self, browser: str, profile: str):
        super().__init__(browser)
        self.profile = profile
        self.cookies = Path(os.environ["TEMP"], "Cookies")

    def __del__(self):
        try:
            self.cookies.unlink()
        except:
            pass

    @property
    def profile(self):
        return self._profile
    
    @profile.setter
    def profile(self, value):
        name = value.title()
        if not self.profiles.get(name):
            print(self.profiles)
            raise Failed2FindProfile
        
        self._profile = self.profiles.get(name)
        print(f"Profile: {name} found.")

    @property
    def cookies(self):
        return self._cookies
        # [NOTE] Adjustment for a recent change to chromium, moving the
        # Cookies file (sqlite db/text file) into the Network directoryvwithin the 
        # 'User Data\User' folder. Backward compatible if the file is in its
        # original location.

    @cookies.setter
    def cookies(self, value):
        path = Path(self.profile, "Cookies")
        if not path.exists():
            path = Path(self.profile, "Network", "Cookies")
            if not path.exists():
                raise Failed2FindCookies
                
        with open(value, "wb+") as f:
            with open(path, "rb") as data:
                f.write(data.read())
        
        self._cookies = value