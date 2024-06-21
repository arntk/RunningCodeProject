import pandas as pd
import openai
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets

# Create a simple DataFrame with pandas
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
print(df)

# Create a simple plot with matplotlib
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title("Simple Plot")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.show()

# Load a sample dataset with scikit-learn
iris = datasets.load_iris()
print(f"Dataset loaded successfully. Iris data shape: {iris.data.shape}")