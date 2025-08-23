import numpy as np
from PIL import Image
import cv2

class QualityAssessor:
    """Assess the quality of crops (fresh vs spoiled)"""
    
    def __init__(self):
        self.spoilage_indicators = {
            'corn': ['brown_spots', 'mold_growth', 'kernel_damage', 'color_change'],
            'yam': ['soft_spots', 'dark_patches', 'sprouting', 'surface_damage'],
            'cassava': ['black_spots', 'soft_rot', 'fiber_separation', 'discoloration'],
            'tomato': ['wrinkles', 'soft_spots', 'color_changes', 'mold_spots']
        }
    
    def assess_quality(self, image, crop_type):
        """Assess the quality of the given crop image"""
        try:
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # Validate input
            if image is None or image.size == 0:
                return self._get_default_result()
            
            # Extract various quality indicators efficiently
            color_analysis = self._analyze_color_degradation(image, crop_type)
            texture_analysis = self._analyze_texture_degradation(image, crop_type)
            shape_analysis = self._analyze_shape_degradation(image, crop_type)
            surface_analysis = self._analyze_surface_condition(image, crop_type)
            
            # Combine all indicators
            spoilage_score = self._calculate_spoilage_score(
                color_analysis, texture_analysis, shape_analysis, surface_analysis, crop_type
            )
            
            # Determine quality status
            if spoilage_score < 0.3:
                status = 'fresh'
                confidence = 1.0 - spoilage_score
            else:
                status = 'spoiled'
                confidence = spoilage_score
        
            return {
                'status': status,
                'confidence': min(confidence, 0.95),  # Cap confidence at 95%
                'spoilage_score': spoilage_score,
                'indicators': {
                    'color': color_analysis,
                    'texture': texture_analysis,
                    'shape': shape_analysis,
                    'surface': surface_analysis
                }
            }
        
        except Exception:
            return self._get_default_result()
    
    def _get_default_result(self):
        """Return default quality assessment result"""
        return {
            'status': 'unknown',
            'confidence': 0.5,
            'spoilage_score': 0.5,
            'indicators': {
                'color': 0.5,
                'texture': 0.5,
                'shape': 0.5,
                'surface': 0.5
            }
        }
    
    def _analyze_color_degradation(self, image, crop_type):
        """Analyze color changes that indicate spoilage"""
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        
        degradation_score = 0.0
        
        if crop_type == 'corn':
            # Look for brown/black spots on yellow kernels
            brown_spots = self._detect_brown_spots(hsv_image)
            degradation_score += brown_spots * 0.7
            
            # Check for overall color dullness
            yellow_vibrancy = self._calculate_yellow_vibrancy(hsv_image)
            degradation_score += (1.0 - yellow_vibrancy) * 0.3
            
        elif crop_type == 'tomato':
            # Look for overripe/underripe indicators
            red_quality = self._assess_tomato_red_quality(hsv_image)
            degradation_score += (1.0 - red_quality) * 0.6
            
            # Check for dark spots
            dark_spots = self._detect_dark_spots(hsv_image)
            degradation_score += dark_spots * 0.4
            
        elif crop_type == 'yam':
            # Look for dark patches on brown surface
            dark_patches = self._detect_dark_patches(hsv_image)
            degradation_score += dark_patches * 0.8
            
            # Check for abnormal color variations
            color_uniformity = self._calculate_color_uniformity(hsv_image)
            degradation_score += (1.0 - color_uniformity) * 0.2
            
        elif crop_type == 'cassava':
            # Look for black spots
            black_spots = self._detect_black_spots(hsv_image)
            degradation_score += black_spots * 0.7
            
            # Check for discoloration from white
            white_purity = self._assess_white_purity(hsv_image)
            degradation_score += (1.0 - white_purity) * 0.3
        
        return min(degradation_score, 1.0)
    
    def _analyze_texture_degradation(self, image, crop_type):
        """Analyze texture changes that indicate spoilage"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate texture features
        texture_variance = np.var(gray)
        texture_mean = np.mean(gray)
        
        # Edge detection for surface roughness
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        degradation_score = 0.0
        
        if crop_type == 'corn':
            # Corn should have regular kernel pattern
            # Irregular texture indicates damage
            expected_variance = 800  # Typical for healthy corn
            variance_deviation = abs(texture_variance - expected_variance) / expected_variance
            degradation_score += min(float(variance_deviation), 1.0) * 0.6
            
        elif crop_type == 'tomato':
            # Tomato should have smooth skin
            # High edge density indicates wrinkles/damage
            degradation_score += min(edge_density * 5, 1.0) * 0.7
            
        elif crop_type == 'yam':
            # Yam naturally has rough texture, but excessive roughness indicates damage
            if edge_density > 0.15:  # Threshold for excessive roughness
                degradation_score += (edge_density - 0.15) * 3
            
        elif crop_type == 'cassava':
            # Cassava should have relatively smooth cut surface
            degradation_score += min(edge_density * 4, 1.0) * 0.6
        
        return min(degradation_score, 1.0)
    
    def _analyze_shape_degradation(self, image, crop_type):
        """Analyze shape deformations that indicate spoilage"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Find contours
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0.5  # Default score if no contours found
        
        # Get largest contour (main object)
        main_contour = max(contours, key=cv2.contourArea)
        
        degradation_score = 0.0
        
        # Calculate shape regularity
        area = cv2.contourArea(main_contour)
        perimeter = cv2.arcLength(main_contour, True)
        
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if crop_type == 'tomato':
                # Tomatoes should be relatively circular
                expected_circularity = 0.7
                circularity_deviation = abs(circularity - expected_circularity)
                degradation_score += circularity_deviation * 0.5
                
            elif crop_type in ['corn', 'yam', 'cassava']:
                # These crops can have more irregular shapes naturally
                # Extreme irregularity indicates damage
                if circularity < 0.2:  # Very irregular
                    degradation_score += (0.2 - circularity) * 2
        
        return min(degradation_score, 1.0)
    
    def _analyze_surface_condition(self, image, crop_type):
        """Analyze surface condition for signs of spoilage"""
        # Convert to different color spaces for analysis
        lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        degradation_score = 0.0
        
        # Detect potential mold growth (greenish or bluish spots)
        mold_score = self._detect_mold_growth(hsv_image)
        degradation_score += mold_score * 0.8
        
        # Detect soft spots (areas with different lighting/texture)
        soft_spots = self._detect_soft_spots(lab_image)
        degradation_score += soft_spots * 0.6
        
        # Detect surface damage (scratches, cuts, bruises)
        surface_damage = self._detect_surface_damage(image)
        degradation_score += surface_damage * 0.4
        
        return min(degradation_score, 1.0)
    
    def _calculate_spoilage_score(self, color, texture, shape, surface, crop_type):
        """Calculate overall spoilage score from individual indicators"""
        # Weight different factors based on crop type
        weights = {
            'corn': {'color': 0.4, 'texture': 0.3, 'shape': 0.1, 'surface': 0.2},
            'tomato': {'color': 0.3, 'texture': 0.2, 'shape': 0.2, 'surface': 0.3},
            'yam': {'color': 0.4, 'texture': 0.2, 'shape': 0.1, 'surface': 0.3},
            'cassava': {'color': 0.4, 'texture': 0.2, 'shape': 0.1, 'surface': 0.3}
        }
        
        crop_weights = weights.get(crop_type, weights['corn'])
        
        spoilage_score = (
            color * crop_weights['color'] +
            texture * crop_weights['texture'] +
            shape * crop_weights['shape'] +
            surface * crop_weights['surface']
        )
        
        return min(spoilage_score, 1.0)
    
    # Helper methods for specific detection algorithms
    def _detect_brown_spots(self, hsv_image):
        """Detect brown spots in the image"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        brown_mask = ((h >= 10) & (h <= 25)) & (s > 30) & (v < 150)
        return np.mean(brown_mask)
    
    def _detect_dark_spots(self, hsv_image):
        """Detect dark spots in the image"""
        v = hsv_image[:,:,2]
        dark_mask = v < 50
        return np.mean(dark_mask)
    
    def _detect_black_spots(self, hsv_image):
        """Detect black spots in the image"""
        v = hsv_image[:,:,2]
        black_mask = v < 30
        return np.mean(black_mask)
    
    def _detect_dark_patches(self, hsv_image):
        """Detect dark patches in the image"""
        v = hsv_image[:,:,2]
        mean_brightness = np.mean(v)
        dark_threshold = mean_brightness * 0.5
        dark_mask = v < dark_threshold
        return np.mean(dark_mask)
    
    def _calculate_yellow_vibrancy(self, hsv_image):
        """Calculate the vibrancy of yellow color"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        yellow_mask = ((h >= 20) & (h <= 35)) & (s > 50) & (v > 100)
        if np.any(yellow_mask):
            return np.mean(s[yellow_mask]) / 255.0
        return 0.0
    
    def _assess_tomato_red_quality(self, hsv_image):
        """Assess the quality of red color in tomatoes"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        red_mask = ((h <= 10) | (h >= 170)) & (s > 50) & (v > 100)
        if np.any(red_mask):
            return np.mean(s[red_mask] * v[red_mask]) / (255.0 * 255.0)
        return 0.0
    
    def _calculate_color_uniformity(self, hsv_image):
        """Calculate color uniformity across the image"""
        h = hsv_image[:,:,0]
        return 1.0 - (np.std(h) / 180.0)  # Normalize by max hue value
    
    def _assess_white_purity(self, hsv_image):
        """Assess the purity of white color"""
        s = hsv_image[:,:,1]
        v = hsv_image[:,:,2]
        white_mask = (s < 30) & (v > 200)
        return np.mean(white_mask)
    
    def _detect_mold_growth(self, hsv_image):
        """Detect potential mold growth (greenish/bluish spots)"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        mold_mask = ((h >= 40) & (h <= 140)) & (s > 30) & (v > 30)
        return np.mean(mold_mask)
    
    def _detect_soft_spots(self, lab_image):
        """Detect soft spots using L*a*b* color space"""
        l_channel = lab_image[:,:,0]
        # Soft spots often have different lightness
        mean_lightness = np.mean(l_channel)
        deviation = np.abs(l_channel - mean_lightness)
        soft_spots = deviation > (np.std(l_channel) * 2)
        return np.mean(soft_spots)
    
    def _detect_surface_damage(self, image):
        """Detect surface damage like scratches and cuts"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Look for long straight lines (scratches) or sharp edges (cuts)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        
        if lines is not None:
            return min(len(lines) / 50.0, 1.0)  # Normalize by expected number
        return 0.0
