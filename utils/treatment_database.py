import json
import os

class TreatmentDatabase:
    """Database of treatment protocols and prevention strategies"""
    
    def __init__(self):
        self.treatments = self._load_treatment_data()
    
    def _load_treatment_data(self):
        """Load treatment data from JSON file"""
        try:
            with open('data/treatment_protocols.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default treatment data if file doesn't exist
            return self._get_default_treatments()
    
    def _get_default_treatments(self):
        """Return default treatment protocols"""
        return {
            "corn": {
                "fungal_infection": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected kernels immediately",
                            "Ensure proper ventilation in storage area",
                            "Reduce moisture levels to below 14%"
                        ],
                        "prevention": [
                            "Maintain proper drying before storage",
                            "Use moisture-proof containers",
                            "Regular inspection for early detection",
                            "Maintain storage temperature below 10°C"
                        ],
                        "treatments": [
                            "Apply food-grade diatomaceous earth",
                            "Use natural antifungal treatments (neem oil)",
                            "Improve storage ventilation"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Isolate affected batch immediately",
                            "Remove all visibly affected kernels",
                            "Test remaining corn for mycotoxins",
                            "Reduce storage humidity to below 60%"
                        ],
                        "prevention": [
                            "Implement proper field drying techniques",
                            "Use certified fungicide treatments",
                            "Install humidity monitoring systems",
                            "Regular cleaning of storage facilities"
                        ],
                        "treatments": [
                            "Apply approved fungicide treatments",
                            "Use ozone treatment for storage areas",
                            "Consider thermal treatment for affected areas"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine entire batch",
                            "Contact agricultural extension services",
                            "Conduct mycotoxin testing",
                            "Do not use for human consumption without testing"
                        ],
                        "prevention": [
                            "Review entire storage and handling process",
                            "Implement integrated pest management",
                            "Consider resistant corn varieties",
                            "Improve field drainage systems"
                        ],
                        "treatments": [
                            "Professional fumigation may be required",
                            "Consider safe disposal of heavily affected portions",
                            "Consult with agricultural specialists"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal of affected corn",
                            "Sanitize all storage equipment",
                            "Report to food safety authorities if for commercial use",
                            "Investigate source of contamination"
                        ],
                        "prevention": [
                            "Complete review of production process",
                            "Implement HACCP principles",
                            "Consider alternative storage methods",
                            "Regular professional inspections"
                        ],
                        "treatments": [
                            "Professional remediation required",
                            "Deep cleaning and sanitization",
                            "May require facility renovation"
                        ]
                    }
                },
                "bacterial_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected kernels",
                            "Improve air circulation",
                            "Check and adjust moisture levels"
                        ],
                        "prevention": [
                            "Proper field harvesting timing",
                            "Avoid physical damage during handling",
                            "Maintain clean storage environment"
                        ],
                        "treatments": [
                            "Natural antimicrobial treatments",
                            "Improve storage conditions",
                            "Regular monitoring"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Isolate affected batch",
                            "Sanitize storage area",
                            "Adjust environmental controls"
                        ],
                        "prevention": [
                            "Implement proper harvesting practices",
                            "Use approved post-harvest treatments",
                            "Regular equipment sanitization"
                        ],
                        "treatments": [
                            "Apply approved bactericides",
                            "Professional storage assessment",
                            "Enhanced monitoring protocols"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine affected corn",
                            "Professional assessment required",
                            "Deep sanitization of facilities"
                        ],
                        "prevention": [
                            "Review entire production chain",
                            "Implement strict hygiene protocols",
                            "Consider facility upgrades"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "May require batch disposal",
                            "Facility decontamination"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal required",
                            "Report to health authorities",
                            "Complete facility sanitization"
                        ],
                        "prevention": [
                            "Complete process overhaul",
                            "Professional consultation required",
                            "Implement comprehensive safety measures"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility may need reconstruction",
                            "Regulatory compliance review"
                        ]
                    }
                },
                "pest_damage": {
                    "mild": {
                        "immediate_actions": [
                            "Inspect for live insects",
                            "Remove damaged kernels",
                            "Clean storage area thoroughly"
                        ],
                        "prevention": [
                            "Use pest-resistant storage containers",
                            "Regular inspection schedules",
                            "Maintain clean storage environment",
                            "Monitor temperature and humidity"
                        ],
                        "treatments": [
                            "Natural pest deterrents (diatomaceous earth)",
                            "Pheromone traps for monitoring",
                            "Improved storage hygiene"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Quarantine affected corn",
                            "Apply approved insecticides",
                            "Deep clean all storage equipment"
                        ],
                        "prevention": [
                            "Implement integrated pest management",
                            "Use certified pest control products",
                            "Regular professional inspections"
                        ],
                        "treatments": [
                            "Professional pest control treatment",
                            "Fumigation if necessary",
                            "Enhanced monitoring systems"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Professional pest control required",
                            "Consider batch disposal",
                            "Facility-wide treatment needed"
                        ],
                        "prevention": [
                            "Complete IPM program implementation",
                            "Facility structural improvements",
                            "Staff training on pest management"
                        ],
                        "treatments": [
                            "Professional fumigation",
                            "Structural pest control measures",
                            "Long-term monitoring program"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal of all affected corn",
                            "Professional facility treatment",
                            "Report to agricultural authorities"
                        ],
                        "prevention": [
                            "Facility reconstruction may be needed",
                            "Complete process redesign",
                            "Professional IPM program design"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "May require facility closure",
                            "Regulatory compliance assessment"
                        ]
                    }
                },
                "overripeness": {
                    "mild": {
                        "immediate_actions": [
                            "Use for immediate consumption or processing",
                            "Separate from fresh corn",
                            "Assess nutritional quality"
                        ],
                        "prevention": [
                            "Optimize harvesting timing",
                            "Improve field monitoring",
                            "Use early maturity indicators"
                        ],
                        "treatments": [
                            "Process into cornmeal or other products",
                            "Blend with fresher corn if quality permits",
                            "Use for animal feed if appropriate"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Test for nutritional quality",
                            "Consider processing options",
                            "Evaluate food safety"
                        ],
                        "prevention": [
                            "Implement better harvest scheduling",
                            "Use field monitoring technology",
                            "Train workers on maturity assessment"
                        ],
                        "treatments": [
                            "Process into suitable products",
                            "Quality testing before use",
                            "Consider alternative uses"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quality assessment required",
                            "May not be suitable for human consumption",
                            "Consider alternative uses"
                        ],
                        "prevention": [
                            "Review harvest timing protocols",
                            "Implement field management improvements",
                            "Consider variety selection"
                        ],
                        "treatments": [
                            "Animal feed use if quality permits",
                            "Composting for agricultural use",
                            "Disposal if completely unsuitable"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Not suitable for food use",
                            "Safe disposal required",
                            "Review production practices"
                        ],
                        "prevention": [
                            "Complete harvest protocol review",
                            "Field management overhaul",
                            "Consider crop rotation"
                        ],
                        "treatments": [
                            "Composting only",
                            "Agricultural waste disposal",
                            "Process review mandatory"
                        ]
                    }
                }
            },
            "tomato": {
                "fungal_infection": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected fruits immediately",
                            "Improve air circulation around plants",
                            "Reduce watering frequency",
                            "Apply organic fungicide treatment"
                        ],
                        "prevention": [
                            "Plant disease-resistant varieties",
                            "Ensure proper plant spacing",
                            "Water at soil level, not on leaves",
                            "Remove plant debris regularly"
                        ],
                        "treatments": [
                            "Baking soda spray (1 tsp per quart water)",
                            "Neem oil application",
                            "Copper-based fungicide spray",
                            "Improve garden sanitation"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Prune affected areas with clean tools",
                            "Apply systemic fungicide",
                            "Increase ventilation in greenhouse",
                            "Isolate affected plants"
                        ],
                        "prevention": [
                            "Implement crop rotation",
                            "Use drip irrigation systems",
                            "Apply preventive fungicide sprays",
                            "Monitor humidity levels closely"
                        ],
                        "treatments": [
                            "Commercial fungicide treatment",
                            "Prune for better air circulation",
                            "Adjust watering schedule",
                            "Consider plant removal if spreading"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Remove entire affected plants",
                            "Apply broad-spectrum fungicide",
                            "Sanitize all garden tools",
                            "Improve drainage systems"
                        ],
                        "prevention": [
                            "Choose highly resistant varieties",
                            "Implement strict sanitation protocols",
                            "Consider soil treatment",
                            "Professional garden assessment"
                        ],
                        "treatments": [
                            "Professional plant disease management",
                            "Soil fumigation may be needed",
                            "Multi-year crop rotation plan",
                            "Enhanced monitoring systems"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Destroy all affected plants immediately",
                            "Do not compost diseased material",
                            "Treat soil with fungicide",
                            "Consider season termination"
                        ],
                        "prevention": [
                            "Complete garden renovation",
                            "Soil replacement or treatment",
                            "Professional consultation required",
                            "Long-term management plan"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "May require greenhouse closure",
                            "Extensive soil treatment needed",
                            "Multi-year recovery plan"
                        ]
                    }
                },
                "bacterial_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected fruits",
                            "Avoid overhead watering",
                            "Sanitize hands and tools",
                            "Improve plant spacing"
                        ],
                        "prevention": [
                            "Use disease-free seeds",
                            "Avoid working in wet conditions",
                            "Sanitize tools between plants",
                            "Maintain proper nutrition"
                        ],
                        "treatments": [
                            "Copper bactericide spray",
                            "Remove lower leaves touching soil",
                            "Improve air circulation",
                            "Adjust irrigation practices"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Quarantine affected plants",
                            "Apply copper-based bactericide",
                            "Remove all affected plant parts",
                            "Disinfect growing area"
                        ],
                        "prevention": [
                            "Implement strict hygiene protocols",
                            "Use certified disease-free plants",
                            "Install proper drainage",
                            "Monitor for early symptoms"
                        ],
                        "treatments": [
                            "Professional bactericide treatment",
                            "Enhanced sanitation measures",
                            "Plant removal if necessary",
                            "Soil treatment protocols"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Remove all affected plants",
                            "Sanitize entire growing area",
                            "Apply broad-spectrum treatment",
                            "Quarantine growing area"
                        ],
                        "prevention": [
                            "Complete growing system review",
                            "Professional consultation",
                            "Enhanced biosecurity measures",
                            "Long-term monitoring plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Facility-wide sanitization",
                            "May require season termination",
                            "Soil replacement consideration"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Destroy all plants immediately",
                            "Professional sanitization required",
                            "Report to agricultural authorities",
                            "Quarantine facility"
                        ],
                        "prevention": [
                            "Complete facility overhaul",
                            "Professional design consultation",
                            "Implement comprehensive protocols",
                            "Regular professional monitoring"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction may be needed",
                            "Regulatory compliance review",
                            "Multi-year recovery plan"
                        ]
                    }
                },
                "overripeness": {
                    "mild": {
                        "immediate_actions": [
                            "Harvest immediately for processing",
                            "Use for cooking or sauce making",
                            "Separate from fresh tomatoes",
                            "Check for secondary infections"
                        ],
                        "prevention": [
                            "Monitor ripening stages daily",
                            "Harvest at optimal timing",
                            "Use succession planting",
                            "Adjust harvest schedules"
                        ],
                        "treatments": [
                            "Process into sauce, paste, or juice",
                            "Dehydrate for preservation",
                            "Use for cooking immediately",
                            "Compost if too soft"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Assess food safety before use",
                            "Use only for processed products",
                            "Remove any diseased portions",
                            "Process within 24 hours"
                        ],
                        "prevention": [
                            "Improve harvest timing",
                            "Use ripeness indicators",
                            "Train workers on assessment",
                            "Implement harvest scheduling"
                        ],
                        "treatments": [
                            "Cooking use only",
                            "Industrial processing if applicable",
                            "Animal feed if safe",
                            "Composting for agriculture"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quality assessment required",
                            "May not be safe for consumption",
                            "Check for mold or bacteria",
                            "Consider disposal"
                        ],
                        "prevention": [
                            "Review harvest protocols",
                            "Improve field monitoring",
                            "Consider variety selection",
                            "Train on quality assessment"
                        ],
                        "treatments": [
                            "Composting only",
                            "Agricultural use if safe",
                            "Safe disposal required",
                            "Not suitable for food"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal required",
                            "Not safe for any food use",
                            "Sanitize handling equipment",
                            "Review handling practices"
                        ],
                        "prevention": [
                            "Complete harvest overhaul",
                            "Professional training required",
                            "System redesign needed",
                            "Quality control implementation"
                        ],
                        "treatments": [
                            "Safe disposal only",
                            "Composting with caution",
                            "Review all practices",
                            "Professional consultation"
                        ]
                    }
                },
                "blossom_end_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Cut away affected area if small",
                            "Increase calcium availability",
                            "Maintain consistent watering",
                            "Test soil pH levels"
                        ],
                        "prevention": [
                            "Ensure adequate calcium in soil",
                            "Maintain consistent soil moisture",
                            "Avoid root damage during cultivation",
                            "Use mulch to retain moisture"
                        ],
                        "treatments": [
                            "Apply calcium chloride spray",
                            "Improve irrigation consistency",
                            "Add organic matter to soil",
                            "Monitor and adjust pH"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Remove affected portions",
                            "Apply calcium foliar spray",
                            "Adjust watering schedule",
                            "Test for nutrient deficiencies"
                        ],
                        "prevention": [
                            "Implement consistent irrigation",
                            "Regular soil testing",
                            "Proper nutrition management",
                            "Avoid excess nitrogen"
                        ],
                        "treatments": [
                            "Professional soil amendment",
                            "Drip irrigation installation",
                            "Calcium supplementation program",
                            "Enhanced moisture management"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Fruits may not be suitable for fresh use",
                            "Process into products if possible",
                            "Review entire nutrition program",
                            "Consult agricultural specialist"
                        ],
                        "prevention": [
                            "Complete soil and nutrition assessment",
                            "Professional irrigation design",
                            "Long-term soil improvement plan",
                            "Regular professional monitoring"
                        ],
                        "treatments": [
                            "Professional consultation required",
                            "Comprehensive soil treatment",
                            "Irrigation system overhaul",
                            "Multi-season recovery plan"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Fruits not suitable for consumption",
                            "Complete growing system review",
                            "Professional assessment required",
                            "Consider crop termination"
                        ],
                        "prevention": [
                            "Complete growing system redesign",
                            "Professional consultation mandatory",
                            "Soil replacement consideration",
                            "Long-term management plan"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "May require facility upgrades",
                            "Multi-year improvement plan",
                            "Regulatory consultation"
                        ]
                    }
                }
            },
            "yam": {
                "fungal_infection": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected portions with clean knife",
                            "Dry cut surfaces in sun",
                            "Improve storage ventilation",
                            "Reduce storage humidity"
                        ],
                        "prevention": [
                            "Cure yams properly before storage",
                            "Maintain storage temperature 55-60°F",
                            "Ensure good air circulation",
                            "Regular inspection for early detection"
                        ],
                        "treatments": [
                            "Apply wood ash to cut surfaces",
                            "Use traditional antifungal herbs",
                            "Improve storage conditions",
                            "Monitor humidity levels"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Isolate affected yams",
                            "Cut away all visible infection",
                            "Apply antifungal treatment",
                            "Adjust storage environment"
                        ],
                        "prevention": [
                            "Implement proper curing process",
                            "Use approved storage treatments",
                            "Install humidity control systems",
                            "Regular professional inspection"
                        ],
                        "treatments": [
                            "Commercial antifungal treatment",
                            "Storage facility sanitization",
                            "Enhanced monitoring protocols",
                            "Professional storage assessment"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine all affected yams",
                            "Deep sanitization of storage area",
                            "Professional assessment required",
                            "May require batch disposal"
                        ],
                        "prevention": [
                            "Complete storage system review",
                            "Professional consultation",
                            "Enhanced quality control",
                            "Long-term monitoring plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Storage facility treatment",
                            "May require equipment replacement",
                            "Comprehensive recovery plan"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal of all affected yams",
                            "Professional facility sanitization",
                            "Report to agricultural authorities",
                            "Complete facility shutdown"
                        ],
                        "prevention": [
                            "Complete facility overhaul",
                            "Professional design consultation",
                            "Implement advanced monitoring",
                            "Regular professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction may be needed",
                            "Regulatory compliance review",
                            "Multi-year recovery program"
                        ]
                    }
                },
                "bacterial_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Remove soft spots immediately",
                            "Dry remaining yam surfaces",
                            "Improve storage sanitation",
                            "Reduce moisture levels"
                        ],
                        "prevention": [
                            "Handle yams carefully to avoid wounds",
                            "Cure properly before storage",
                            "Maintain clean storage environment",
                            "Regular quality inspections"
                        ],
                        "treatments": [
                            "Natural antimicrobial treatments",
                            "Improve storage hygiene",
                            "Enhanced ventilation",
                            "Regular monitoring"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Isolate affected yams",
                            "Sanitize storage containers",
                            "Apply approved treatments",
                            "Monitor remaining stock closely"
                        ],
                        "prevention": [
                            "Implement hygiene protocols",
                            "Use clean handling equipment",
                            "Regular sanitization schedules",
                            "Staff training on handling"
                        ],
                        "treatments": [
                            "Professional antimicrobial treatment",
                            "Storage facility sanitization",
                            "Enhanced quality control",
                            "Professional monitoring"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine entire batch",
                            "Professional assessment required",
                            "Deep facility sanitization",
                            "Consider batch disposal"
                        ],
                        "prevention": [
                            "Complete process review",
                            "Professional consultation",
                            "Enhanced biosecurity measures",
                            "Long-term improvement plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Facility-wide treatment",
                            "May require equipment replacement",
                            "Comprehensive monitoring system"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal required",
                            "Professional facility treatment",
                            "Report to health authorities",
                            "Complete operation shutdown"
                        ],
                        "prevention": [
                            "Complete facility overhaul",
                            "Professional system redesign",
                            "Implement comprehensive protocols",
                            "Regular professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction consideration",
                            "Regulatory compliance review",
                            "Multi-year recovery plan"
                        ]
                    }
                },
                "storage_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected areas",
                            "Improve storage conditions",
                            "Check environmental controls",
                            "Monitor remaining stock"
                        ],
                        "prevention": [
                            "Optimize storage temperature and humidity",
                            "Ensure proper air circulation",
                            "Regular facility maintenance",
                            "Quality monitoring systems"
                        ],
                        "treatments": [
                            "Adjust storage parameters",
                            "Improve facility conditions",
                            "Enhanced monitoring",
                            "Regular inspections"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Separate affected yams",
                            "Review storage protocols",
                            "Adjust environmental controls",
                            "Professional assessment"
                        ],
                        "prevention": [
                            "Upgrade storage facilities",
                            "Implement monitoring systems",
                            "Staff training programs",
                            "Regular professional reviews"
                        ],
                        "treatments": [
                            "Professional storage consultation",
                            "Facility improvements",
                            "Enhanced control systems",
                            "Long-term monitoring"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine affected stock",
                            "Professional facility assessment",
                            "Major storage adjustments",
                            "Consider stock disposal"
                        ],
                        "prevention": [
                            "Complete storage system overhaul",
                            "Professional facility design",
                            "Advanced monitoring implementation",
                            "Comprehensive training programs"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Major facility upgrades",
                            "Complete system redesign",
                            "Multi-phase improvement plan"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Complete stock disposal",
                            "Facility closure for renovation",
                            "Professional remediation",
                            "Regulatory notification"
                        ],
                        "prevention": [
                            "Complete facility reconstruction",
                            "Professional design and oversight",
                            "Implement advanced systems",
                            "Ongoing professional management"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction required",
                            "Regulatory compliance program",
                            "Long-term recovery plan"
                        ]
                    }
                },
                "sprouting": {
                    "mild": {
                        "immediate_actions": [
                            "Remove sprouts carefully",
                            "Adjust storage temperature",
                            "Reduce light exposure",
                            "Use sprouted yams first"
                        ],
                        "prevention": [
                            "Maintain proper storage temperature",
                            "Store in dark conditions",
                            "Ensure proper curing",
                            "Regular rotation of stock"
                        ],
                        "treatments": [
                            "Adjust storage conditions",
                            "Remove sprouts before cooking",
                            "Use for immediate consumption",
                            "Monitor storage environment"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Separate sprouting yams",
                            "Review storage conditions",
                            "Adjust temperature and humidity",
                            "Process sprouted yams quickly"
                        ],
                        "prevention": [
                            "Optimize storage parameters",
                            "Implement proper curing",
                            "Regular monitoring systems",
                            "Improved facility design"
                        ],
                        "treatments": [
                            "Professional storage assessment",
                            "Environmental control improvements",
                            "Enhanced monitoring protocols",
                            "Adjusted handling procedures"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Assess yam quality thoroughly",
                            "May not be suitable for fresh use",
                            "Consider processing options",
                            "Review entire storage system"
                        ],
                        "prevention": [
                            "Complete storage system review",
                            "Professional consultation",
                            "Advanced environmental controls",
                            "Long-term monitoring plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Major storage improvements",
                            "Quality assessment protocols",
                            "Alternative use planning"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Yams not suitable for consumption",
                            "Complete storage system failure",
                            "Professional assessment required",
                            "Consider total loss"
                        ],
                        "prevention": [
                            "Complete facility overhaul",
                            "Professional system redesign",
                            "Implement advanced controls",
                            "Ongoing professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Complete system replacement",
                            "May require facility reconstruction",
                            "Long-term recovery plan"
                        ]
                    }
                }
            },
            "cassava": {
                "fungal_infection": {
                    "mild": {
                        "immediate_actions": [
                            "Remove affected areas with clean knife",
                            "Dry cut surfaces thoroughly",
                            "Process within 24 hours",
                            "Improve storage ventilation"
                        ],
                        "prevention": [
                            "Harvest at optimal timing",
                            "Process soon after harvest",
                            "Maintain clean processing environment",
                            "Proper drying techniques"
                        ],
                        "treatments": [
                            "Traditional antimicrobial treatments",
                            "Improved processing hygiene",
                            "Enhanced drying methods",
                            "Regular quality monitoring"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Isolate affected cassava",
                            "Cut away all infected portions",
                            "Apply approved treatments",
                            "Sanitize processing equipment"
                        ],
                        "prevention": [
                            "Implement proper harvest timing",
                            "Use clean processing methods",
                            "Regular equipment sanitization",
                            "Quality control protocols"
                        ],
                        "treatments": [
                            "Commercial antifungal treatment",
                            "Professional processing assessment",
                            "Enhanced sanitation protocols",
                            "Improved quality control"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine all affected cassava",
                            "Professional quality assessment",
                            "Deep sanitization required",
                            "May require batch disposal"
                        ],
                        "prevention": [
                            "Complete process review",
                            "Professional consultation",
                            "Enhanced biosecurity measures",
                            "Long-term improvement plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Facility-wide treatment",
                            "Process redesign consideration",
                            "Comprehensive monitoring"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal required",
                            "Professional facility treatment",
                            "Report to food safety authorities",
                            "Processing facility shutdown"
                        ],
                        "prevention": [
                            "Complete facility overhaul",
                            "Professional system redesign",
                            "Implement comprehensive protocols",
                            "Regular professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction consideration",
                            "Regulatory compliance review",
                            "Multi-year recovery plan"
                        ]
                    }
                },
                "bacterial_rot": {
                    "mild": {
                        "immediate_actions": [
                            "Remove soft spots immediately",
                            "Process remaining cassava quickly",
                            "Sanitize cutting tools",
                            "Improve processing hygiene"
                        ],
                        "prevention": [
                            "Minimize processing time after harvest",
                            "Maintain clean processing environment",
                            "Use sanitized equipment",
                            "Regular quality inspections"
                        ],
                        "treatments": [
                            "Enhanced sanitation protocols",
                            "Improved processing speed",
                            "Regular equipment cleaning",
                            "Quality monitoring systems"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Separate affected cassava",
                            "Deep sanitization of equipment",
                            "Apply antimicrobial treatments",
                            "Review processing procedures"
                        ],
                        "prevention": [
                            "Implement strict hygiene protocols",
                            "Regular equipment sanitization",
                            "Staff training on hygiene",
                            "Environmental monitoring"
                        ],
                        "treatments": [
                            "Professional sanitization",
                            "Enhanced processing protocols",
                            "Quality control improvements",
                            "Staff training programs"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Quarantine all affected material",
                            "Professional assessment required",
                            "Facility-wide sanitization",
                            "Consider batch disposal"
                        ],
                        "prevention": [
                            "Complete process review",
                            "Professional consultation",
                            "Enhanced biosecurity protocols",
                            "Long-term monitoring plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Comprehensive facility treatment",
                            "Process redesign consideration",
                            "Multi-phase improvement"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal of all material",
                            "Professional facility treatment",
                            "Report to health authorities",
                            "Complete facility shutdown"
                        ],
                        "prevention": [
                            "Complete facility reconstruction",
                            "Professional system design",
                            "Implement comprehensive protocols",
                            "Ongoing professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction required",
                            "Regulatory compliance program",
                            "Long-term recovery plan"
                        ]
                    }
                },
                "storage_deterioration": {
                    "mild": {
                        "immediate_actions": [
                            "Process immediately",
                            "Remove discolored portions",
                            "Assess remaining quality",
                            "Improve storage conditions"
                        ],
                        "prevention": [
                            "Minimize storage time",
                            "Maintain optimal storage conditions",
                            "Regular quality monitoring",
                            "First-in-first-out rotation"
                        ],
                        "treatments": [
                            "Immediate processing",
                            "Quality assessment protocols",
                            "Improved storage management",
                            "Enhanced monitoring"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Assess food safety",
                            "Process only if quality permits",
                            "Remove all affected areas",
                            "Review storage protocols"
                        ],
                        "prevention": [
                            "Optimize storage parameters",
                            "Implement monitoring systems",
                            "Regular facility maintenance",
                            "Staff training programs"
                        ],
                        "treatments": [
                            "Professional quality assessment",
                            "Storage system improvements",
                            "Enhanced monitoring protocols",
                            "Process optimization"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "May not be suitable for consumption",
                            "Professional quality assessment",
                            "Consider alternative uses",
                            "Review entire storage system"
                        ],
                        "prevention": [
                            "Complete storage system review",
                            "Professional consultation",
                            "Advanced monitoring implementation",
                            "Long-term improvement plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Major storage improvements",
                            "Quality control overhaul",
                            "Alternative use assessment"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Not suitable for food use",
                            "Safe disposal required",
                            "Complete system failure",
                            "Professional assessment needed"
                        ],
                        "prevention": [
                            "Complete system overhaul",
                            "Professional facility redesign",
                            "Implement advanced controls",
                            "Ongoing professional management"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Complete system replacement",
                            "Facility reconstruction consideration",
                            "Long-term recovery program"
                        ]
                    }
                },
                "pest_damage": {
                    "mild": {
                        "immediate_actions": [
                            "Remove damaged portions",
                            "Inspect for live pests",
                            "Clean processing area",
                            "Process remaining cassava quickly"
                        ],
                        "prevention": [
                            "Regular pest monitoring",
                            "Maintain clean storage areas",
                            "Use pest-resistant storage methods",
                            "Rapid processing after harvest"
                        ],
                        "treatments": [
                            "Natural pest deterrents",
                            "Improved sanitation",
                            "Enhanced monitoring",
                            "Quality control measures"
                        ]
                    },
                    "moderate": {
                        "immediate_actions": [
                            "Quarantine affected cassava",
                            "Apply appropriate pest control",
                            "Deep clean all equipment",
                            "Assess remaining stock"
                        ],
                        "prevention": [
                            "Implement integrated pest management",
                            "Regular facility inspections",
                            "Use certified pest control methods",
                            "Staff training on pest identification"
                        ],
                        "treatments": [
                            "Professional pest control",
                            "Enhanced sanitation protocols",
                            "Monitoring system installation",
                            "Quality assessment procedures"
                        ]
                    },
                    "severe": {
                        "immediate_actions": [
                            "Professional pest control required",
                            "May require material disposal",
                            "Facility-wide treatment needed",
                            "Complete facility inspection"
                        ],
                        "prevention": [
                            "Complete IPM program implementation",
                            "Facility structural improvements",
                            "Professional monitoring systems",
                            "Long-term pest management plan"
                        ],
                        "treatments": [
                            "Professional intervention required",
                            "Comprehensive facility treatment",
                            "Structural pest control measures",
                            "Multi-phase improvement plan"
                        ]
                    },
                    "critical": {
                        "immediate_actions": [
                            "Immediate disposal of all material",
                            "Professional facility treatment",
                            "Report to agricultural authorities",
                            "Complete facility quarantine"
                        ],
                        "prevention": [
                            "Complete facility reconstruction",
                            "Professional IPM design",
                            "Implement comprehensive protocols",
                            "Ongoing professional oversight"
                        ],
                        "treatments": [
                            "Professional remediation only",
                            "Facility reconstruction required",
                            "Regulatory compliance review",
                            "Long-term recovery program"
                        ]
                    }
                }
            }
        }
    
    def get_treatments(self, crop_type, disease_type, severity):
        """Get treatment recommendations for specific crop, disease, and severity"""
        try:
            return self.treatments[crop_type][disease_type][severity]
        except KeyError:
            # Return generic treatment if specific combination not found
            return {
                "immediate_actions": [
                    "Remove affected portions immediately",
                    "Improve storage/growing conditions",
                    "Consult with agricultural specialist"
                ],
                "prevention": [
                    "Regular monitoring and inspection",
                    "Maintain optimal environmental conditions",
                    "Use certified disease-resistant varieties",
                    "Implement proper sanitation practices"
                ],
                "treatments": [
                    "Apply appropriate organic or chemical treatments",
                    "Improve environmental controls",
                    "Consider professional consultation",
                    "Monitor treatment effectiveness"
                ]
            }
    
    def get_general_recommendations(self, crop_type):
        """Get general care recommendations for a crop type"""
        recommendations = {
            "corn": {
                "optimal_conditions": {
                    "temperature": "50-60°F for storage",
                    "humidity": "Below 14% moisture content",
                    "ventilation": "Good air circulation required"
                },
                "common_issues": [
                    "Fungal infections in high humidity",
                    "Pest infestations in storage",
                    "Moisture-related spoilage"
                ],
                "best_practices": [
                    "Proper drying before storage",
                    "Regular monitoring for pests",
                    "Clean storage facilities",
                    "Maintain optimal temperature and humidity"
                ]
            },
            "tomato": {
                "optimal_conditions": {
                    "temperature": "55-70°F",
                    "humidity": "85-90% relative humidity",
                    "ventilation": "Good air circulation"
                },
                "common_issues": [
                    "Fungal diseases in humid conditions",
                    "Bacterial infections",
                    "Rapid ripening and overripeness"
                ],
                "best_practices": [
                    "Harvest at proper ripeness stage",
                    "Handle carefully to avoid damage",
                    "Store at appropriate temperature",
                    "Regular quality inspections"
                ]
            },
            "yam": {
                "optimal_conditions": {
                    "temperature": "55-60°F",
                    "humidity": "85-90% relative humidity",
                    "ventilation": "Good air circulation"
                },
                "common_issues": [
                    "Storage rot in poor conditions",
                    "Sprouting in warm conditions",
                    "Fungal infections"
                ],
                "best_practices": [
                    "Proper curing before storage",
                    "Maintain optimal storage conditions",
                    "Regular rotation of stock",
                    "Careful handling to avoid damage"
                ]
            },
            "cassava": {
                "optimal_conditions": {
                    "temperature": "32-40°F for short-term storage",
                    "humidity": "85-95% relative humidity",
                    "processing": "Process within 24-48 hours of harvest"
                },
                "common_issues": [
                    "Rapid deterioration after harvest",
                    "Post-harvest physiological deterioration",
                    "Pest damage in storage"
                ],
                "best_practices": [
                    "Process as soon as possible after harvest",
                    "Maintain cold chain if storing",
                    "Use proper processing techniques",
                    "Monitor for quality changes"
                ]
            }
        }
        
        return recommendations.get(crop_type, {
            "optimal_conditions": {
                "temperature": "Maintain appropriate temperature",
                "humidity": "Control humidity levels",
                "ventilation": "Ensure adequate air circulation"
            },
            "common_issues": [
                "Environmental stress",
                "Disease and pest problems",
                "Storage and handling issues"
            ],
            "best_practices": [
                "Regular monitoring and inspection",
                "Proper storage conditions",
                "Good sanitation practices",
                "Professional consultation when needed"
            ]
        })
    
    def search_treatments(self, keyword):
        """Search for treatments containing specific keywords"""
        results = []
        
        for crop in self.treatments:
            for disease in self.treatments[crop]:
                for severity in self.treatments[crop][disease]:
                    treatment_data = self.treatments[crop][disease][severity]
                    
                    # Search in all treatment fields
                    all_text = str(treatment_data).lower()
                    if keyword.lower() in all_text:
                        results.append({
                            'crop': crop,
                            'disease': disease,
                            'severity': severity,
                            'treatments': treatment_data
                        })
        
        return results
