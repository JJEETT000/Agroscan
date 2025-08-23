import numpy as np
from PIL import Image
import cv2
import tensorflow as tf

class ImageProcessor:
    """Handle image preprocessing for the computer vision models"""
    
    def __init__(self):
        self.target_size = (224, 224)
        self.normalization_mean = [0.485, 0.456, 0.406]  # ImageNet means
        self.normalization_std = [0.229, 0.224, 0.225]   # ImageNet stds
    
    def preprocess_image(self, image):
        """Complete preprocessing pipeline for model input"""
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Resize image
        resized = self.resize_image(image)
        
        # Normalize for model input
        normalized = self.normalize_image(resized)
        
        # Add batch dimension
        preprocessed = np.expand_dims(normalized, axis=0)
        
        return preprocessed
    
    def resize_image(self, image, target_size=None):
        """Resize image to target dimensions while maintaining aspect ratio"""
        if target_size is None:
            target_size = self.target_size
        
        if isinstance(image, Image.Image):
            # Use PIL for high-quality resizing
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            return np.array(image)
        else:
            # Use OpenCV for numpy arrays
            return cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
    
    def normalize_image(self, image):
        """Normalize image for neural network input"""
        # Ensure image is in 0-1 range
        if image.dtype == np.uint8:
            image = image.astype(np.float32) / 255.0
        
        # Apply ImageNet normalization
        normalized = np.zeros_like(image, dtype=np.float32)
        for i in range(3):  # RGB channels
            if len(image.shape) == 3 and image.shape[2] > i:
                normalized[:, :, i] = (image[:, :, i] - self.normalization_mean[i]) / self.normalization_std[i]
        
        return normalized
    
    def denormalize_image(self, image):
        """Reverse normalization for display purposes"""
        denormalized = np.zeros_like(image)
        for i in range(3):
            if len(image.shape) == 3 and image.shape[2] > i:
                denormalized[:, :, i] = image[:, :, i] * self.normalization_std[i] + self.normalization_mean[i]
        
        # Clip to valid range and convert to uint8
        denormalized = np.clip(denormalized * 255, 0, 255).astype(np.uint8)
        return denormalized
    
    def enhance_image_quality(self, image):
        """Enhance image quality for better analysis"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[:, :, 0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        return enhanced
    
    def remove_background(self, image, method='grabcut'):
        """Remove background from crop image"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        if method == 'grabcut':
            return self._grabcut_segmentation(image)
        elif method == 'threshold':
            return self._threshold_segmentation(image)
        else:
            return image  # No background removal
    
    def _grabcut_segmentation(self, image):
        """Use GrabCut algorithm for background removal"""
        # Create mask
        mask = np.zeros(image.shape[:2], np.uint8)
        
        # Define rectangle around the object (assume object is in center 60% of image)
        height, width = image.shape[:2]
        margin_h, margin_w = int(height * 0.2), int(width * 0.2)
        rect = (margin_w, margin_h, width - 2*margin_w, height - 2*margin_h)
        
        # Initialize foreground and background models
        fgdModel = np.zeros((1, 65), np.float64)
        bgdModel = np.zeros((1, 65), np.float64)
        
        try:
            # Apply GrabCut
            cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            
            # Create final mask
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # Apply mask to image
            result = image * mask2[:, :, np.newaxis]
            return result
        except:
            # If GrabCut fails, return original image
            return image
    
    def _threshold_segmentation(self, image):
        """Use simple thresholding for background removal"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply Otsu's thresholding
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations to clean up mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Apply mask
        mask_3channel = cv2.merge([mask, mask, mask]) / 255.0
        result = image * mask_3channel
        
        return result.astype(np.uint8)
    
    def extract_color_histogram(self, image, bins=32):
        """Extract color histogram features"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Calculate histogram for each channel
        hist_features = []
        for i in range(3):  # RGB channels
            hist = cv2.calcHist([image], [i], None, [bins], [0, 256])
            hist = hist.flatten() / hist.sum()  # Normalize
            hist_features.extend(hist)
        
        return np.array(hist_features)
    
    def extract_texture_features(self, image):
        """Extract texture features using Gray-Level Co-occurrence Matrix (GLCM)"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Simple texture measures
        features = {}
        
        # Local Binary Pattern approximation
        features['texture_variance'] = np.var(gray)
        features['texture_mean'] = np.mean(gray)
        
        # Edge density
        edges = cv2.Canny(gray, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / edges.size
        
        # Gradient magnitude
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        features['gradient_mean'] = np.mean(gradient_magnitude)
        features['gradient_std'] = np.std(gradient_magnitude)
        
        return features
    
    def detect_dominant_colors(self, image, k=5):
        """Detect dominant colors using K-means clustering"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Reshape image to list of pixels
        pixels = image.reshape(-1, 3)
        
        # Apply K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(
            pixels.astype(np.float32), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        
        # Calculate color percentages
        unique_labels, counts = np.unique(labels, return_counts=True)
        percentages = counts / len(labels)
        
        # Sort by percentage
        sorted_indices = np.argsort(percentages)[::-1]
        
        dominant_colors = []
        for i in sorted_indices:
            color = centers[unique_labels[i]].astype(int)
            percentage = percentages[i]
            dominant_colors.append({
                'color': color.tolist(),
                'percentage': float(percentage),
                'hex': f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            })
        
        return dominant_colors
    
    def calculate_sharpness(self, image):
        """Calculate image sharpness using Laplacian variance"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = np.var(laplacian)
        
        return sharpness
    
    def adjust_brightness_contrast(self, image, brightness=0, contrast=1.0):
        """Adjust brightness and contrast of image"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Apply brightness and contrast adjustment
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        
        return adjusted
    
    def rotate_image(self, image, angle):
        """Rotate image by specified angle"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        # Get rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
        
        return rotated
    
    def crop_to_object(self, image, padding=20):
        """Crop image to focus on the main object"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to grayscale and threshold
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get bounding box of largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add padding
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            # Crop image
            cropped = image[y:y+h, x:x+w]
            return cropped
        
        return image  # Return original if no contours found
