# Agricultural Computer Vision System

## Overview

This is an AI-powered agricultural analysis system built with Streamlit that provides comprehensive crop analysis capabilities. The system uses computer vision and machine learning to analyze images of four main crops (corn, yam, cassava, and tomato) and provides:

- **Crop identification** using transfer learning with MobileNetV2
- **Quality assessment** to determine if crops are fresh or spoiled
- **Disease detection** to identify specific diseases, spoilage types, and pest damage
- **Treatment recommendations** with actionable protocols based on detected issues

The system is designed to assist farmers, agricultural professionals, and food safety inspectors in making informed decisions about crop management and treatment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Streamlit-based web interface** providing an intuitive upload-and-analyze workflow
- **Single-page application** with sidebar navigation for system information
- **Real-time image processing** with immediate visual feedback and analysis results
- **Responsive layout** supporting wide-screen displays for detailed analysis views

### Machine Learning Pipeline
- **Transfer Learning Approach**: Uses pre-trained MobileNetV2 as the backbone for crop classification
- **Multi-model Architecture**: Three specialized models working in concert:
  - Crop classifier for species identification
  - Quality assessor for freshness evaluation
  - Disease detector for specific pathology identification
- **Image Processing Pipeline**: Standardized preprocessing with ImageNet normalization and resizing to 224x224 pixels
- **Confidence-based Results**: All models provide confidence scores capped at 95% for reliability

### Data Management
- **JSON-based Treatment Database**: Comprehensive treatment protocols stored in structured JSON format
- **Hierarchical Disease Classification**: Organized by crop type, disease category, and severity levels
- **Cached Model Loading**: Streamlit caching for efficient model initialization and reuse
- **Pattern-based Detection**: Rule-based systems for identifying visual indicators of diseases and spoilage

### Treatment Recommendation System
- **Severity-based Protocols**: Treatment recommendations scaled by detected severity (mild, moderate, severe, critical)
- **Multi-category Approach**: Addresses immediate actions, prevention strategies, and ongoing treatments
- **Safety-first Philosophy**: Prioritizes food safety and consumer health in all recommendations
- **Professional Consultation Integration**: Built-in escalation paths for severe cases

## External Dependencies

### Machine Learning Frameworks
- **TensorFlow/Keras**: Core deep learning framework for model building and inference
- **MobileNetV2**: Pre-trained ImageNet model for transfer learning backbone

### Image Processing Libraries
- **OpenCV (cv2)**: Advanced image processing operations and computer vision algorithms
- **PIL (Python Imaging Library)**: Image loading, manipulation, and format conversion
- **NumPy**: Numerical computing foundation for array operations

### Web Framework and Visualization
- **Streamlit**: Web application framework for the user interface
- **Matplotlib**: Statistical plotting and visualization
- **Plotly Express**: Interactive plotting and data visualization
- **Pandas**: Data manipulation and analysis

### Data Storage
- **JSON files**: Treatment protocols and configuration data stored locally
- **No external database**: Self-contained system with file-based data storage

### Potential Future Integrations
- **Agricultural APIs**: Weather data, pest alerts, and market information
- **Cloud Storage**: For model weights and large datasets
- **Database Systems**: PostgreSQL or similar for production deployments
- **Mobile APIs**: Integration with mobile apps for field use