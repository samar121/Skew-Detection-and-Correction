import cv2
import numpy as np

def detect_skew(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve HoughLines accuracy
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use HoughLines to detect lines in the image
    lines = cv2.HoughLines(blurred, 1, np.pi / 180, 100)

    # Find the angle of the most prominent line
    if lines is not None:
        angles = []
        for line in lines:
            for rho, theta in line:
                angle = theta * 90 / np.pi
                angles.append(angle)
        skew_angle = np.median(angles)
        return skew_angle
    else:
        return 0  # If no lines are detected, assume no skew

def correct_skew(image, skew_angle):
    # Rotate the image to correct skew
    rows, cols, _ = image.shape
    M = cv2.getRotationMatrix2D((cols // 2, rows // 2), skew_angle, 1)
    corrected_image = cv2.warpAffine(image, M, (cols, rows), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    return corrected_image

# Example usage
image_path = "1.jpg"  # Replace with the actual path to your image
original_image = cv2.imread(image_path)

# Detect skew angle
skew_angle = detect_skew(original_image)
print(f"Detected skew angle: {skew_angle} degrees")

# Correct skew
corrected_image = correct_skew(original_image, skew_angle)

# Display the results
cv2.imshow("Original Image", original_image)
cv2.imshow("Corrected Image", corrected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
