import requests

DIRECT = "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt"
PROXY = "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/proxy-list.txt"
APPLECN = "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/apple-cn.txt"

TODIRECTADDR = "-**DIRECT**-"
TOPROXYADDR = "-**PROXYADDR**-"


class site:
    def __init__(self, raw):
        self.raw = raw
        if not len(raw):
            self.raw = ''
        if self.raw.startswith('full:'):
            self.type = 'full'
            self.domain = self.raw[5:]
        elif self.raw.startswith('regexp:'):
            self.type = 'regexp'
            self.domain = self.raw[7:]
        else:
            self.type = 'domain'
            self.domain = self.raw

    def adg_dump(self, to_direct):
        if not self.type == 'regexp':
            return f'[/{self.domain}/]{TODIRECTADDR if to_direct else TOPROXYADDR}\n'
        return None

    def clash_dump(self, ):
        pass


def get(path):
    res = requests.get(path)
    reslist = res.text.split('\n') if res.ok else []
    complist = []
    for domain in reslist:
        if not len(domain):
            continue
        complist.append(site(domain))
    return complist


if __name__ == '__main__':
    directlist = list(set(get(DIRECT) + get(APPLECN)))
    proxylist = get(PROXY)
    with open('adg1.txt', 'w', encoding='UTF-8') as f:
        for line in directlist:
            line = line.adg_dump(True)
            if line:
                f.write(line)
        for line in proxylist:
            line = line.adg_dump(False)
            if line:
                f.write(line)
        f.close()
