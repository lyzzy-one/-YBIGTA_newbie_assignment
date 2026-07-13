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


from math import factorial
import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


MOD: int = 1234567891


def main() -> None:
    """
    N개의 이름으로 트라이를 만들고 '아름다운 이름' 배치의 경우의 수를 출력한다.
    각 노드에서 배치 가능한 가지 수(자식 수 + 그 노드에서 끝나는 단어)의
    팩토리얼을 모두 곱한 값을 MOD(1234567891)로 나눈 나머지를 출력한다.
    """
    data: list[str] = sys.stdin.read().split()
    n: int = int(data[0])
    names: list[str] = data[1:1 + n]

    trie: Trie = Trie()
    for name in names:
        trie.push(map(ord, name))   # 글자를 ord(int)로 저장

    # 각 노드에서 배치 가능한 가지 수(자식 + 여기서 끝나는 단어)의 팩토리얼을 모두 곱함
    answer: int = 1
    for node in trie:
        groups: int = len(node.children) + (1 if node.is_end else 0)
        answer = answer * factorial(groups) % MOD

    print(answer)


if __name__ == "__main__":
    main()