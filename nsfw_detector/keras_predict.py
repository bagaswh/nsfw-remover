import keras
import cv2
import numpy as np

from PIL import Image


def load_images(images, image_size):
    '''
    Function for loading images into numpy arrays for passing to model.predict
    inputs:
        images: list of image arrays (Numpy array) to load
        image_size: size into which images should be resized

    outputs:images_preds
        loaded_images: loaded images on which keras model can run predictions
        loaded_image_indexes: paths of images which the function is able to process

    '''
    loaded_images = []

    for i, img in enumerate(images):
        image = Image.fromarray(img).convert("RGB")
        image = keras.preprocessing.image.img_to_array(image)
        image = cv2.resize(image, image_size)
        image /= 255
        loaded_images.append(image)

    return np.asarray(loaded_images)


class keras_predictor():
    '''
        Class for loading model and running predictions.
        For example on how to use take a look the if __name__ == '__main__' part.
    '''
    nsfw_model = None

    def __init__(self, model_path):
        '''
            model = keras_predictor('path_to_weights')
        '''
        keras_predictor.nsfw_model = keras.models.load_model(model_path)

    def predict(self, images=[], batch_size=32, image_size=(299, 299), categories=['drawings', 'hentai', 'neutral', 'porn', 'sexy']):
        '''
            inputs:
                images: list of image arrays or can be a string too (for single image)
                batch_size: batch_size for running predictions
                image_size: size to which the image needs to be resized
                categories: since the model predicts numbers, categories is the list of actual names of categories
        '''
        loaded_images = load_images(images, image_size)

        if len(loaded_images) == 0:
            return {}

        model_preds = keras_predictor.nsfw_model.predict(
            loaded_images, batch_size=batch_size)

        preds = np.argsort(model_preds, axis=1).tolist()

        probs = []
        for i, single_preds in enumerate(preds):
            single_probs = []
            for j, pred in enumerate(single_preds):
                single_probs.append(model_preds[i][pred])
                preds[i][j] = categories[pred]

            probs.append(single_probs)

        images_preds = {}

        for _ in range(len(preds[i])):
            images_preds[preds[i][_]] = probs[i][_]

        return images_preds
