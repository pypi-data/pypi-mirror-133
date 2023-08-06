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

"""    
    matrix A:
            1 
            3 
            4
            5

    matrix B:
            1
            0
            2
            5
"""

matrixA = Matrix([[1], [3], [4], [5]])
matrixB = Matrix([[1], [0], [2], [5]])
print(matrixA + matrixB)
```

Here's an example for square matrices

```python
from pymatrix123 import SquareMatrix

"""    
    matrix A:
            1 2
            3 4

    matrix B:
            3 4
            2 1
"""
        
matrixA = SquareMatrix([[1, 2], [3, 4]])
matrixB = SquareMatrix([[4, 3], [2, 1]])
print(matrixA.trace())
print(matrixA.get_dim())
print(matrixB.trace())
print(matrixB.get_dim())
print(matrixA * matrixB)

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