import numpy as np
from PIL import Image
import cv2

class DiseaseDetector:
    """Detect specific diseases and spoilage types in crops"""
    
    def __init__(self):
        self.disease_patterns = {
            'corn': {
                'fungal_infection': {
                    'color_patterns': ['gray_spots', 'black_mold'],
                    'texture_patterns': ['fuzzy_growth', 'irregular_surface'],
                    'severity_indicators': ['spot_coverage', 'color_intensity']
                },
                'bacterial_rot': {
                    'color_patterns': ['brown_discoloration', 'yellow_edges'],
                    'texture_patterns': ['soft_kernels', 'liquid_discharge'],
                    'severity_indicators': ['affected_area', 'color_depth']
                },
                'pest_damage': {
                    'color_patterns': ['holes', 'chewed_kernels'],
                    'texture_patterns': ['irregular_holes', 'damaged_surface'],
                    'severity_indicators': ['hole_count', 'damage_extent']
                },
                'overripeness': {
                    'color_patterns': ['dark_kernels', 'brown_patches'],
                    'texture_patterns': ['dried_surface', 'hardened_kernels'],
                    'severity_indicators': ['dryness_level', 'color_change']
                }
            },
            'tomato': {
                'fungal_infection': {
                    'color_patterns': ['gray_mold', 'white_fuzzy_spots'],
                    'texture_patterns': ['fuzzy_growth', 'soft_spots'],
                    'severity_indicators': ['mold_coverage', 'softness_degree']
                },
                'bacterial_rot': {
                    'color_patterns': ['dark_spots', 'black_patches'],
                    'texture_patterns': ['liquid_spots', 'soft_areas'],
                    'severity_indicators': ['spot_size', 'liquid_amount']
                },
                'overripeness': {
                    'color_patterns': ['deep_red', 'brown_patches'],
                    'texture_patterns': ['soft_skin', 'wrinkled_surface'],
                    'severity_indicators': ['softness', 'wrinkling']
                },
                'blossom_end_rot': {
                    'color_patterns': ['black_bottom', 'dark_circular_spot'],
                    'texture_patterns': ['sunken_area', 'hardened_spot'],
                    'severity_indicators': ['spot_diameter', 'depth']
                }
            },
            'yam': {
                'fungal_infection': {
                    'color_patterns': ['white_mold', 'gray_spots'],
                    'texture_patterns': ['fuzzy_surface', 'soft_spots'],
                    'severity_indicators': ['mold_extent', 'softness']
                },
                'bacterial_rot': {
                    'color_patterns': ['dark_patches', 'black_spots'],
                    'texture_patterns': ['soft_areas', 'liquid_discharge'],
                    'severity_indicators': ['patch_size', 'softness_degree']
                },
                'storage_rot': {
                    'color_patterns': ['brown_discoloration', 'dark_areas'],
                    'texture_patterns': ['soft_flesh', 'collapsed_areas'],
                    'severity_indicators': ['discoloration_extent', 'firmness_loss']
                },
                'sprouting': {
                    'color_patterns': ['green_shoots', 'white_roots'],
                    'texture_patterns': ['protruding_growth', 'bumpy_surface'],
                    'severity_indicators': ['sprout_length', 'number_of_sprouts']
                }
            },
            'cassava': {
                'fungal_infection': {
                    'color_patterns': ['black_spots', 'gray_mold'],
                    'texture_patterns': ['fuzzy_growth', 'soft_areas'],
                    'severity_indicators': ['spot_coverage', 'mold_density']
                },
                'bacterial_rot': {
                    'color_patterns': ['brown_streaks', 'dark_discoloration'],
                    'texture_patterns': ['soft_flesh', 'watery_areas'],
                    'severity_indicators': ['streak_length', 'softness']
                },
                'storage_deterioration': {
                    'color_patterns': ['blue_discoloration', 'brown_lines'],
                    'texture_patterns': ['fiber_separation', 'tough_areas'],
                    'severity_indicators': ['discoloration_depth', 'fiber_damage']
                },
                'pest_damage': {
                    'color_patterns': ['holes', 'chewed_areas'],
                    'texture_patterns': ['tunnel_patterns', 'irregular_holes'],
                    'severity_indicators': ['hole_density', 'tunnel_extent']
                }
            }
        }
    
    def detect_disease(self, image, crop_type):
        """Detect specific disease type and severity"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        if crop_type not in self.disease_patterns:
            return {
                'disease_type': 'unknown_spoilage',
                'confidence': 0.5,
                'severity': 'moderate',
                'description': 'Spoilage detected but specific type could not be determined'
            }
        
        # Analyze image for each possible disease
        disease_scores = {}
        crop_diseases = self.disease_patterns[crop_type]
        
        for disease_name, patterns in crop_diseases.items():
            score = self._analyze_disease_pattern(image, patterns, crop_type)
            disease_scores[disease_name] = score
        
        # Find most likely disease
        most_likely_disease = max(disease_scores, key=disease_scores.get)
        max_score = disease_scores[most_likely_disease]
        
        # Determine severity
        severity = self._determine_severity(image, most_likely_disease, crop_type, max_score)
        
        # Get description
        description = self._get_disease_description(most_likely_disease, crop_type)
        
        return {
            'disease_type': most_likely_disease,
            'confidence': min(max_score, 0.95),
            'severity': severity,
            'description': description,
            'all_scores': disease_scores
        }
    
    def _analyze_disease_pattern(self, image, patterns, crop_type):
        """Analyze image for specific disease patterns"""
        color_score = self._analyze_color_patterns(image, patterns['color_patterns'])
        texture_score = self._analyze_texture_patterns(image, patterns['texture_patterns'])
        
        # Weighted combination
        total_score = 0.6 * color_score + 0.4 * texture_score
        
        return total_score
    
    def _analyze_color_patterns(self, image, color_patterns):
        """Analyze color patterns associated with disease"""
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        
        pattern_score = 0.0
        
        for pattern in color_patterns:
            if pattern == 'gray_spots':
                pattern_score += self._detect_gray_spots(hsv_image) * 0.3
            elif pattern == 'black_mold':
                pattern_score += self._detect_black_mold(hsv_image) * 0.4
            elif pattern == 'brown_discoloration':
                pattern_score += self._detect_brown_discoloration(hsv_image) * 0.3
            elif pattern == 'yellow_edges':
                pattern_score += self._detect_yellow_edges(hsv_image) * 0.2
            elif pattern == 'holes':
                pattern_score += self._detect_holes(image) * 0.5
            elif pattern == 'white_fuzzy_spots':
                pattern_score += self._detect_white_fuzzy_spots(hsv_image) * 0.4
            elif pattern == 'dark_spots':
                pattern_score += self._detect_dark_spots(hsv_image) * 0.3
            elif pattern == 'deep_red':
                pattern_score += self._detect_deep_red(hsv_image) * 0.2
            elif pattern == 'black_bottom':
                pattern_score += self._detect_black_bottom(hsv_image) * 0.5
            elif pattern == 'white_mold':
                pattern_score += self._detect_white_mold(hsv_image) * 0.4
            elif pattern == 'green_shoots':
                pattern_score += self._detect_green_shoots(hsv_image) * 0.6
            elif pattern == 'blue_discoloration':
                pattern_score += self._detect_blue_discoloration(lab_image) * 0.4
            elif pattern == 'brown_streaks':
                pattern_score += self._detect_brown_streaks(hsv_image) * 0.3
        
        return min(pattern_score, 1.0)
    
    def _analyze_texture_patterns(self, image, texture_patterns):
        """Analyze texture patterns associated with disease"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        pattern_score = 0.0
        
        for pattern in texture_patterns:
            if pattern == 'fuzzy_growth':
                pattern_score += self._detect_fuzzy_growth(gray) * 0.4
            elif pattern == 'irregular_surface':
                pattern_score += self._detect_irregular_surface(gray) * 0.2
            elif pattern == 'soft_kernels':
                pattern_score += self._detect_soft_kernels(gray) * 0.3
            elif pattern == 'liquid_discharge':
                pattern_score += self._detect_liquid_discharge(image) * 0.5
            elif pattern == 'irregular_holes':
                pattern_score += self._detect_irregular_holes(gray) * 0.4
            elif pattern == 'soft_spots':
                pattern_score += self._detect_soft_spots(gray) * 0.3
            elif pattern == 'wrinkled_surface':
                pattern_score += self._detect_wrinkled_surface(gray) * 0.3
            elif pattern == 'sunken_area':
                pattern_score += self._detect_sunken_area(gray) * 0.4
            elif pattern == 'protruding_growth':
                pattern_score += self._detect_protruding_growth(gray) * 0.5
            elif pattern == 'fiber_separation':
                pattern_score += self._detect_fiber_separation(gray) * 0.3
            elif pattern == 'tunnel_patterns':
                pattern_score += self._detect_tunnel_patterns(gray) * 0.4
        
        return min(pattern_score, 1.0)
    
    def _determine_severity(self, image, disease_type, crop_type, confidence_score):
        """Determine the severity of the detected disease"""
        # Base severity on confidence score and additional analysis
        if confidence_score < 0.3:
            return 'mild'
        elif confidence_score < 0.6:
            return 'moderate'
        elif confidence_score < 0.8:
            return 'severe'
        else:
            return 'critical'
    
    def _get_disease_description(self, disease_type, crop_type):
        """Get human-readable description of the disease"""
        descriptions = {
            'fungal_infection': f'Fungal infection detected on {crop_type}. Characterized by mold growth and discoloration.',
            'bacterial_rot': f'Bacterial rot affecting {crop_type}. Shows soft spots and discoloration.',
            'pest_damage': f'Pest damage visible on {crop_type}. Shows holes and chewed areas.',
            'overripeness': f'{crop_type.title()} is overripe. Shows color changes and texture deterioration.',
            'blossom_end_rot': 'Blossom end rot in tomato. Dark spot at blossom end due to calcium deficiency.',
            'storage_rot': f'Storage rot in {crop_type}. Deterioration due to improper storage conditions.',
            'sprouting': f'Sprouting detected in {crop_type}. New growth indicating storage issues.',
            'storage_deterioration': f'Storage deterioration in {crop_type}. Quality loss due to storage conditions.'
        }
        
        return descriptions.get(disease_type, f'Unspecified spoilage detected in {crop_type}.')
    
    # Detection methods for specific patterns
    def _detect_gray_spots(self, hsv_image):
        """Detect gray spots in the image"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        gray_mask = (s < 50) & (v >= 50) & (v <= 150)
        return np.mean(gray_mask)
    
    def _detect_black_mold(self, hsv_image):
        """Detect black mold growth"""
        v = hsv_image[:,:,2]
        black_mask = v < 40
        return np.mean(black_mask)
    
    def _detect_brown_discoloration(self, hsv_image):
        """Detect brown discoloration"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        brown_mask = ((h >= 10) & (h <= 25)) & (s > 30) & (v < 120)
        return np.mean(brown_mask)
    
    def _detect_yellow_edges(self, hsv_image):
        """Detect yellow edges or borders"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        yellow_mask = ((h >= 20) & (h <= 35)) & (s > 50) & (v > 100)
        
        # Check if yellow areas are near edges
        gray = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Dilate edges to create edge regions
        kernel = np.ones((5,5), np.uint8)
        edge_regions = cv2.dilate(edges, kernel, iterations=1)
        
        # Check overlap between yellow areas and edge regions
        overlap = yellow_mask & (edge_regions > 0)
        return np.mean(overlap)
    
    def _detect_holes(self, image):
        """Detect holes in the crop"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Use adaptive threshold to find dark regions
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Find contours of dark regions
        contours, _ = cv2.findContours(255 - thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Count circular/hole-like contours
        hole_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Minimum hole size
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.5:  # Reasonably circular
                        hole_count += 1
        
        return min(hole_count / 10.0, 1.0)  # Normalize
    
    def _detect_white_fuzzy_spots(self, hsv_image):
        """Detect white fuzzy spots (mold)"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        white_mask = (s < 30) & (v > 200)
        
        # Check for texture variation in white areas (fuzziness)
        gray = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2GRAY)
        
        # Calculate local standard deviation
        kernel = np.ones((5,5), np.float32) / 25
        mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
        sqr_mean = cv2.filter2D((gray.astype(np.float32))**2, -1, kernel)
        variance = sqr_mean - mean**2
        
        # High variance in white areas indicates fuzziness
        fuzzy_white = white_mask & (variance > np.percentile(variance, 70))
        return np.mean(fuzzy_white)
    
    def _detect_dark_spots(self, hsv_image):
        """Detect dark spots"""
        v = hsv_image[:,:,2]
        dark_mask = v < 60
        return np.mean(dark_mask)
    
    def _detect_deep_red(self, hsv_image):
        """Detect deep red coloration (overripe tomatoes)"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        deep_red_mask = ((h <= 5) | (h >= 175)) & (s > 100) & (v < 150)
        return np.mean(deep_red_mask)
    
    def _detect_black_bottom(self, hsv_image):
        """Detect black spots at bottom (blossom end rot)"""
        v = hsv_image[:,:,2]
        height = v.shape[0]
        
        # Focus on bottom third of image
        bottom_region = v[int(2*height/3):, :]
        black_mask = bottom_region < 40
        
        return np.mean(black_mask)
    
    def _detect_white_mold(self, hsv_image):
        """Detect white mold growth"""
        return self._detect_white_fuzzy_spots(hsv_image)
    
    def _detect_green_shoots(self, hsv_image):
        """Detect green shoots (sprouting)"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        green_mask = ((h >= 40) & (h <= 80)) & (s > 50) & (v > 50)
        return np.mean(green_mask)
    
    def _detect_blue_discoloration(self, lab_image):
        """Detect blue discoloration in LAB color space"""
        b_channel = lab_image[:,:,2]
        # Blue in LAB space has low b* values
        blue_mask = b_channel < 120  # Typical blue threshold in LAB
        return np.mean(blue_mask)
    
    def _detect_brown_streaks(self, hsv_image):
        """Detect brown streaks or lines"""
        h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
        brown_mask = ((h >= 10) & (h <= 25)) & (s > 30) & (v < 120)
        
        # Use morphological operations to detect line-like structures
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))  # Vertical lines
        vertical_lines = cv2.morphologyEx(brown_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))  # Horizontal lines
        horizontal_lines = cv2.morphologyEx(brown_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
        
        streaks = vertical_lines | horizontal_lines
        return np.mean(streaks)
    
    def _detect_fuzzy_growth(self, gray):
        """Detect fuzzy texture growth"""
        # Use Laplacian to detect texture variation
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = np.var(laplacian)
        
        # High variance indicates fuzzy texture
        return min(variance / 1000.0, 1.0)  # Normalize
    
    def _detect_irregular_surface(self, gray):
        """Detect irregular surface texture"""
        # Use sobel gradients to detect surface irregularities
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        irregularity = np.std(magnitude) / np.mean(magnitude) if np.mean(magnitude) > 0 else 0
        return min(irregularity / 2.0, 1.0)  # Normalize
    
    def _detect_soft_kernels(self, gray):
        """Detect soft kernels (corn specific)"""
        # Soft kernels have less defined edges
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Low edge density indicates soft/mushy kernels
        return max(0, 1.0 - edge_density * 10)
    
    def _detect_liquid_discharge(self, image):
        """Detect areas with liquid discharge"""
        # Convert to HSV and look for areas with high saturation and brightness
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        s, v = hsv[:,:,1], hsv[:,:,2]
        
        # Liquid areas often have high saturation and reflectivity
        liquid_mask = (s > 100) & (v > 200)
        return np.mean(liquid_mask)
    
    def _detect_irregular_holes(self, gray):
        """Detect irregular holes"""
        holes_score = self._detect_holes(gray)  # Reuse hole detection
        
        # Additional check for irregularity
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(255 - thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        irregular_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity < 0.3:  # Very irregular
                        irregular_count += 1
        
        irregularity = min(irregular_count / 5.0, 1.0)
        return holes_score * irregularity
    
    def _detect_soft_spots(self, gray):
        """Detect soft spots based on texture analysis"""
        # Soft spots have different texture than surrounding areas
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        difference = np.abs(gray.astype(np.float32) - blur.astype(np.float32))
        
        # Areas with low difference are likely soft spots
        soft_mask = difference < np.percentile(difference, 20)
        return np.mean(soft_mask)
    
    def _detect_wrinkled_surface(self, gray):
        """Detect wrinkled surface texture"""
        # Wrinkles create fine line patterns
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # High gradient magnitude indicates wrinkles
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        wrinkle_score = np.mean(magnitude > np.percentile(magnitude, 80))
        
        return wrinkle_score
    
    def _detect_sunken_area(self, gray):
        """Detect sunken areas using brightness analysis"""
        # Sunken areas are typically darker
        mean_brightness = np.mean(gray)
        sunken_mask = gray < (mean_brightness * 0.7)
        
        # Check if sunken areas form coherent regions
        kernel = np.ones((5,5), np.uint8)
        closed = cv2.morphologyEx(sunken_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
        
        return np.mean(closed)
    
    def _detect_protruding_growth(self, gray):
        """Detect protruding growth (sprouts)"""
        # Protruding areas are typically brighter and have distinct edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Look for bright areas with strong edges
        bright_mask = gray > np.percentile(gray, 80)
        
        # Dilate edges to create edge regions
        kernel = np.ones((3,3), np.uint8)
        edge_regions = cv2.dilate(edges, kernel, iterations=1)
        
        # Overlap between bright areas and edge regions
        protrusion_mask = bright_mask & (edge_regions > 0)
        return np.mean(protrusion_mask)
    
    def _detect_fiber_separation(self, gray):
        """Detect fiber separation in cassava"""
        # Fiber separation creates linear patterns
        # Use morphological operations to detect line structures
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 9))
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_v)
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_h)
        
        lines = vertical_lines | horizontal_lines
        return np.mean(lines > 0)
    
    def _detect_tunnel_patterns(self, gray):
        """Detect tunnel patterns from pest damage"""
        # Tunnels create connected dark regions
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Find connected components
        contours, _ = cv2.findContours(255 - thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tunnel_score = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum tunnel size
                # Check aspect ratio for tunnel-like shapes
                rect = cv2.minAreaRect(contour)
                width, height = rect[1]
                if width > 0 and height > 0:
                    aspect_ratio = max(width/height, height/width)
                    if aspect_ratio > 3:  # Long and narrow (tunnel-like)
                        tunnel_score += 1
        
        return min(tunnel_score / 5.0, 1.0)  # Normalize
