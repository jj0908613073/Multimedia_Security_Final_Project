import numpy as np
import cv2
import matplotlib.pyplot as plt

def lsb_matching(cover_image, message_image, M, N, m, n):
    for i in range(m):
        for j in range(0, min(n * 2, N - 1), 2):  # Adjusted loop bounds
            if (j == n * 2 - 2 or j == n * 2 - 3) and i < m - 1:
                i += 1

            if j + 1 < N and i < M:
                if message_image[i, j] == cover_image[i, j] % 2:
                    if j + 1 < N and i < M and message_image[i, j + 1] != (cover_image[i, j] // 2 + cover_image[i, j + 1]) % 2:
                        if cover_image[i, j + 1] % 2 == 1:
                            cover_image[i, j + 1] -= 1
                        elif cover_image[i, j + 1] % 2 == 0:
                            cover_image[i, j + 1] += 1
                    else:
                        cover_image[i, j + 1] = cover_image[i, j + 1]
                    cover_image[i, j] = cover_image[i, j]
                elif j + 1 < N and i < M and message_image[i, j] != cover_image[i, j] % 2:
                    if j + 1 < N and i < M and message_image[i, j + 1] == (cover_image[i, j] // 2 - 1 + cover_image[i, j + 1]) % 2:
                        cover_image[i, j] -= 1
                    else:
                        cover_image[i, j] += 1
                    cover_image[i, j + 1] = cover_image[i, j + 1]

    return cover_image

# Load images with error handling
cover_image = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
if cover_image is None:
    print("Error: Unable to load cover image.")
    exit()

message_image = cv2.imread('airplane.bmp', cv2.IMREAD_GRAYSCALE)
if message_image is None:
    print("Error: Unable to load message image.")
    exit()

_, message_image = cv2.threshold(message_image, 128, 255, cv2.THRESH_BINARY)

# Get image dimensions
M, N = cover_image.shape
m, n = message_image.shape

# Apply LSB matching algorithm
hide_image = lsb_matching(cover_image.astype(float), message_image.astype(float), M, N, m, n)
# Save the hidden image
cv2.imwrite('hidden_image.bmp', hide_image.astype(np.uint8))

# Display images
plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1), plt.imshow(cover_image, cmap='gray'), plt.title('Cover Image')
plt.subplot(1, 3, 2), plt.imshow(message_image, cmap='gray'), plt.title('Message Image')
plt.subplot(1, 3, 3), plt.imshow(hide_image, cmap='gray'), plt.title('Hidden Image')
plt.show()

# Calculate metrics
B = 8  # Number of bits used to encode one pixel
MAX = 2 ** B - 1  # Maximum grayscale level
MES = np.sum((cover_image - hide_image) ** 2) / (M * N)  # Mean Squared Error
PSNR = 20 * np.log10(MAX / np.sqrt(MES))  # Peak Signal-to-Noise Ratio
print(f'Peak Signal-to-Noise Ratio: {PSNR:.2f} dB')
