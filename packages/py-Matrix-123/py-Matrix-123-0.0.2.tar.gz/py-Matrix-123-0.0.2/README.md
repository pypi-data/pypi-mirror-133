# py-Matrix-123

## Installation

To install with pip, run: `pip install py-Matrix-123`

## Basic Usage
You can retrieve matrix dimensions, their trace, and performs matrix addition, subtraction, multiplication and scalar multiplication.

requirements:
python3

Here's an example for regular matrices

```python
from pymatrix123 import Matrix

matrices = [
    ([[1], [3], [4], [5]], 
        [[1], [0], [2], [5]]),

    ([[1, 2], [3, -1], [4, 0.0], [5, -18]], 
        [1, 0, 2, 5]),

    ([1.1, 3, 4, 5], 
        [1, 0, -2.0, -5])
]



if __name__ == '__main__':
    for A, B in matrices:
    matrixA = Matrix(A)
    matrixA.trace()
    matrixA.get_dim()
    matrixB = Matrix(B)
    matrixB.trace()
    matrixB.get_dim()
```

```python
from pymatrix123 import Matrix

matrices = [
    ([[1], [3], [4], [5]], 
        [[1], [0], [2], [5]]),

    ([[1, 2], [3, -1], [4, 0.0], [5, -18]], 
        [1, 0, 2, 5]),

    ([1.1, 3, 4, 5], 
        [1, 0, -2.0, -5])
]

if __name__ == '__main__':
    for A, B in matrices:
    matrixA = Matrix(A)
    matrixB = Matrix(B)
    sum_up = matrixA + matrixB
```

Here's an example for square matrices

```python
from pymatrix123 import SquareMatrix

square = [
    ([[1, 2], [3, 4]], 
        [[4, 3], [2, 1]], 
        [[1*4 + 2*2, 1*3 + 2*1], [3*4 + 4*2, 4*1+3*3]]),

    ([[1, 2, 0], 
        [3, 4, -1.0], 
        [2, 4, 0]], 

        [[4, 3, -1], 
        [2, 1, 2.0], 
        [0, 15, -1.1]], 

        [[1*4+2*2+0*0, 1*3+2*1+0*15, 1*(-1)+2*2.0+0*(-1.1)], 
        [3*4+4*2+(-1.0)*0, 4*1+3*3+(-1.0)*15, 3*(-1)+4*2.0+(-1.0)*(-1.1)], 
        [2*4+4*2+0*0, 2*3+4*1+0*15, 2*(-1)+(2.0)*4+0*(-1.1)]]),
]

if __name__ == '__main__':
    for A, B, solution in square:
    matrixA = SquareMatrix(A)
    matrixB = SquareMatrix(B)
    mul = matrixA * matrixB

```

## Reference

| Setup   | Command             | Notes
| :------ | :------------------ | :---------
| install | `pip install pymatrix123`  |

| Creating a CLI | Command                | Notes
| :--------------| :--------------------- | :---------
| import         | `import pymatrix123`          |
| Call           | `Matrix(A)`          | Turns the current list into a matrix object.
| Call           | `SquareMatrix(B)` | Turns the current list into a matrix object.


## License

Licensed under the
[The Python Packaging Authority](pymatrix123/license.txt) License.