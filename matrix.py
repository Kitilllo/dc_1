import copy


class Matrix:
    def __init__(self, data=None):
        self.data = copy.deepcopy(data)

        if data is not None:
            self.height = len(data)
            self.width = len(data[0])

            for row in data:
                if len(row) != self.width:
                    raise Exception("Row width is not equal")

    @classmethod
    def from_file(cls, filename):
        data = []

        with open(filename, "r") as f:
            for line in f.readlines():
                numbers_str = line.split()

                numbers = [float(number) if '.' in number else int(number) for number in numbers_str]
                data.append(numbers)

        return cls(data)

    def __add__(self, other):
        if self.data is None or other.data is None:
            raise Exception("Can`t operate with uninitialized matrix")

        if self.width != other.width or self.height != other.height:
            raise Exception("Matrix shapes is not equal")

        data = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                data[i][j] += other.data[i][j]

        return Matrix(data)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.__mul_matrix(other)
        else:
            return self.__mul_number(other)

    def __mul_matrix(self, other):
        if self.data is None or other.data is None:
            raise Exception("Can`t operate with uninitialized matrix")

        if self.width != other.height:
            raise Exception("Can`t operate. Matrix mismatch")

        data = [[0 for _ in range(other.width)] for _ in range(self.height)]

        for i in range(self.height):
            for j in range(other.width):
                for k in range(other.height):
                    tmp = self.data[i][k] * other.data[k][j]
                    data[i][j] += tmp
        return Matrix(data)

    def __mul_number(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            raise Exception("Matrix multiplies only on float or int")

        if self.data is None:
            raise Exception("Can`t operate with uninitialized matrix")

        data = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                data[i][j] *= other
        return Matrix(data)

    def transpose(self):
        data = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                data[j][i] = self.data[i][j]
        return Matrix(data)

    def __str__(self):
        ret_str = ""

        for row in self.data:
            row_str = ""
            for number in row:
                row_str += f"{number} "
            row_str += '\n'

            ret_str += row_str

        return ret_str


if __name__ == "__main__":
    a = Matrix.from_file("tests/data.txt")
    b = Matrix.from_file("tests/data2.txt")

    with open('tests/out.txt', "w") as f:
        f.write(str(a*b))
