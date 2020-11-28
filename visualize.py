import tensorflow as tf
import numpy as np
from network import Network
import matplotlib.pyplot as plt

network = Network()
model=tf.keras.models.load_model('network.h5')
train_X, train_Y, test_X, test_Y=network.read_data()
# model, history=network.fit(model,train_X, train_Y, test_X, test_Y)
model.summary()

print(train_X.shape)
img_tensor = train_X[3000]
# print(data_set.shape)
img_tensor = np.expand_dims(img_tensor, axis = 0)
img_tensor /= 255.
print(img_tensor.shape)


layer_outputs = [layer.output for layer in model.layers[:6]]
activation_model = tf.keras.models.Model(inputs = model.input, outputs = layer_outputs)

activations = activation_model.predict(img_tensor)

first_layer_activation = activations[0]

layer_names = []
for layer in model.layers[:8]:
    layer_names.append(layer.name)
    
images_per_row = 16

for layer_name, layer_activation in zip(layer_names, activations):
    n_features = layer_activation.shape[-1]
    
    size = layer_activation.shape[1]
    
    n_cols = n_features // images_per_row
    display_grid = np.zeros((size * n_cols, images_per_row * size))
    
    for col in range(n_cols):
        for row in range(images_per_row):
            channel_image = layer_activation[0,
                                            :,:,
                                            col * images_per_row + row]
            channel_image -= channel_image.mean()
            channel_image /= channel_image.std()
            channel_image *= 64
            channel_image += 128
            channel_image = np.clip(channel_image, 0, 255).astype('uint8')
            display_grid[col * size : (col + 1) * size, row * size : (row + 1) * size] = channel_image
            
    scale = 1./size
    plt.figure(figsize=(scale * display_grid.shape[1], scale * display_grid.shape[0]))

    plt.title(layer_name)
    plt.grid(False)
    plt.imshow(display_grid, aspect='auto', cmap='viridis')
plt.show()