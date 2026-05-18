import * as tf from '@tensorflow/tfjs';

// Global variables for lightweight frame differencing (motion detection)
let previousTensor: tf.Tensor3D | null = null;
let isTfInitialized = false;

// Initialize tfjs
async function initTf() {
  if (!isTfInitialized) {
    await tf.ready();
    isTfInitialized = true;
  }
}

/**
 * Processes a video frame using TensorFlow.js to detect movement/activity.
 * Uses a lightweight frame-differencing algorithm suitable for old phones.
 */
export async function processFrame(videoElement: HTMLVideoElement): Promise<number | null> {
  await initTf();

  try {
    return tf.tidy(() => {
      // 1. Get current frame as tensor
      const currentTensor = tf.browser.fromPixels(videoElement);

      // 2. Convert to grayscale and resize for performance
      const grayTensor = currentTensor.mean(2).expandDims(2) as tf.Tensor3D;
      const resizedTensor = tf.image.resizeBilinear(grayTensor, [64, 64]);

      // 3. Calculate difference from previous frame if it exists
      let score = 0;
      if (previousTensor !== null) {
        // Absolute difference between current and previous frame
        const diff = tf.abs(tf.sub(resizedTensor, previousTensor));

        // Thresholding to ignore small noise (e.g. slight lighting changes)
        const thresholded = tf.greater(diff, tf.scalar(20)).toFloat();

        // Sum up the changed pixels and normalize
        const sumChanges = tf.sum(thresholded).dataSync()[0];
        const totalPixels = 64 * 64;

        score = sumChanges / totalPixels;
      }

      // 4. Cleanup old tensor and keep new one for next frame
      if (previousTensor) {
        previousTensor.dispose();
      }

      // We must use tf.keep() to prevent tidy from cleaning it up
      previousTensor = tf.keep(resizedTensor.clone());

      return score;
    });
  } catch (error) {
    console.error("Error processing AI frame:", error);
    return null;
  }
}
