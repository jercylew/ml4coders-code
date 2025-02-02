# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
import os.path
# https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an \"AS IS\" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import urllib.request
import zipfile
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
import tensorflow as tf

training_dir = 'horse-or-human/training/'
validation_dir = 'horse-or-human/validation/'


def download_data_files():
    """Download data files from server"""
    if not os.path.exists(training_dir):
        print("Data files not downloaded, download it now...")
        training_url = "https://storage.googleapis.com/learning-datasets/horse-or-human.zip"
        training_file_name = "horse-or-human.zip"

        urllib.request.urlretrieve(training_url, training_file_name)

        zip_ref = zipfile.ZipFile(training_file_name, 'r')
        zip_ref.extractall(training_dir)
        zip_ref.close()

    if not os.path.exists(validation_dir):
        validation_url = "https://storage.googleapis.com/learning-datasets/validation-horse-or-human.zip"
        validation_file_name = "validation-horse-or-human.zip"
        urllib.request.urlretrieve(validation_url, validation_file_name)

        zip_ref = zipfile.ZipFile(validation_file_name, 'r')
        zip_ref.extractall(validation_dir)
        zip_ref.close()


download_data_files()
# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
        training_dir,
        target_size=(300, 300),
        class_mode='binary')

# All images will be rescaled by 1./255
validation_datagen = ImageDataGenerator(rescale=1/255)

validation_generator = train_datagen.flow_from_directory(
        validation_dir,
        target_size=(300, 300),
        class_mode='binary')

model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 300x300 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(300, 300, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The fourth convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fifth convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('horses') and 1 for the
    # other ('humans')
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(learning_rate=0.001),
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    epochs=15,
    validation_data=validation_generator)

