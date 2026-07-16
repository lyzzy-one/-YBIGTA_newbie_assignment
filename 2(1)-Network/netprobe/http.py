from __future__ import annotations

from typing import Optional


def build_request(host: str, path: str) -> bytes:
    """
    HTTP GET 요청 메시지를 바이트 형태로 생성합니다.
    """
    if not path.startswith("/"):
        path = "/" + path

    ###########################################################
    # HTTP/1.1 규격: 각 줄은 \r\n으로 끝나며, 헤더 끝에는 빈 줄(\r\n)이 하나 더 필요합니다.
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    ###########################################################

    return req.encode("utf-8")


def send_and_recv(sock, request: bytes, max_bytes: int) -> bytes:
    
    sock.sendall(request)

    chunks: list[bytes] = []
    total = 0
    while True:
        data = sock.recv(4096)
        if not data:
            break
        chunks.append(data)
        total += len(data)
        if total > max_bytes:
            break
    return b"".join(chunks)


def parse_status_and_preview(raw: bytes, max_preview: int = 200) -> tuple[Optional[int], str, Optional[str]]:
    """
    서버의 Raw 응답 데이터를 분석하여 상태 코드와 본문 미리보기를 추출합니다. 
    
    요구사항:
    1. 헤더와 바디를 구분하는 CRLF 2번(b"\\r\\n\\r\\n")의 위치를 찾으세요. 
    2. 헤더 영역을 decode한 뒤, Status Line(첫 줄)에서 상태 코드를 추출하세요. 
    3. 바디 영역에서 max_preview 만큼의 데이터를 decode하여 반환하세요. 
    4. 규격에 맞지 않는 데이터가 들어올 경우 적절한 에러 메시지를 반환하세요. 
    """
    
    status_code = None
    preview = ""
    error = None

    ###########################################################
    # 1. b"\r\n\r\n"를 기준으로 헤더와 바디를 분리합니다.
    sep = raw.find(b"\r\n\r\n")
    if sep == -1:
        return None, "", "Invalid HTTP response: header/body separator not found"

    header_bytes = raw[:sep]
    body_bytes = raw[sep + 4:]  # b"\r\n\r\n" 길이(4)만큼 건너뜀

    # 2. 첫 줄(Status Line)에서 상태 코드(int)를 추출합니다.
    header_text = header_bytes.decode("utf-8", errors="replace")
    status_line = header_text.split("\r\n")[0]
    parts = status_line.split()
    # 예: "HTTP/1.1 200 OK" -> parts[1] == "200"
    if len(parts) < 2 or not parts[0].startswith("HTTP/"):
        return None, "", f"Invalid status line: {status_line!r}"
    try:
        status_code = int(parts[1])
    except ValueError:
        return None, "", f"Invalid status code: {parts[1]!r}"

    # 3. 바디 영역을 max_preview 만큼 decode하여 preview를 만듭니다.
    preview = body_bytes[:max_preview].decode("utf-8", errors="replace")
    ###########################################################


    return status_code, preview, error