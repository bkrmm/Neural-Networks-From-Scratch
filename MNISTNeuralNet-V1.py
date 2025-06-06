# import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Load the dataset
traindf = pd.read_csv(r'C:\DHANDA\CursorAI\updatedvenv\train.csv')
train = np.array(traindf)
np.random.shuffle(train)

# Params
m, n = train.shape
train_dev = train[0:1000].T
Y_dev = train_dev[0]
X_dev = train_dev[1:n]

X_dev = X_dev / 255

train_data = train[1000:m].T
Ytrain = train_data[0]
Xtrain = train_data[1:n]
Xtrain = Xtrain / 255
_,m_train = Xtrain.shape

#Forward Propagation
def init_params():
    W1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) - 0.5
    W2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    return W1, b1, W2, b2

def ReLU(Z):
    return np.maximum(0, Z)

def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A

def ForwardPropagation(W1,b1,W2,b2,X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2

def one_hot(Y):
    one_hot_y = np.zeros((Y.size, Y.max() + 1))
    one_hot_y[np.arange(Y.size), Y] = 1
    one_hot_y = one_hot_y.T
    return one_hot_y

def derivative_ReLU(Z):
    return Z > 0

def BackPropagation(Z1,A1,Z2,A2,W1,W2,X,Y):
    one_hot_y = one_hot(Y)
    dZ2 = A2 - one_hot_y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2,axis = 1, keepdims=True)
    dZ1 = W2.T.dot(dZ2) * derivative_ReLU(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1,axis = 1, keepdims=True)
    return dW1, db1, dW2, db2

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2

def get_predictions(A2):
    return np.argmax(A2, 0)

def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.mean(predictions == Y) / Y.size

def gradient_descent(X,Y,iterations, alpha):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = ForwardPropagation(W1,b1,W2,b2,X)
        dW1, db1, dW2, db2 = BackPropagation(Z1,A1,Z2,A2,W1,W2,X,Y)
        W1, b1, W2, b2 = update_params(W1,b1,W2,b2,dW1,db1,dW2,db2,alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            print("Accuracy", get_accuracy(get_predictions(A2), Y))
    return W1, b1, W2, b2

W1, b1, W2, b2 = gradient_descent(Xtrain, Ytrain, 500, 0.1)
