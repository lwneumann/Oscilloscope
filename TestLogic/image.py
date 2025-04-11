import cv2
import numpy as np


class ImgPath:
    def __init__(self, img_path, output_point_count=5000):
        self.path = generate_image_path(img_path, output_point_count)
        return

    def get_path(self):
        return self.path


def generate_image_path(image_path, output_point_count=5000):
    # Load image and convert to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Resize for simplicity (also going down to [-1, 1] anyway)
    img = cv2.resize(img, (512, 512))

    # Edge detection
    edges = cv2.Canny(img, 100, 200)

    # Find contours (openCV returns a list of point lists)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = list(contours)

    # Resample points within each contour
    def resample_contour(points, n_samples):
        cumdist = np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))
        cumdist = np.insert(cumdist, 0, 0)
        even_distances = np.linspace(0, cumdist[-1], n_samples)
        new_points = np.zeros((n_samples, 2))
        for i, d in enumerate(even_distances):
            idx = np.searchsorted(cumdist, d)
            if idx == 0:
                new_points[i] = points[0]
            else:
                alpha = (d - cumdist[idx-1]) / (cumdist[idx] - cumdist[idx-1])
                new_points[i] = (1 - alpha) * points[idx-1] + alpha * points[idx]
        return new_points

    # Resample each contour and combine them
    path_points = []
    total_points = 0
    for contour in contours:
        contour = contour[:, 0, :]  # Remove nested structure
        n_samples = max(1, int(output_point_count * len(contour) / sum(len(c) for c in contours)))
        resampled_contour = resample_contour(contour, n_samples)
        path_points.extend(resampled_contour)
        total_points += n_samples

    path_points = np.array(path_points, dtype=np.float32)

    # Normalize to [-1, 1] for oscilloscope input
    path_points -= np.min(path_points, axis=0)
    # scale to [0, 1]
    path_points /= np.ptp(path_points, axis=0)
    # scale to [-1, 1]
    path_points = path_points * 2 - 1

    return path_points.tolist()
