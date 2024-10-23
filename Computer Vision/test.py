import numpy as np

image = np.array([[1, 2, 2, 6],
                  [1, 2, 7, 1],
                  [0, 3, 4, 4],
                  [5, 2, 8, 7]])

# Define filters
box_filter = np.ones((3, 3)) / 9
gaussian_filter = np.array([[0, 1/8, 0],
                             [1/8, 4/8, 1/8],
                             [0, 1/8, 0]])
sobel_filter = np.array([[-1, 0, 1],
                          [-2, 0, 2],
                          [-1, 0, 1]])

def apply_filter(image, filter):
    h, w = filter.shape
    responses = []
    for i in range(image.shape[0] - h + 1):
        response_row = []
        for j in range(image.shape[1] - w + 1):
            patch = image[i:i+h, j:j+w]
            response = np.sum(patch * filter)
            response_row.append(response)
        responses.append(response_row)
    return np.array(responses)

# Apply filters
box_response = apply_filter(image, box_filter)
gaussian_response = apply_filter(image, gaussian_filter)
sobel_response = apply_filter(image, sobel_filter)

print("Box Filter Response:\n", box_response)
print("Gaussian Filter Response:\n", gaussian_response)
print("Sobel Filter Response:\n", sobel_response)
