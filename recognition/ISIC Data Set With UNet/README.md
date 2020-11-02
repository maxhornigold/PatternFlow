# ISIC data set with U-Net
My solution to the ISIC data set using a U-Net model.

The folder contains the following two files:
* driver_script.py
* solution.py


## solution.py

This is the U-Net model. It is implemented entirely in TensorFlow.

This file does not need to be run. Instead, it is imported into driver_script.py


## driver_script.py

This is the driver script. This file:
* imports the data.
* manipulates the data into various datasets for training, validating and testing.
* import the model from solution.py and compile this model.
* train the model using the datasets.
* makes and plots predictions using the model.

Call this file to run.
Will need to change where your images are saved. Currently, I am pulling them from my computer.

## Results

When we run the driver script, the first thing it does it output an example image and mask from the training dataset.
This image is shown below.

![alt text]()

### Next, the model is created.

The model summary is output. The output is shown below.

Layer (type)                    Output Shape         Param #     Connected to                     

input_2 (InputLayer)            [(None, 256, 256, 1) 0

conv2d_19 (Conv2D)              (None, 256, 256, 6)  60          input_2[0][0]                    

conv2d_20 (Conv2D)              (None, 256, 256, 6)  330         conv2d_19[0][0]                  

max_pooling2d_4 (MaxPooling2D)  (None, 128, 128, 6)  0           conv2d_20[0][0]                  

conv2d_21 (Conv2D)              (None, 128, 128, 12) 660         max_pooling2d_4[0][0]            

conv2d_22 (Conv2D)              (None, 128, 128, 12) 1308        conv2d_21[0][0]                  

max_pooling2d_5 (MaxPooling2D)  (None, 64, 64, 12)   0           conv2d_22[0][0]                  

conv2d_23 (Conv2D)              (None, 64, 64, 24)   2616        max_pooling2d_5[0][0]            

conv2d_24 (Conv2D)              (None, 64, 64, 24)   5208        conv2d_23[0][0]                  

max_pooling2d_6 (MaxPooling2D)  (None, 32, 32, 24)   0           conv2d_24[0][0]                  

conv2d_25 (Conv2D)              (None, 32, 32, 48)   10416       max_pooling2d_6[0][0]            

conv2d_26 (Conv2D)              (None, 32, 32, 48)   20784       conv2d_25[0][0]                  

max_pooling2d_7 (MaxPooling2D)  (None, 16, 16, 48)   0           conv2d_26[0][0]                  

conv2d_27 (Conv2D)              (None, 16, 16, 96)   41568       max_pooling2d_7[0][0]            

conv2d_28 (Conv2D)              (None, 16, 16, 96)   83040       conv2d_27[0][0]                  

up_sampling2d_4 (UpSampling2D)  (None, 32, 32, 96)   0           conv2d_28[0][0]                  

concatenate_4 (Concatenate)     (None, 32, 32, 144)  0           up_sampling2d_4[0][0]            
                                                                 conv2d_26[0][0]                  
conv2d_29 (Conv2D)              (None, 32, 32, 48)   62256       concatenate_4[0][0]              

conv2d_30 (Conv2D)              (None, 32, 32, 48)   20784       conv2d_29[0][0]                  

up_sampling2d_5 (UpSampling2D)  (None, 64, 64, 48)   0           conv2d_30[0][0]                  

concatenate_5 (Concatenate)     (None, 64, 64, 72)   0           up_sampling2d_5[0][0]            
                                                                 conv2d_24[0][0]                  
conv2d_31 (Conv2D)              (None, 64, 64, 24)   15576       concatenate_5[0][0]              

conv2d_32 (Conv2D)              (None, 64, 64, 24)   5208        conv2d_31[0][0]                  

up_sampling2d_6 (UpSampling2D)  (None, 128, 128, 24) 0           conv2d_32[0][0]                  

concatenate_6 (Concatenate)     (None, 128, 128, 36) 0           up_sampling2d_6[0][0]            
                                                                 conv2d_22[0][0]                  

conv2d_33 (Conv2D)              (None, 128, 128, 12) 3900        concatenate_6[0][0]              

conv2d_34 (Conv2D)              (None, 128, 128, 12) 1308        conv2d_33[0][0]                  

up_sampling2d_7 (UpSampling2D)  (None, 256, 256, 12) 0           conv2d_34[0][0]                  

concatenate_7 (Concatenate)     (None, 256, 256, 18) 0           up_sampling2d_7[0][0]            
                                                                 conv2d_20[0][0]                  
conv2d_35 (Conv2D)              (None, 256, 256, 6)  978         concatenate_7[0][0]              

conv2d_36 (Conv2D)              (None, 256, 256, 6)  330         conv2d_35[0][0]                  

conv2d_37 (Conv2D)              (None, 256, 256, 1)  7           conv2d_36[0][0]                  

Total params: 276,337
Trainable params: 276,337
Non-trainable params: 0

### Next, the model is compiled. 

I used the adam optimizer, binary crossentropy as the loss function and accuracy as a metric.

### Next, the model is trained.

I used 12 epochs with a training batch size of 32.

### Next, I analysed the training history.

This showed how the accuracy and val accuracy changed over time. The plot of the training history is shown below.

...

### Next, I displayed some predictions I made. One such prediciton is shown below.

...

### Next, I computed the dice similarity coefficient.

I computed the minimum dice similarity coefficient, which was ...

I also computed the average dice similarity coefficient, which was ...