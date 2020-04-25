from training_data import training_data_angle
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

training_data_x, training_data_y = training_data_angle()

model = Sequential()
model.add(Dense(units=25, input_dim=4))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(output_dim=1,  activation='tanh'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])


model.fit(np.array(training_data_x).reshape(-1, 4), np.array(training_data_y).reshape(-1, 1), nb_epoch=3)

model.save('model.h5')
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)
