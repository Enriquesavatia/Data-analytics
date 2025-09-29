import numpy as np
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])

#Addition
elementwise_add = A + B

#Multiplication
elementwise_mul = A * B

#Matrix product
matrix_product = A @ B

print("A:\n", A)
print("B:\n", B)
print("elementwise_add:\n", elementwise_add)
print("elementwise_mul:\n", elementwise_mul)
print("matrix_product:\n", matrix_product)

