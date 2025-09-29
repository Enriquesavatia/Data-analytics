import math
class Rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length

        def area(self):
            return self.width * self.length

        def perimeter(self):
            return 2 * (self.width + self.length)

        def diagonal(self):
            return (self.width ** 2) + (self.length ** 2)

        def bounding_box(self, x=0, y=0):
            return (x,y, x + self.width, y + self.length)

        #Testing the Rectangle class
        if __name__ == '__main__':
            rect =Rectangle(4, 5)
            print("area:", rect.area())
            #Output:20
            print("perimeter:", rect.perimeter())

            print("Diagonal:", rect.diagonal())

            print("Bounding box:", rect.bounding_box())