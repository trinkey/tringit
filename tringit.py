import os
import ast
import json
try:
    import requests
except ImportError:
    print("Requests library not found, installing it now. If this doesn't work, try manually installing it (pip install requests)")
    import pip
    pip.main(["install", "requests"])
    import requests

class Main:
    def __init__(self):
        print("Setting up...")
        self.debug = True
        self.version = 0.1
        self.path = os.path.abspath(".")
        self.id = ""
        self.defaultFilenames = [
            "index.html",
            "main.py"
        ]
        self.fileBlacklist = [
            os.path.basename(__file__),
            "library.json",
            "library-parser.py"
        ]

        if not os.path.exists(f"{self.path}/.tringit"):
            os.makedirs(f"{self.path}/.tringit")
            with open(f"{self.path}/.tringit/cookie.txt", "x") as f:
                pass
            with open(f"{self.path}/.tringit/current.txt", "x") as f:
                pass

        self.cookie = open(f"{self.path}/.tringit/cookie.txt", "r", encoding="utf-8").read()
        if not self.cookie:
            self.cookie = input("Please enter your cookie.\n>>> ")
            f = open(f"{self.path}/.tringit/cookie.txt", "w")
            f.write(self.cookie)
            f.close()

        self.shortID = open(f"{self.path}/.tringit/current.txt", "r").read()
        if not self.shortID:
            self.shortID = input("Please enter the trinket id (found in the url).\n>>> ")
            f = open(f"{self.path}/.tringit/current.txt", "w")
            f.write(self.shortID)
            f.close()

        try:
            info = self.loadInfo(self.shortID)
            self.longID = info["longID"]
            self.name = info["name"]
            self.lang = info["lang"]
        except:
            print("The ID inputted is either incorrect or the trinket has been deleted.")
            self.shortID = input("Please enter the trinket id (found in the url).\n>>> ")
            f = open(f"{self.path}/.tringit/current.txt", "w")
            f.write(self.shortID)
            f.close()

        while True:
            f = input(f"What do you want to do?\n1- Change trinket (Current: {self.name} - {self.lang} / {self.shortID})\n2- Clone current state of the trinket to current directory\n3- Push current changes to trinket\n4- Dump trinket library files\n5- Reset cookie\n6- List your published trinkets\n>>> ")
            if f == "1":
                self.shortID = input("Please enter the trinket id (found in the url).\n>>> ")
                print("Getting info...")
                f = open(f"{self.path}/.tringit/current.txt", "w")
                f.write(self.shortID)
                f.close()
                info = self.loadInfo(self.shortID)
                self.longID = info["longID"]
                self.name = info["name"]
                self.lang = info["lang"]
            elif f == "2":
                print("Cloning...")
                self.clone()
            elif f == "3":
                print("Pushing...")
                print(self.push())
            elif f == "4":
                print("Getting trinket list...")
                try:
                    g = open(f"{self.path}/library.json", "x")
                except:
                    g = open(f"{self.path}/library.json", "w")
                g.write(json.dumps(self.trinketList()))
                g.close()
                print("Wrote library files to library.json")
            elif f == "5":
                self.cookie = input("Please enter your cookie.\n>>> ")
                f = open(f"{self.path}/.tringit/cookie.txt", "w")
                f.write(self.cookie)
                f.close()
            elif f == "6":
                print("Getting trinket list...")
                x = self.trinketList()
                for i in x["trinkets"]:
                    if i["published"]:
                        print(f"/sites/{i['published']}")
                for i in x["folders"]:
                    for o in x["folders"][i]:
                        if o["published"]:
                            print(f"/sites/{o['published']}")
            else:
                print("Invalid input")

    def sortKey(self, thing):
        fileType = thing.split(".")[-1]
        if thing in self.defaultFilenames:
            return "A" + fileType + thing
        else:
            return "B" + fileType + thing

    def dpr(self, string):
        if self.debug:
            print(string)

    def clone(self):
        f = self.loadInfo(self.shortID)
        for i in os.listdir(self.path):
            if os.path.isfile(i) and i not in self.fileBlacklist:
                os.remove(f"{self.path}/{i}")
        for i in f["code"]:
            try:
                g = open(f"{self.path}/{i['name']}", "x")
            except:
                g = open(f"{self.path}/{i['name']}", "w")
            g.write(i["code"])
            g.close()

    def trinketList(self):
        trinkets = []
        f = requests.get("https://trinket.io/api/trinkets?sort=name", headers=self.getHeaders()).json()["data"]

        for i in f:
            k = self.loadInfo(i["shortCode"])
            trinkets.append({
                "name"      : i["name"],
                "shortID"   : i["shortCode"],
                "longID"    : k["longID"],
                "lang"      : i["lang"],
                "code"      : k["code"],
                "published" : False if "published" not in k or not k["published"] else k["slug"]
            })

        output = {
            "trinkets": [i for i in trinkets],
            "folders": {}
        }

        f = requests.get("https://trinket.io/api/folders", headers=self.getHeaders()).json()["data"]
        for i in f:
            trinkets = []
            g = requests.get(f"https://trinket.io/api/folders/{i['id']}/trinkets?sort=name", headers=self.getHeaders()).json()["data"]
            for o in g:
                k = self.loadInfo(o["shortCode"])
                trinkets.append({
                    "name"      : o["name"],
                    "shortID"   : o["shortCode"],
                    "longID"    : k["longID"],
                    "lang"      : o["lang"],
                    "code"      : k["code"],
                    "published" : k["published"]
                })
            output["folders"][i["name"]] = [i for i in trinkets]

        return output

    def loadInfo(self, id):
        x = requests.get(f"https://trinket.io/api/trinkets/{id}").json()["data"]
        files = []
        try:
            for i in ast.literal_eval(x["code"]):
                files.append({
                    "name": i["name"],
                    "code": i["content"].replace("\\\"", "\"")
                })
        except ValueError:
            files.append({
                "name": "main.music",
                "code": x["code"]
            })

        return {
            "name"      : x["name"],
            "longID"    : x["id"],
            "shortID"   : id,
            "lang"      : x["lang"],
            "code"      : files,
            "published" : False if not x["published"] else x["slug"]
        }

    def getHeaders(self):
        return {
            "Host": "trinket.io",
            "User-Agent": f"Tringit v0.1 (Python)",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://trinket.io",
            "DNT": "1",
            "Cookie": self.cookie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1"
        }

    def push(self):
        code = ""
        for i in sorted(os.listdir(self.path), key=self.sortKey):
            if i not in self.fileBlacklist and os.path.isfile(f"{self.path}/{i}"):
                code += '{"name": "' + i + '", "content": "' + open(f"{self.path}/{i}", "r").read().replace("\\", "\\\\").replace("\n", "\\n").replace("\"", "\\\"") + '"},'

        return requests.put(
            f"https://trinket.io/api/trinkets/{self.longID}/code",
            headers=self.getHeaders(),
            json={
                "assets": [],
                "code": f"[{code[:-1:]}]",
                "settings": {"astro_pi_mission_submission": False, "autofocusEnabled": True, "testsEnabled": False}
            }
        )

if __name__ == "__main__":
    Main()
