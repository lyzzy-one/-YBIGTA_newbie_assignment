from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        pointer = 0
        for element in seq:
            child = self.find_child(pointer, element)
            if child is None:                       # 없으면 새 노드 생성
                self.append(TrieNode(body=element))
                child = len(self) - 1
                self[pointer].children.append(child)
            pointer = child
        self[pointer].is_end = True                 # 단어 끝 표시

    def find_child(self, index: int, element: T) -> Optional[int]:
        """index 노드의 자식 중 body == element 인 노드의 인덱스를 반환 (없으면 None)"""
        for child in self[index].children:
            if self[child].body == element:
                return child
        return None


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