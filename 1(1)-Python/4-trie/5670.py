from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = trie.find_child(pointer, ord(element))  # 다음 글자로 이동
        assert new_index is not None  # query_seq는 trie에 이미 삽입되어 있어 항상 존재

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    """
    여러 테스트케이스를 입력받아 각각의 평균 버튼 입력 횟수를 출력한다.
    각 케이스마다 N개의 단어로 트라이를 만든 뒤, 모든 단어의 count 합을
    N으로 나눈 평균을 소수점 둘째 자리까지 출력한다.
    """
    data: list[str] = sys.stdin.read().split()
    i: int = 0
    out: list[str] = []

    while i < len(data):
        n: int = int(data[i])
        i += 1
        words: list[str] = data[i:i + n]
        i += n

        trie: Trie = Trie()
        for word in words:
            trie.push(map(ord, word))   # 글자를 ord(int)로 저장

        total: int = sum(count(trie, word) for word in words)
        out.append(f"{total / n:.2f}")

    print("\n".join(out))


if __name__ == "__main__":
    main()