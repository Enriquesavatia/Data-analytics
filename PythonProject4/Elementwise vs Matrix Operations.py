import numpy as np
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])

#Addition
elemntwise_add = A + B

#Multiplication
elementwise_mul = A * B

#Matrix product
matrix_product = A @ B

print("A:\n", A)
print("B:\n", B)
print("elemntwise_add:\n", elemntwise_add)
print("elementwise_mul:\n", elementwise_mul)
print("matrix_product:\n", matrix_product)