from lib import Trie
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