"""
Spec Management Skill for Qwen
Manages the creation, validation, and processing of specification files
"""

import os
import json
from datetime import datetime

def create_spec(feature_name, description="", requirements=None, acceptance_criteria=None, phase="I"):
    """
    Creates a new specification file based on the project's template
    """
    if requirements is None:
        requirements = []
    if acceptance_criteria is None:
        acceptance_criteria = []
    
    # Create the specs directory if it doesn't exist
    specs_dir = "specs"
    if not os.path.exists(specs_dir):
        os.makedirs(specs_dir)
    
    # Create feature directory
    feature_dir = os.path.join(specs_dir, feature_name.lower().replace(" ", "_"))
    if not os.path.exists(feature_dir):
        os.makedirs(feature_dir)
    
    # Create spec content following the template structure
    spec_content = f"""# {feature_name.replace('-', ' ').title()} Spec

## Feature Overview
{description}

## Phase
Phase {phase} - {get_phase_description(phase)}

## Requirements
"""
    
    for i, req in enumerate(requirements, 1):
        spec_content += f"\n{i}. {req}"
    
    spec_content += "\n\n## Acceptance Criteria"
    
    for i, criteria in enumerate(acceptance_criteria, 1):
        spec_content += f"\n{i}. {criteria}"
    
    spec_content += f"""

## Dependencies
- None

## Out of Scope
- Items not included in this feature

## Implementation Notes
- Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- AI-generated implementation required
- Must comply with project constitution
"""

    # Write the spec file
    spec_path = os.path.join(feature_dir, "spec.md")
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    return f"Specification created at {spec_path}"

def get_phase_description(phase):
    """Returns description for each phase"""
    phases = {
        "I": "Core Todo Engine - Local, non-AI Todo system with CRUD operations",
        "II": "Persistence & Validation - Persistent storage and input validation",
        "III": "Conversational AI Interface - Natural language Todo management",
        "IV": "Local Cloud-Native Deployment - Containerized application with Minikube",
        "V": "Cloud Deployment & Scaling - Deployment to DigitalOcean Kubernetes"
    }
    return phases.get(phase, "Unknown phase")

def validate_spec(spec_path):
    """
    Validates that a spec file follows the required structure per constitution
    """
    if not os.path.exists(spec_path):
        return {"valid": False, "errors": [f"File does not exist: {spec_path}"]}
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = [
        "# ",           # Main title
        "## Feature Overview", 
        "## Requirements", 
        "## Acceptance Criteria",
        "## Dependencies",
        "## Out of Scope"
    ]
    
    errors = []
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check if it mentions AI implementation requirement
    if "AI-generated" not in content and "AI generated" not in content:
        errors.append("Spec should mention AI-generated implementation requirement")
    
    # Check if it mentions constitution compliance
    if "constitution" not in content.lower():
        errors.append("Spec should mention compliance with project constitution")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "message": "Spec is valid" if len(errors) == 0 else f"Spec has {len(errors)} issues"
    }

def create_phase_spec(phase_number, additional_features=None):
    """
    Creates a specification for a specific phase of the project
    """
    if additional_features is None:
        additional_features = []
    
    phase_names = {
        "I": "Core Todo Engine",
        "II": "Persistence & Validation", 
        "III": "Conversational AI Interface",
        "IV": "Local Cloud-Native Deployment",
        "V": "Cloud Deployment & Scaling"
    }
    
    phase_descriptions = {
        "I": "Implement core todo functionality: Add, Delete, Update, View, Mark Complete",
        "II": "Add persistent storage and input validation to core functionality",
        "III": "Integrate conversational AI for natural language todo management",
        "IV": "Deploy application locally using containerization and Minikube",
        "V": "Deploy application to cloud using DigitalOcean Kubernetes"
    }
    
    requirements = [
        "All core todo functions must be implemented as specified in Constitution section 3",
        "Implementation must be AI-generated only as per Constitution section 2.3",
        "Must comply with Constitution at all times as per section 2.2"
    ]
    
    # Add phase-specific requirements
    requirements.extend(get_phase_requirements(phase_number))
    
    acceptance_criteria = [
        "All required functionality works as specified",
        "Implementation was generated by AI without manual code changes",
        "All tests pass",
        "Spec complies with project constitution"
    ]
    
    # Add phase-specific acceptance criteria
    acceptance_criteria.extend(get_phase_acceptance_criteria(phase_number))
    
    return create_spec(
        f"phase_{phase_number}_spec",
        f"Specification for Phase {phase_number} - {phase_names[phase_number]}: {phase_descriptions[phase_number]}",
        requirements,
        acceptance_criteria,
        phase_number
    )

def get_phase_requirements(phase):
    """Get phase-specific requirements"""
    requirements = {
        "I": [
            "Implement Add Task functionality",
            "Implement Delete Task functionality", 
            "Implement Update Task functionality",
            "Implement View Task List functionality",
            "Implement Mark as Complete functionality"
        ],
        "II": [
            "Add persistent storage (file or database)",
            "Implement input validation rules",
            "Add comprehensive error handling"
        ],
        "III": [
            "Integrate with OpenAI Chatkit",
            "Integrate with OpenAI Agents SDK", 
            "Integrate with Official MCP SDK",
            "Implement natural language processing for todo commands"
        ],
        "IV": [
            "Create Kubernetes manifests",
            "Containerize the application",
            "Deploy using Minikube",
            "Ensure AI chatbot works in cluster"
        ],
        "V": [
            "Deploy to DigitalOcean Kubernetes (DOKS)",
            "Implement scalable AI chatbot service",
            "Set up production-ready architecture"
        ]
    }
    return requirements.get(phase, [])

def get_phase_acceptance_criteria(phase):
    """Get phase-specific acceptance criteria"""
    acceptance = {
        "I": [
            "Core todo functions (Add, Delete, Update, View, Mark Complete) work correctly",
            "No data persistence required yet"
        ],
        "II": [
            "Todos persist between application runs",
            "Input validation prevents invalid data",
            "Error handling works appropriately"
        ],
        "III": [
            "Natural language commands work correctly",
            "AI correctly interprets user intent",
            "All core functions accessible via chat interface"
        ],
        "IV": [
            "Application deploys successfully on Minikube",
            "All functionality works in containerized environment",
            "AI chatbot functions in cluster"
        ],
        "V": [
            "Application deploys successfully on DOKS",
            "System scales appropriately",
            "Production-level performance achieved"
        ]
    }
    return acceptance.get(phase, [])

def list_specs():
    """List all available spec directories"""
    specs_dir = "specs"
    if not os.path.exists(specs_dir):
        return []
    
    return [d for d in os.listdir(specs_dir) if os.path.isdir(os.path.join(specs_dir, d))]