from .generalmatrix import Matrix


class SquareMatrix(Matrix):
    def __init__(self, matrix=None):
        Matrix.__init__(self, matrix)

    def __mul__(self, other):
        """ Function to multiply together two Matrices
        of size n-by-m
        
        Args:
            other (Matrix): Matrix instance
            
        Returns:
            Matrix: A different
            
        """
        m = int(self.get_dim().split('-')[2])
        q = int(other.get_dim().split('-')[0])
        result = [None for _ in range(m)]
        if m == q:
            for i in range(m):
                vals = []
                for j in range(m):
                    total = 0
                    for k in range(m):
                        total += self.entries[i][k] * other.entries[k][j]
                    vals.append(total)
                result[i] = vals
        else:
            result = None

        result = Matrix(result)
        return result
        
    def trace(self):
        """ Function to take the trace of a Matrices
        of size n-by-n

        n (int) number of rows and column

        Args:
            None
            
        Returns:
            float

        e.g. give A = 1 2 3 4 5
                      4 3 2 1 1
                      0 1 5 6 9
                      0 0 2 3 8
                      1 1 2 9 9
        
        then the trace of A is the sum
        A[0][0] + A[1][1] + A[2][2] + A[3][3] + A[4][4] = 21
           1         3         5         3         9
        """
        trace = 0
        n = int(self.get_dim().split('-')[0])
        for i in range(n):
            trace += self.entries[i][i]

        return trace
