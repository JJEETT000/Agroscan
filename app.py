import streamlit as st
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from models.crop_classifier import CropClassifier
from models.quality_assessor import QualityAssessor
from models.disease_detector import DiseaseDetector
from utils.image_processor import ImageProcessor
from utils.treatment_database import TreatmentDatabase

# Initialize components
@st.cache_resource
def load_models():
    """Load all models and initialize components"""
    crop_classifier = CropClassifier()
    quality_assessor = QualityAssessor()
    disease_detector = DiseaseDetector()
    image_processor = ImageProcessor()
    treatment_db = TreatmentDatabase()
    
    return crop_classifier, quality_assessor, disease_detector, image_processor, treatment_db

def main():
    st.set_page_config(
        page_title="Agricultural Computer Vision System",
        page_icon="🌾",
        layout="wide"
    )
    
    st.title("🌾 Agricultural Computer Vision System")
    st.markdown("Upload an image of crops (corn, yam, cassava, or tomato) to get AI-powered analysis and treatment recommendations.")
    
    # Load models
    crop_classifier, quality_assessor, disease_detector, image_processor, treatment_db = load_models()
    
    # Sidebar for system information
    with st.sidebar:
        st.header("System Information")
        st.markdown("""
        **Supported Crops:**
        - 🌽 Corn
        - 🍠 Yam
        - 🥔 Cassava
        - 🍅 Tomato
        
        **Analysis Features:**
        - Crop identification
        - Quality assessment
        - Disease detection
        - Treatment recommendations
        """)
        
        st.header("Analysis Settings")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
        show_preprocessing = st.checkbox("Show image preprocessing steps", False)
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Image Upload")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of corn, yam, cassava, or tomato"
        )
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_container_width=True)
            
            # Image preprocessing
            processed_image = image_processor.preprocess_image(image)  # For neural network
            resized_image = image_processor.resize_image(image)  # For quality/disease analysis
            
            if show_preprocessing:
                st.subheader("Preprocessing Steps")
                fig, axes = plt.subplots(1, 3, figsize=(12, 4))
                
                # Original
                axes[0].imshow(image)
                axes[0].set_title("Original")
                axes[0].axis('off')
                
                # Resized
                axes[1].imshow(resized_image)
                axes[1].set_title("Resized")
                axes[1].axis('off')
                
                # Normalized
                normalized = image_processor.normalize_image(resized_image)
                # Denormalize for display
                normalized_display = image_processor.denormalize_image(normalized)
                axes[2].imshow(normalized_display)
                axes[2].set_title("Normalized")
                axes[2].axis('off')
                
                plt.tight_layout()
                st.pyplot(fig)
    
    with col2:
        if uploaded_file is not None:
            st.header("Analysis Results")
            
            with st.spinner("Analyzing image..."):
                # Ensure we have the processed images available
                if 'processed_image' not in locals():
                    processed_image = image_processor.preprocess_image(image)
                if 'resized_image' not in locals():
                    resized_image = image_processor.resize_image(image)
                
                # Crop classification
                crop_predictions = crop_classifier.predict(processed_image, uploaded_file.name)
                top_crop = max(crop_predictions.items(), key=lambda x: x[1])[0]
                crop_confidence = crop_predictions[top_crop]
                
                # Quality assessment
                quality_result = quality_assessor.assess_quality(resized_image, top_crop)
                
                # Disease detection (if spoiled)
                disease_result = None
                if quality_result['status'] == 'spoiled':
                    disease_result = disease_detector.detect_disease(resized_image, top_crop)
                
                # Display results
                st.subheader("🔍 Crop Identification")
                
                # Main prediction
                if crop_confidence >= confidence_threshold:
                    st.success(f"**Identified Crop:** {top_crop.title()} (Confidence: {crop_confidence:.2%})")
                    if uploaded_file.name:
                        filename_hint = "Filename analysis also helped with identification" if any(word in uploaded_file.name.lower() for word in [top_crop, 'corn', 'maize', 'yam', 'cassava', 'manioc', 'tapioca', 'tomato', 'tomatoes']) else ""
                        if filename_hint:
                            st.info(f"💡 {filename_hint}")
                else:
                    st.warning(f"Low confidence prediction: {top_crop.title()} (Confidence: {crop_confidence:.2%})")
                
                # Quality assessment
                st.subheader("🏥 Quality Assessment")
                quality_status = quality_result['status']
                quality_confidence = quality_result['confidence']
                
                if quality_status == 'fresh':
                    st.success(f"**Status:** Fresh/Healthy (Confidence: {quality_confidence:.2%})")
                    st.info("No treatment required. Continue with good storage practices.")
                else:
                    st.error(f"**Status:** Spoiled/Damaged (Confidence: {quality_confidence:.2%})")
                    
                    # Disease detection results
                    if disease_result:
                        st.subheader("🦠 Disease/Spoilage Analysis")
                        disease_type = disease_result['disease_type']
                        disease_confidence = disease_result['confidence']
                        severity = disease_result['severity']
                        
                        st.warning(f"**Detected Issue:** {disease_type}")
                        st.info(f"**Severity:** {severity} (Confidence: {disease_confidence:.2%})")
                        
                        # Treatment recommendations
                        st.subheader("💊 Treatment Recommendations")
                        treatments = treatment_db.get_treatments(top_crop, disease_type, severity)
                        
                        if treatments:
                            # Immediate actions
                            if treatments.get('immediate_actions'):
                                st.markdown("**Immediate Actions:**")
                                for action in treatments['immediate_actions']:
                                    st.markdown(f"• {action}")
                            
                            # Prevention measures
                            if treatments.get('prevention'):
                                st.markdown("**Prevention Measures:**")
                                for measure in treatments['prevention']:
                                    st.markdown(f"• {measure}")
                            
                            # Treatment options
                            if treatments.get('treatments'):
                                st.markdown("**Treatment Options:**")
                                for treatment in treatments['treatments']:
                                    st.markdown(f"• {treatment}")
                        else:
                            st.warning("No specific treatment recommendations available for this condition.")
                
                # Additional metrics
                st.subheader("📊 Analysis Metrics")
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.metric("Crop Confidence", f"{crop_confidence:.1%}")
                
                with metrics_col2:
                    st.metric("Quality Confidence", f"{quality_confidence:.1%}")
                
                with metrics_col3:
                    if disease_result:
                        st.metric("Disease Confidence", f"{disease_result['confidence']:.1%}")
                    else:
                        st.metric("Disease Confidence", "N/A")
        
        else:
            st.info("Upload an image to begin analysis")
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This system provides AI-assisted analysis for agricultural diagnostics. Always consult with agricultural experts for critical decisions.")

if __name__ == "__main__":
    main()
