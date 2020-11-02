"""
ISIC 2018

@author Max Hornigold
"""


import tensorflow as tf
import matplotlib.pyplot as plt
import math
import glob
from IPython.display import clear_output
from solution import unet_model
from tensorflow.keras import backend as K


def dice_coefficient(y_true, y_pred, smooth = 0.):
    """Compute the dice coefficient for a prediction"""
    
    # change the dimension to one
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    
    # calculation for the loss function
    intersection = K.sum(y_true_f * y_pred_f)
    
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coefficient_loss(y_true, y_pred):
    """Compute the dice coefficient loss for a prediction"""
    return 1. - dice_coefficient(y_true, y_pred)


def compute_dice_coefficients(model, ds):
    """Compute the minimum and the average dice coefficient for all predictions"""
    DCEs = []
    for image, mask in ds:
        pred_mask = model.predict(image[tf.newaxis, ...])
        DCE = dice_coefficient(mask, pred_mask)
        DCEs.append(DCE)
    print("Minimum Dice Coefficient = ", min(DCEs))
    print("Average Dice Coefficient = ", sum(DCEs)/len(DCEs))


def display(display_list):
    """Display plots"""
    plt.figure(figsize=(10, 6))
    for i in range(len(display_list)):
        plt.subplot(1, len(display_list), i+1)
        plt.imshow(display_list[i], cmap='gray')
        plt.axis('off')
    plt.show()


def display_data(ds, n=1):
    """Display the image and mask from a given dataset"""
    for image, mask in ds.take(n):
        display([tf.squeeze(image), tf.squeeze(mask)])


def display_predictions(model, ds, n=1):
    """"Make n predictions using the model and the given dataset"""
    for image, mask in ds.take(n):
        pred_mask = model.predict(image[tf.newaxis, ...])
        display([tf.squeeze(image), tf.squeeze(mask), tf.squeeze(pred_mask)])


def analyse_training_history(history):
    """Plot the acuraccy and val accuracy of the model as it trains"""
    plt.figure(figsize=(10, 6))
    #plt.plot(history.history['accuracy'], label='accuracy')
    #plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.plot(history.history['dice_coefficient'], label='dice_coefficient')
    plt.plot(history.history['val_dice_coefficient'], label = 'val_dice_coefficient')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')
    plt.show()


class DisplayCallback(tf.keras.callbacks.Callback):
    
    def on_epoch_end(self, epoch, logs=None):
        clear_output(wait=True)
        display_predictions(model, val_ds, n=1)


def decode_png(file_path):
    """Decodes a png image"""
    png = tf.io.read_file(file_path)
    png = tf.image.decode_png(png, channels=1)
    png = tf.image.resize(png, (256, 256))
    return png


def decode_jpg(file_path):
    """Decodes a jpeg image"""
    jpg = tf.io.read_file(file_path)
    jpg = tf.image.decode_jpeg(jpg, channels=1)
    jpg = tf.image.resize(jpg, (256, 256))
    return jpg


def process_path(image_fp, mask_fp):
    
    image = decode_jpg(image_fp)
    image = tf.cast(image, tf.float32) / 255.0

    mask = decode_png(mask_fp)
    mask = tf.cast(mask, tf.float32) / 255.0
    mask = tf.math.round(mask)
    
    return image, mask


def import_ISIC_data():
    """ Download the dataset """
    
    # Get images and masks
    images = sorted(glob.glob("C:/Users/Mchor/OneDrive/Desktop/All/Personal/UQ/COMP3710/Assessment/Laboratory Report/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1-2_Training_Input_x2/*.jpg"))
    masks = sorted(glob.glob("C:/Users/Mchor/OneDrive/Desktop/All/Personal/UQ/COMP3710/Assessment/Laboratory Report/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1_Training_GroundTruth_x2/*.png"))

    # choose number of training, validate and test images to use
    num_images = len(images)
    num_training = math.ceil(0.5*num_images)
    num_val = math.ceil(0.2*num_images)
    num_test = math.ceil(0.2*num_images)
    
    # Split the images into train, validate and test datasets
    train_images = [images[i] for i in range(0, num_training)]
    val_images = [images[i] for i in range(num_training, num_training + num_val)]
    test_images = [images[i] for i in range(num_training + num_val, num_training + num_val + num_test)]

    # Split the masks into train, validate and test datasets
    train_masks = [masks[i] for i in range(0, num_training)]
    val_masks = [masks[i] for i in range(num_training, num_training + num_val)]
    test_masks = [masks[i] for i in range(num_training + num_val, num_training + num_val + num_test)]
    
    # make dataset from images and masks
    train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_masks))
    val_ds = tf.data.Dataset.from_tensor_slices((val_images, val_masks))
    test_ds = tf.data.Dataset.from_tensor_slices((test_images, test_masks))

    # shuffle dataset
    train_ds = train_ds.shuffle((len(train_images)))
    val_ds = val_ds.shuffle((len(val_images)))
    test_ds = test_ds.shuffle((len(test_images)))
    
    # map the dataset to process_path function
    train_ds = train_ds.map(process_path)
    val_ds = val_ds.map(process_path)
    test_ds = test_ds.map(process_path)
    
    # return training, validation and testing datasets
    return train_ds, val_ds, test_ds



# import the data
train_ds, val_ds, test_ds = import_ISIC_data()
   
# plot example image
display_data(train_ds, n=1)
   
# create the model
model = unet_model(1, f=6)
    
# show a summary of the model
print(model.summary())

# compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy', # dice_coefficient_loss binary_crossentropy
              metrics=[dice_coefficient]) # accuracy dice_coefficient_loss binary_crossentropy

# specify batch sizes
train_batch_size = 32
val_batch_size = 32

# specify number of epochs
num_epochs = 20

# train the model
history = model.fit(train_ds.batch(train_batch_size), 
                    epochs=num_epochs,
                    validation_data=val_ds.batch(val_batch_size),
                    callbacks=[DisplayCallback()])

# save the model
#model.save("filepath")

# or I could just load the model
#tf.keras.models.load_model("filepath")

# analyse history of training the model
analyse_training_history(history)

# plot some predictions
display_predictions(model, test_ds, n=1)

# compute dice similarity coefficients predictions
compute_dice_coefficients(model, test_ds)