from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """
        matrix[i, j] = value 형태의 대입을 처리한다.
        key = (i, j) 위치에 value를 MOD로 나눈 나머지를 저장하여,
        행렬 원소가 항상 0 ~ MOD-1 범위를 유지하도록 한다.
        """
        self.matrix[key[0]][key[1]] = value % Matrix.MOD

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        """
        행렬의 n제곱(self ** n)을 분할 정복으로 계산해 반환한다.
        단위행렬에서 시작해, 지수 n을 이진수로 보고 비트가 1인 자리에서만
        현재 base를 곱하며 base는 매 단계 제곱한다. 시간복잡도 O(log n).
        """
        result = Matrix.eye(self.shape[0])  # 단위행렬로 시작
        base = self.clone()
        while n > 0:
            if n & 1:                        # 지수의 현재 비트가 1이면 결과에 곱하기
                result = result @ base
            base = base @ base               # base 제곱 (분할 정복)
            n >>= 1                          # 지수를 절반으로
        return result

    def __repr__(self) -> str:
        """
        행렬을 출력용 문자열로 변환한다.
        각 원소는 MOD로 나눈 나머지를 공백으로, 각 행은 개행으로 이어 붙인다.
        (print(matrix)나 str(matrix) 호출 시 이 형식이 사용된다.)
        """
        return "\n".join(
            " ".join(str(x % Matrix.MOD) for x in row) for row in self.matrix
        )


from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)

    print(modmat ** B)


if __name__ == "__main__":
    main()