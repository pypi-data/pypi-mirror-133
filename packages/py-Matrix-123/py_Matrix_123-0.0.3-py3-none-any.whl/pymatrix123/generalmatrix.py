# python3

import copy


class Matrix:
    def __init__(self, matrix=None):
        """ A gerneral n-by-m matrix class for
        calculating basic algebra.
        Note: The matrix A is said to represent the linear map f, 
              and A is called the transformation matrix of f.

            Attributes:
            n (int) the number of rows in the matrix
            m (int) the number of columns in the matrix
            with 0 < n * m < 2 ** 20

            matrix (list[list[floats]] the list of lists of floats

        """
        self._n = 0
        self._m = 0
        self.entries = []
        if matrix:
            self.add(matrix)

    def get_dim(self):
        """ A method to return the dimension of
        the matrix class

        Args: None

        Return:
            dimension of the matrix
            e.g. A = 0 1 2
                     3 2 5
                     0 1 1
                     7 6 5

            So should return 4-by-3

        """
        return "{}-by-{}".format(self._n, self._m)

    def add(self, nums):
        """ Function to add to the matrix attributes:

        Args:
            list[int] or list[list[int]]

        Returns:
            None
        """

        n = len(nums)
        if n == 0:
            return

        try:
            m = len(nums[0])
        except TypeError:
            for i in range(n):
                nums[i] = [nums[i]]
            m = 1

        self._add_dim(n, m)
        self._add_Matrix(nums)

    def read_data_file(self, file_name):
        """ Method in Matrix class to read in data from a txt file. The txt file
        should have 2 numbers (the number of rows value and the number
        of columns) in the first line. The next lines should be an equal number
        of values (floats).

        The numbers are stored in the data attributes
        e.g.
        txt file should look like this

        2 3
        1 2 5.0
        6 -1 0

        Args:
            file_name (string): name of a file to read from

        Returns:
            None

        """
        with open(file_name) as f:
            data_list = []
            lines = f.readlines()
            n, m = list(map(int, lines[0].split()))
            for line in lines[1:]:
                vals = list(map(float, line.split()))
                data_list.append(vals)

        f.close()

        if n == len(data_list) and m == len(data_list[0]):
            self._add_dim(n, m)
            self._add_Matrix(data_list)
        else:
            print("file needs to be in correct format")

    def _add_dim(self, n, m):
        """ Private method util function to add dimension to the rectangular matrix

        Args:
            n (int) number of rows
            m (int) numbers of columns

        Returns:
            None

        """
        self._n = n
        self._m = m

    def _add_Matrix(self, nums):
        """ Private method util function to add a list of lists of values
        to the matrix class to obtain a matrix class

        Args:
            list[list[float]] or list[float]

        Returns:
            None

        """
        self.entries = [None for i in range(self._n)]
        for i in range(self._n):
            self.entries[i] = nums[i]

    def __add__(self, other):
        """ Function to add together two Matrices
        
        Args:
            other (Matrix): Matrix instance
            
        Returns:
            Matrix
            
        """
        result = Matrix()
        temp = [None for _ in range(self._n)]

        if self.get_dim() == other.get_dim():
            n, m = self._n, self._m
            for i in range(n):
                vals = []
                for j in range(m):
                    sum_index = self.entries[i][j] + other.entries[i][j]
                    vals.append(sum_index)
                temp[i] = vals

        else:
            return result

        result.add(temp)
        return result
    
    def __sub__(self, other):
        """ Function to subtract together two Matrices
        
        Args:
            other (Matrix): Matrix instance
            
        Returns:
            Matrix
            
        """
        result = Matrix()
        temp = [None for _ in range(self._n)]

        if self.get_dim() == other.get_dim():
            n, m = self._n, self._m
            for i in range(n):
                vals = []
                for j in range(m):
                    sum_index = self.entries[i][j] - other.entries[i][j]
                    vals.append(sum_index)
                temp[i] = vals

        else:
            return result

        result.add(temp)
        return result

    def __mul__(self, num):
        """ Function to multiply together two Matrices
        
        Args:
            other (Matrix): Matrix instance
            
        Returns:
            Matrix: A different
            
        """

        temp = [[] for i in range(self._n)]
        for i in range(self._n):
            for j in range(self._m):
                temp[i].append(num * self.entries[i][j])
        
        return Matrix(temp)

    def __str__(self):
        """ Function to output the matrix of the Matrix instance
        
        Args:
            None
        
        Returns:
            string
        
        """
        return str(self.entries)
