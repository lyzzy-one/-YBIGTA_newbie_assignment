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