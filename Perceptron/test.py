import numpy as np

class Perceptron:
    def __init__(self, LR=0.1):
        self.LR = LR
        self.bias = 0.0
        self.weight = None
        self.misclassified_samples = []

    def fit(self, x, y, No_Iterations=10):
        self.bias = 0.0
        self.weight = np.zeros(x.shape[1])
        self.misclassified_samples = []

        for _ in range(No_Iterations):
            errors_values = 0
            for xi, yi in zip(x, y):
                update = self.LR * (yi - self.predict(xi))

                self.bias += update
                self.weight += update * xi
                errors_values += int(update != 0.0)

            self.misclassified_samples.append(errors_values)

    def f(self, x):
        return np.dot(x, self.weight) + self.bias

    def predict(self, x):
        return np.where(self.f(x) >= 0, 1, -1)