import tensorflow as tf

sign = tf.keras.models.load_model('action.h5')

class SignModel:
    def predict(self, results):
        return sign.predict(results)