from __future__ import annotations

import socket
from typing import Optional


def resolve(host: str) -> tuple[list[str], Optional[str]]:
    """
    도메인 이름을 IP 주소 리스트로 변환합니다.
    """
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        
        ###########################################################
        # sockaddr에서 IP 주소만 추출하고, 순서를 유지하면서 중복을 제거합니다.
        seen: set[str] = set()
        ips = []
        for info in infos:
            ip = info[4][0]  # sockaddr[0] == IP 주소
            if ip not in seen:
                seen.add(ip)
                ips.append(ip)
        ###########################################################

        return ips, None
    except Exception as e:
        return [], str(e)


def pick_ip(ips: list[str], prefer: str = "any") -> Optional[str]:
    """
    주어진 IP 리스트 중 prefer 정책에 맞는 최적의 IP 하나를 선택하여 반환합니다. 
    
    요구사항:
    1. prefer가 "ipv4"인 경우: 리스트에서 가장 먼저 발견되는 IPv4 주소(:가 없는 주소)를 반환합니다. 
    2. prefer가 "ipv6"인 경우: 리스트에서 가장 먼저 발견되는 IPv6 주소(:가 있는 주소)를 반환합니다. 
    3. 정책에 맞는 주소가 없거나 prefer가 "any"인 경우: 리스트의 첫 번째 주소를 반환합니다. 
    """
    if not ips:
        return None

    ###########################################################
    # prefer 정책에 따라 가장 먼저 발견되는 해당 형식의 주소를 반환합니다.
    if prefer == "ipv4":
        for ip in ips:
            if ":" not in ip:  # IPv4 주소에는 ':'가 없음
                return ip
    elif prefer == "ipv6":
        for ip in ips:
            if ":" in ip:  # IPv6 주소에는 ':'가 있음
                return ip
    ###########################################################

    # 정책에 맞는 주소가 없거나 prefer가 "any"인 경우 첫 번째 주소 반환
    return ips[0]