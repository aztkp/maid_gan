from keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = (X_train.astype(np.float32) - 127.5)/127.5
X_train = X_train[:, :, :, None]
train_num = X_train.shape[0]
train_num_per_step = train_num // 64
