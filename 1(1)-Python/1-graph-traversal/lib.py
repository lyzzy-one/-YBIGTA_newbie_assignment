from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
    
        self.n = n
        self.graph: list[list[int]] = [[] for _ in range(n + 1)]
        
    

    
    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def dfs(self, start: int) -> list[int]:
        visited = [False] * (self.n + 1)
        result: list[int] = []
        
        def recur(node: int) -> None:
            visited[node] = True          # 방문 표시
            result.append(node)           # 순서에 기록
            for nxt in sorted(self.graph[node]):   # 이웃을 작은 번호부터
                if not visited[nxt]:      # 아직 안 갔으면
                    recur(nxt)
        recur(start)
        return result
    
    def bfs(self, start: int) -> list[int]:
        visited = [False] * (self.n + 1)
        result: list[int] = []
        queue = deque([start])
        visited[start] = True
        while queue:
            node = queue.popleft()        # 큐 앞에서 하나 꺼냄
            result.append(node)
            for nxt in sorted(self.graph[node]):
                if not visited[nxt]:
                    visited[nxt] = True   # 큐에 넣을 때 방문 표시! (중복 방지)
                    queue.append(nxt)
        return result
    
    def search_and_print(self, start: int) -> None:
    
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))
