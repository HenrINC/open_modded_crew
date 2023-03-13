import subprocess
import logging
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import atexit
import os
from typing import Literal, Union, Callable, Any, Optional
import requests
import json
import platform
import threading
import tkinter
from debug_server import DebugServer, start_debug_server

logging.getLogger().setLevel(logging.INFO)

def split_big_text(text, max_len):
    DECORATORS_LEN = 8
    for i in []:
        text = text.replace(i, "")
    if len(text) > max_len:
        part_count = 1+len(text)//(max_len-DECORATORS_LEN)
        parts = [f"({i+1}/{part_count})"+text[(max_len-DECORATORS_LEN)*i:(1+i)*(max_len-DECORATORS_LEN)]+"..." for i in range(part_count)]
        parts[-1] = parts[-1][:-3]
        return parts
    else:
        return [text]

def fix_style_proprety_value(text:str):
    for i, j in {
        #Crew ranks
        "&gt;": ">", 
        "&lt;": "<",

        #Crew motto
        "&#166;" : "¦",

        #Command
        "[rv]": "¦", #R* verified
        "[rc]": "<", #R* created
        "[bw]": ">", #Blank Space
        "[r1]": "÷", #R* 1
        "[r2]": "∑", #R* 2
        "[lk]": "Ω", #Lock
        "[ws]": "~ws~", #Wanted star
        "[r]": "~r~", #Red
        "[g]": "~g~", #Green
        "[y]": "~y~", #Yellow
        "[p]": "~p~", #Purple
        "[o]": "~o~", #Orange
        "[b]": "~b~", #Blue
        "[d]": "~d~", #Dark blue
        "[f]": "~f~", #Light blue
        "[s]": "~s~", #White (default)
        "[m]": "~m~", #Dark gray
        "[c]": "~c~", #Grey
        "[t]": "~t~", #Grey
        "[u]": "~u~", #Black
        "[l]": "~l~", #Black
        "[v]": "~v~", #Black
        "[n]": "~n~", #Skip line
        "[italic]": "~italic~", #Italic
        "[bold]" : "~bold~", #Bold
    
    }.items():
        text = text.replace(i, j)
    return text

##Code from WF2 (the lib i used to make twitter bots)
def go_as_blind_where(driver, fun, timeout = 30):
    end = time.time()+timeout
    while True:
        focus = driver.execute_script('return document.activeElement')
        try:
            if fun(focus):
                return focus
        except: pass
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        if end < time.time():
            raise TimeoutError("Can't go there in time")

def compleate_fields(driver,fields, timeout = 30):

    """
Fields is a dict {css_selector:keys}
"""

    for i in fields:
        target = ""
        for ii in range(timeout):
            try:
                target = driver.find_element(By.CSS_SELECTOR, i)
                break
            except:
                time.sleep(1)
                timeout -= 1
        if target == "":
            raise TimeoutError("Can't go there in time")
        go_as_blind_where(driver,lambda focus: focus == target,timeout)
        webdriver.ActionChains(driver).send_keys(fields[i]).perform()

def get_json_or_default(filename, default={}):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    else:
        return default

#JMP:CONNECTOR
class Connector():
    def __init__(self):
        self.cookies:str = ""
        self.verif_token:str = ""
        self.debug:bool = True
        self.running:bool = True
        self.proxy_thread:Optional[threading.Thread] = None
        self.proxy_process:Optional[subprocess.Popen] = None
        self.fresh_cookies_thread:Optional[threading.Thread] = None
        self.player:Optional[Player] = None
        self.driver:Optional[webdriver.Chrome] = None
        self.debug_thread:Optional[threading.Thread] = None
        self.debug_server_thread:Optional[threading.Thread] = None
        
        atexit.register(self.stop)

    def proxy_thread_target(self):
        system = platform.system().lower()
        bin_map:dict[str,str] = {
            "windows": "mitmdump.exe",
            "linux": "mitmdump"
        }
        while self.running:
            if self.proxy_process is not None:
                self.proxy_process.wait()    
            self.proxy_process = subprocess.Popen(
                [f"./{bin_map[system]}", "-q", "-s",  "./mitm_addon.py"],
                cwd=os.getcwd()
            )
        
    def ensure_framebuffer(self):
        """
        This programm is intended to be used on headless servers but:
         - the socialclub website does not work with headless chrome
        so we need to install something like xvfb
        this method will ensure that chromium can outpout it's display
        on a framebuffer
        """
        
        #This can seem a bit junky but tk ships whith python so no more requirements
        try:
            test_gui_app = tkinter.Tk()
            test_gui_app.withdraw()
            screen_size = test_gui_app.winfo_screenwidth()*test_gui_app.winfo_screenheight()
            has_framebuffer = screen_size > 0

        except:
            has_framebuffer = False
        
        if not has_framebuffer:
            system = platform.system().lower()
            if system == "linux":
                try:
                    from xvfbwrapper import Xvfb
                except ImportError:
                    raise ImportError("You are running open modded crew on a headless server,\
                                        you need to install the Xvfb wrapper 'pip install xvfbwrapper'")
                self.vdisplay = Xvfb()
                self.vdisplay.start()

            else:
                raise NotImplementedError("Can only start virtual frame buffer on linux")
    
    def stop(self):
        self.running = False
        if self.proxy_process is not None:
            self.proxy_process.kill()
        if self.proxy_thread is not None:
            self.proxy_thread.join()
        if self.fresh_cookies_thread is not None:
            self.fresh_cookies_thread.join()
        if self.driver is not None:
            self.driver.quit()
        if self.debug_thread is not None:
            self.debug_thread.join()
        if self.debug_server_thread is not None:
            self.debug_server_thread.join()
        if self.vdisplay is not None:
            self.vdisplay.stop()
    
    def debug_thread_target(self):
        logging.info(f"Running status {self.running}")
        while self.running:
            logging.info("Updating screenshot")
            DebugServer.last_screenshot = self.driver.get_screenshot_as_png()

    def login(self, email:str, password:str):
        chromedriver_autoinstaller.install()
        self.proxy_thread = threading.Thread(target=self.proxy_thread_target)
        self.proxy_thread.start()
        logging.info("Waiting for proxy to start")
        ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                ping_socket.connect(("127.0.0.1", 8080))
                break
            except Exception as e:
                pass
        logging.info("Started")
        opts = Options()
        opts.add_argument("--proxy-server=http://127.0.0.1:8080")
        opts.add_argument("--no-sandbox")
        #opts.headless = True #does not work in headless
        self.ensure_framebuffer()
        self.driver = webdriver.Chrome(options=opts)
        if self.debug:
            self.debug_server_thread = threading.Thread(target=start_debug_server, kwargs={"port": 8081})
            self.debug_server_thread.start()
            self.debug_thread = threading.Thread(target=self.debug_thread_target)
            self.debug_thread.start()
            
        self.driver.get("https://socialclub.rockstargames.com/profile/signin")
        compleate_fields(self.driver,{
            "form [type=email]": email,
            "form [type=password]": password,
            "form [type=submit]": Keys.ENTER
            })
        for i in range(2):
            for j in range(50):
                if self.driver.current_url == "https://socialclub.rockstargames.com/":
                    time.sleep(3)
                    with open("verif_token.txt", "r") as file:
                        self.verif_token = file.read()
                    self.update_cookies()
                    self.keep_cookies_fresh()
                    self.driver.minimize_window()
                    return True
                time.sleep(0.1)
            logging.warning("The anti-bot protection has been triggered")
            input("PLASE COMPLEATE CAPTCHA")

        return False

    def update_cookies_api(self):
        """
        Will replace the need for a selenium webdriver
        Does not work
        TODO make it work
        """
        headers = {
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8",
            "x-requested-with": "XMLHttpRequest",
            "cookie": self.cookies
        }
        response = requests.post(
            "https://socialclub.rockstargames.com/connect/refreshaccess",
            headers = headers
        )
        response

    def export_driver_cookies(self):
        return ";".join([f"{cookie['name']}={cookie['value']}"for cookie in self.driver.get_cookies()])
    
    def update_cookies(self):
        self.cookies = self.export_driver_cookies()
    
    def refresh_cookies(self):
        self.driver.refresh()
        time.sleep(5)
        self.update_cookies()

    def keep_cookies_fresh(self):
        self.fresh_cookies_thread = threading.Thread(target=self.fresh_cookies_thread_target)
        self.fresh_cookies_thread.start()

    def fresh_cookies_thread_target(self):
        while self.running:
            time.sleep(50)
            self.refresh_cookies()

    
    def api_request(
            self,
            func:Callable[[Any],requests.Response],
            url:str,
            data = False,
            headers = {}
        ) -> requests.Response:
        """
sends a request to the api
it has a bunch of robustness
"""
        last_code = 0
        for i in range(3):
            try:
                print(f"Requesting {url}")
                if data:
                    response:requests.Response = func(url, headers = headers, data = data)
                else:
                    response:requests.Response = func(url, headers = headers)
                print(f"Response [{response.status_code}] {url}")

                if "json" in response.headers["content-type"].lower():
                    content = response.json()
                    if response.status_code in [200, 500]:
                        #Sometimes an error returns code 200, sometimes it's 500, the body can spot the diference tho
                        if "Error" in content:
                            logging.warning(f"API ERROR : [{content['Error']['_msg']}] Attempting to fix...")
                        elif "error" in content: #The other type of error you'll probably never see
                            logging.warning(f"API ERROR : [{content['error']['errorMessage']}] Attempting to fix...")
                        else:
                            logging.debug("SUCCESS")
                            return response
                        #proxy_obj.disabled_until = int(time.time())+5
                        time.sleep(5) #Sleep if error #Waiting is now handled by the proxy chooser

                    elif response.status_code == 429:
                        if last_code == 429:
                            logging.warning("Got a 429 twice, waiting won't solve it, returning response")
                            return response
                        logging.warning("Too many requests, attempting to fix...")
                        time.sleep(60)
                    elif response.status_code == 401:
                        logging.warning("Unauthorized request, attempting to fix...")
                        self.refresh_cookies()

                    last_code = response.status_code

                else:
                    logging.warning(f"The API returnd a non JSON response with code [{response.status_code}], it's an issue we can't solve")
                    logging.debug("The progarmm will wait 5 seconds to avoid the next response to be glitched too")
                    time.sleep(5)
                    return response
            except:
                logging.exception("An unexpected error occured, waiting might solve it")
                time.sleep(5)

        logging.error("Couldn't solve the issue, here is the response")
        return response

    def request(
            self,
            func,
            url,
            data:Union[dict, bool] = False,
            auth_type:Union[Literal["cookie", "bearer"], None] = None,
        ) -> requests.Response:
        if auth_type == "cookie":
            headers = {
                "cookie": self.cookies,
                "__RequestVerificationToken" : self.verif_token,
                "Content-Type": "application/json"
            }
        elif auth_type == "bearer":
            bearer = self.cookies.split("BearerToken=")[1].split(";")[0]
            headers = {
                "Authorization":"Bearer "+bearer,
                "X-Requested-With": "XMLHttpRequest"
            }
        elif auth_type == None:
            headers = {
                "Authorization":None,
                "X-Requested-With": "XMLHttpRequest"
            }
        else:
            raise ValueError("Invalid auth_type")
        return self.api_request(func, url, data, headers)

    def doc_api(self, func, url) -> requests.Response:
        headers = {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
             'Connection': 'keep-alive',
             'Cookie': self.cookies,
             'Host': 'socialclub.rockstargames.com',
             'Referer': 'https://socialclub.rockstargames.com/',
             'Sec-Fetch-Dest': 'document',
             'Sec-Fetch-Mode': 'navigate',
             'Sec-Fetch-Site': 'same-origin',
             'Sec-Fetch-User': '?1',
             'Upgrade-Insecure-Requests': '1',
             #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
             #'sec-ch-ua': '"Opera GX";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
             'sec-ch-ua-mobile': '?0',
             'sec-ch-ua-platform': '"Windows"'}
        for i in range(3):
            response = func(url, headers = headers)
            if response.status_code == 200:
                return response
            else:
                logging.error(f"Got an error code [{response.status_code}], waiting 300 seconds")
                time.sleep(300)
        return response

    #TODO find a better place for those methods

    def like_post(self, post_id, set_liked = True):
        URL = "https://scapi.rockstargames.com/feed/likes"
        payload = {
            "postId" : post_id,
            "setLiked" : set_liked
            }
        self.request(requests.post, URL, payload, auth_type="Bearer")
    
    def get_self_player(self) -> "Player":
        if self.player is None:
            URL = "https://scapi.rockstargames.com/profile/getbasicprofile"
            info = self.request(requests.get, URL, auth_type="bearer").json()["accounts"][0]["rockstarAccount"]
            self.player = Player(info["rockstarId"], **info)
        return self.player

    def comment_post(self, post_id, comment: Union[str, list[str]]):
        URL = "https://scapi.rockstargames.com/feed/comments"
        
        if not isinstance(comment, list):
            comment = split_big_text(comment, 140)
            
        for i in comment:
            payload = {
                "message": i,
                "postId": post_id
                }
            
            self.request(requests.post, URL, payload, auth_type="bearer")

#JMP:CREW
class CrewSingleton(type):
    _instances:dict = {}
    def __call__(cls, *args, **kargs):
        if "name" in kargs:    
            name = kargs['name'] 
            #del kargs["name"]
        else:
            name = cls.__name__

        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kargs)
        
        return cls._instances[name]


class Crew(metaclass=CrewSingleton):
    def __init__(self, name:str, connector):
        self.services = {
            "hooked":{},
            "free":[]
        }
        self.service_config = {}
        self.commands = []
        self.command_config = {}
        self.name = name
        self.connector = connector
        response = self.connector.request(
            requests.get,
            f"https://scapi.rockstargames.com/crew/byname?name={self.name}",
        ).json()
        self.id = response["crewId"]
        self.name = response["crewName"]
        self.motto = response["crewMotto"]
        self.member_count = response["memberCount"]
        self.tag = response["crewTag"]
        self.color = response["crewColour"]
        self.open = response["isOpen"]
        self.members:list[CrewMember]
        self.update_members()
        self.style = False
    
    def add_hooked_service(self, hook, service):
        if hook not in self.services["hooked"]:
            self.services["hooked"][hook] = []
        if service not in self.services["hooked"][hook]:
            self.services["hooked"][hook].append(service)

    def save_config(self):
        with open(f"services/{self.name}.json", "w") as file:
            json.dump(self.service_config, file, indent=1)
        with open(f"commands/{self.name}.json", "w") as file:
            json.dump(self.command_config, file, indent=1)
    
    def load_config(self):
        self.service_config = get_json_or_default(
            f"services/{self.name}.json",
            {
                "hooked": {
                    "posts": [
                        "command_service"
                    ],
                    "style": {
                        
                    }
                },
                "free": [
                    "hook_service"
                ]
            }
        )
        self.command_config = get_json_or_default(
            f"commands/{self.name}.json",
            {
                "service": {"min_rank": 0},
                "command": {"min_rank":0}
            }
            
        )
    
    def __repr__(self):
        return f'<Crew "{self.name}">'
    
    def update_members(self):
        members = []
        for i in range(4):
            response = self.connector.request(
                requests.get,
                f"https://scapi.rockstargames.com/crew/rankMembership?crewId={self.id}&rankOrder={i}&onlineService=sc&searchTerm=&pageIndex=0&pageSize={1000}",
                auth_type=None
            ).json()
            rank_members = response["rankMembers"]
            for rank_member in rank_members:
                member = CrewMember(
                    name=rank_member["nickname"],
                    id=rank_member["rockstarId"],
                    connector=self.connector
                )
                member.add_crew(
                    crew=self,
                    crew_rank=i,
                )
                members.append(member)
        self.members = members

    def set_style(self, style):
        URL = "https://socialclub.rockstargames.com/crewsapi/EditCrew"
        payload = json.dumps(style)
        response = self.connector.request(requests.post, URL, payload.encode(), auth_type="cookie")
        return response

    def update_style(self):
        url = f"https://socialclub.rockstargames.com/crew/{self.name}/manage/edit"
        response = self.connector.doc_api(requests.get, url)
        doc = response.text
        doc = doc.split("crews:")[1].split("\n")[0]
        doc = doc.rsplit("]", 1)[0]+"]" #For some reason only known by god himself, strip(",") does not remove the "," at the end, this fixes the issue
        crews = json.loads(doc)
        for i in crews:
            if i["CrewId"] == self.id:
                payload = {
                    "loadData": False,
                    "crewType": None,
                    "recruitmentStatus": "open" if i["IsOpen"] else "invite",
                    "crewColor": i["CrewColour"]
                }
                
                for key in [
                        'crewName', 'crewMotto',
                        'RankTitle1', 'RankTitle2', 'RankTitle3',
                        'RankTitle4', 'RankTitle5', 'RankTitle6',
                        'RankTitle7', 'RankTitle8', 'RankTitle9',
                        'RankTitle10', 'crewAnimation']:
                    payload[key] = fix_style_proprety_value(i[key[0].upper()+key[1:]])
                self.style = payload
                break
    

    
    def get_style(self):
        if not self.style:
            self.update_style()
        return self.style

    def get_wall_posts(self, limit = 100):
        url = f"https://scapi.rockstargames.com/feed/crew?crewId={self.id}&offset=0&limit={limit}&title=&platform=&group=all"
        response = self.connector.request(requests.get, url, auth_type="bearer")
        return response.json()["activities"]

    def get_services_list(self) -> list:
        """Puts all the services in a list for iteration"""
        services = self.services["free"]
        for hook in self.services["hooked"]:
            services.extend(self.services["hooked"][hook])
        return services
    
    def import_service_from_name(self, name):
        module = __import__(f"services.{name}") 
        file = getattr(module, name)
        return file.Service

    def add_service(self, service_name, hook=None):
        service = self.import_service_from_name(service_name)(self, self.connector, service_name)
        if hook is None:
            self.services["free"].append(service)
        else:
            self.add_hooked_service(hook, service)
        service.start()
        
    
    def relaod_services(self):
        for service in self.get_services_list():
            service.stop()
        self.services = {
            "hooked":{},
            "free":[]
        }
        for service_name in self.service_config["free"]:
            self.add_service(service_name)
        for hook in self.service_config["hooked"]:
            for service_name in self.service_config["hooked"][hook]:
                self.add_service(service_name, hook)
    
    def add_service_to_cfg(self, service_name, hook=None):
        if service_name not in [i.rsplit(".py", 1)[0] for i in os.listdir("services")]:
            raise ValueError(f"\"{service_name}\" is not in the services directory")
        if hook is None:
            srvc_list:list = self.service_config["free"]
        else:
            srvc_list:list = self.service_config["hooked"][hook]
        srvc_list.append(service_name)
        self.save_config()
    
    def remove_service_from_cfg(self, service_name, hook=None):
        if hook is None:
            srvc_list:list = self.service_config["free"]
        else:
            srvc_list:list = self.service_config["hooked"][hook]
        srvc_list.remove(service_name)
        self.save_config()
    
    def get_service_from_name(self, service_name, hook=None):
        if hook is None:
            for service in self.services["free"]:
                if service.name == service_name:
                    return service
        else:
            for service in self.services["hooked"][hook]:
                if service.name == service_name:
                    return service

    def import_command_from_name(self, name):
        module = __import__(f"commands.{name}") 
        file = getattr(module, name)
        return file.Command

    def add_command(self, command_name, min_rank):
        command = self.import_command_from_name(command_name)(self, self.connector, command_name, min_rank)
        self.commands.append(command)
    
    def reload_commands(self):
        self.commands = []
        for command_name, cfg in self.command_config.items():
            min_rank = cfg["min_rank"]
            self.add_command(command_name, min_rank)
        
    
    def add_command_to_cfg(self, command_name, min_rank):
        if command_name not in [i.rsplit(".py", 1)[0] for i in os.listdir("commands")]:
            raise ValueError(f"\"{command_name}\" is not in the commands directory")
        self.command_config.update({command_name: {"min_rank":min_rank}})
        self.save_config()
        

    

#JMP:PLAYER           
"""
Ok so player objects are quite unintuitive.
They all inherit from base player and are all "singleton"
The singleton metaclass il also wierd because if you init a CrewMember
with a name that is already in taken by an instance of Player,
the instance of Player will be returned instead of an instance of CrewMember
therefore, all of the methods of CrewMember need to work with Player
"""

class PlayerSingleton(type):
    __instances__:dict[str, "AbstractPlayer"] = {}
    def __call__(cls:"AbstractPlayer", *args, **kargs):
        priority = cls.__priority__ if hasattr(cls, '__priority__') else 0    
        if "name" in kargs:    
            name = kargs['name']
        else:
            name = cls.__name__
        if name in cls.__instances__:
            instance = cls.__instances__[name]
            instance_priority = instance.__priority__ if hasattr(instance, '__priority__') else 0
            #If the class we want to instanciate has higher priority
            if instance_priority < priority:
                #We need to replace that lower priority instance by the higher one
                instance.__class__ = cls
                instance.update_from_lower_class()

        else:
            cls.__instances__[name] = super().__call__(*args, **kargs)
        
        return cls.__instances__[name]



class AbstractPlayer(metaclass = PlayerSingleton):
    """
Base class for player
    """
    __priority__ = 0
    def __init__(self, name, id, connector: Connector):
        self.name = name
        self.id = id
        self.connector = connector
    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}">'

    def to_player(self):
        return NotImplementedError

    def update_from_lower_class(self):
        raise NotImplementedError("Can't update to this class")

class CrewMember(AbstractPlayer):
    """
    Crew member object, with a bunch more crew related info 
    """
    __priority__ = 1
    def __init__(self, name, id, connector):
        super().__init__(name=name, id=id, connector=connector)
        self.crews:list[Crew]
        self.crew_ranks:dict[int, int]
    
    def add_crew(self, crew:Crew, crew_rank:int):
        if not hasattr(self, "crews"):
            self.crews = []
            self.crew_ranks = {}
        if crew not in self.crews:
            #TODO: ask god himself why the hell the "not in" clause don't work
            self.crews.append(crew)
            self.crew_ranks[crew.id] = crew_rank

    def get_rank(self, crew:Crew) -> int:
        if crew in self.crews:
            return self.crew_ranks[crew.id]
        
        raise ValueError(
            f"{self.name} is not a member of {crew.name}"
        )
        

    def to_player(self):
        new =  Player(
            name=self.name,
            connector=self.connector
        )
        return new


class Player(CrewMember):
    """
    Player object, with all the info possible on said player
    collecting all the info takes time and multiple requests
    use this class only when you need to
    """
    __priority__ = 2
    def __init__(self, name:str, connector:Connector):
        super().__init__(name=name, id=0, connector=connector)
        self.connector = connector
        self.update_from_lower_class()
        
    def update_from_lower_class(self):
        url = f"https://scapi.rockstargames.com/profile/getprofile?nickname={self.name}&maxFriends={1000}"
        response = self.connector.request(requests.get, url, auth_type="bearer").json()
        accounts = response["accounts"][0]
        r_account = accounts["rockstarAccount"]
        self.id = r_account["rockstarId"]
        self.country_code = r_account["countryCode"]
        self.bio = r_account["status"]
        for crew_dict in accounts["crews"]:
            crew_name = crew_dict["crewName"]
            crew = Crew(name = crew_name, connector=self.connector)
            self.add_crew(crew=crew, crew_rank=crew_dict["rankOrder"])
    
    def to_player(self):
        return self

