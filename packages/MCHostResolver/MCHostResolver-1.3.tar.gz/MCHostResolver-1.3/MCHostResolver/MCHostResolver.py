import colorama
import dns.resolver
import socket

from colorama import Fore
colorama.init()

colors = [Fore.RED, Fore.CYAN, Fore.WHITE, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.GREEN, Fore.YELLOW]

class IPFinder():
    def resolve(ip):
        """Returns a resolved ip:port from hostname
        :param ip: Minecraft server hostname (e.g - hypixel.net)"""
        host = ip
        port = None
        if ":" in ip:
            parts = ip.split(":")
            if len(parts) > 2:
                raise ValueError("Неверный адресс '%s'" % ip)
            host = parts[0]
            port = int(parts[1])
        if port is None:
            port = 25565
            try:
                answers = dns.resolver.query("_minecraft._tcp." + host, "SRV")
                if len(answers):
                    answer = answers[0]
                    host = str(answer.target).rstrip(".")
                    port = int(answer.port)
                    fullip = socket.gethostbyname(host)
                    realyfull = fullip + ":" + str(port)
            except Exception:
                raise ValueError("Неверный адрес '%s'" % ip)
        return realyfull
    def resonlyip(ip):
        """Returns a resolved ip from hostname
        :param ip: Minecraft server hostname (e.g - hypixel.net)"""
        host = ip
        port = None
        if ":" in ip:
            parts = ip.split(":")
            if len(parts) > 2:
                raise ValueError("Неверный адресс '%s'" % ip)
            host = parts[0]
            port = int(parts[1])
        if port is None:
            try:
                answers = dns.resolver.query("_minecraft._tcp." + host, "SRV")
                if len(answers):
                    answer = answers[0]
                    host = str(answer.target).rstrip(".")
                    fullip = socket.gethostbyname(host)
            except Exception:
                raise ValueError("Неверный адрес '%s'" % ip)
        return fullip
