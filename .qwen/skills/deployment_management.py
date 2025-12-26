"""
Deployment Management Skill for Qwen
Handles deployment operations for Phase IV (Minikube) and Phase V (DOKS) as specified in the constitution
"""

import os
import json
from typing import Dict, List, Optional

def generate_k8s_manifests(app_name: str, 
                          image_name: str, 
                          replicas: int = 1, 
                          port: int = 8080,
                          env_vars: Optional[Dict[str, str]] = None) -> Dict:
    """
    Generate Kubernetes manifests for deployment
    Following Constitution section 7: Deployment & Infrastructure Rules
    """
    
    if env_vars is None:
        env_vars = {}
    
    # Generate Deployment manifest
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": app_name,
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": app_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": app_name
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": app_name,
                            "image": image_name,
                            "ports": [
                                {
                                    "containerPort": port
                                }
                            ],
                            "env": [{"name": k, "value": v} for k, v in env_vars.items()]
                        }
                    ]
                }
            }
        }
    }
    
    # Generate Service manifest
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"{app_name}-service"
        },
        "spec": {
            "selector": {
                "app": app_name
            },
            "ports": [
                {
                    "protocol": "TCP",
                    "port": 80,
                    "targetPort": port
                }
            ],
            "type": "LoadBalancer"  # For external access
        }
    }
    
    # Generate ConfigMap if there are environment variables
    config_map = None
    if env_vars:
        config_map = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": f"{app_name}-config"
            },
            "data": env_vars
        }
    
    manifests = {
        "deployment": deployment,
        "service": service
    }
    
    if config_map:
        manifests["configmap"] = config_map
    
    return manifests

def save_k8s_manifests(manifests: Dict, output_dir: str = "k8s-manifests") -> List[str]:
    """
    Save Kubernetes manifests to files
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    saved_files = []
    
    for manifest_type, manifest in manifests.items():
        filename = os.path.join(output_dir, f"{manifest_type}.yaml")
        with open(filename, 'w') as f:
            # Convert dict to YAML-like string (simplified)
            yaml_content = dict_to_yaml(manifest)
            f.write(yaml_content)
        saved_files.append(filename)
    
    return saved_files

def dict_to_yaml(d, indent=0):
    """
    Convert a dictionary to a YAML-like string representation
    """
    yaml_str = ""
    indent_space = "  " * indent
    
    for key, value in d.items():
        if isinstance(value, dict):
            yaml_str += f"{indent_space}{key}:\n"
            yaml_str += dict_to_yaml(value, indent + 1)
        elif isinstance(value, list):
            yaml_str += f"{indent_space}{key}:\n"
            for item in value:
                if isinstance(item, dict):
                    yaml_str += f"{indent_space}  -\n"
                    yaml_str += dict_to_yaml(item, indent + 2)
                else:
                    yaml_str += f"{indent_space}  - {item}\n"
        else:
            yaml_str += f"{indent_space}{key}: {value}\n"
    
    return yaml_str

def generate_minikube_deployment(app_name: str, 
                                image_name: str, 
                                replicas: int = 1, 
                                port: int = 8080,
                                env_vars: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Generate Kubernetes manifests specifically for Minikube deployment (Phase IV)
    Following Constitution section 7.1: Local Deployment
    """
    manifests = generate_k8s_manifests(app_name, image_name, replicas, port, env_vars)
    return save_k8s_manifests(manifests, "minikube-manifests")

def generate_doks_deployment(app_name: str, 
                            image_name: str, 
                            replicas: int = 3,  # More replicas for production
                            port: int = 8080,
                            env_vars: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Generate Kubernetes manifests specifically for DOKS deployment (Phase V)
    Following Constitution section 7.2: Cloud Deployment
    """
    # Add production-specific environment variables
    prod_env_vars = {
        "ENV": "production",
        "LOG_LEVEL": "info"
    }
    if env_vars:
        prod_env_vars.update(env_vars)
    
    manifests = generate_k8s_manifests(app_name, image_name, replicas, port, prod_env_vars)
    return save_k8s_manifests(manifests, "doks-manifests")

def create_deployment_spec(phase: str, 
                          app_name: str, 
                          image_name: str,
                          additional_config: Optional[Dict] = None) -> str:
    """
    Create a deployment specification following the Constitution's requirements
    """
    if additional_config is None:
        additional_config = {}
    
    deployment_spec = {
        "phase": phase,
        "app_name": app_name,
        "image_name": image_name,
        "created_at": __import__('datetime').datetime.now().isoformat(),
        "constitution_compliant": True,
        "ai_generated": True,
        "deployment_config": {
            "replicas": additional_config.get("replicas", 1 if phase == "IV" else 3),
            "port": additional_config.get("port", 8080),
            "environment": additional_config.get("environment", "dev" if phase == "IV" else "prod"),
            "provider": "minikube" if phase == "IV" else "doks"
        }
    }
    
    # Save the deployment spec
    spec_dir = "deployment-specs"
    if not os.path.exists(spec_dir):
        os.makedirs(spec_dir)
    
    spec_path = os.path.join(spec_dir, f"phase_{phase.lower()}_deployment.json")
    with open(spec_path, 'w') as f:
        json.dump(deployment_spec, f, indent=2)
    
    return spec_path

def validate_deployment_spec(spec_path: str) -> Dict:
    """
    Validate that a deployment spec follows the Constitution's requirements
    """
    if not os.path.exists(spec_path):
        return {"valid": False, "errors": [f"Spec file does not exist: {spec_path}"]}
    
    with open(spec_path, 'r') as f:
        spec = json.load(f)
    
    errors = []
    
    # Check constitution compliance
    if not spec.get("constitution_compliant"):
        errors.append("Deployment spec must be constitution compliant")
    
    # Check AI generation requirement
    if not spec.get("ai_generated"):
        errors.append("Deployment spec must be AI-generated as per Constitution section 2.3")
    
    # Check required fields
    required_fields = ["phase", "app_name", "image_name", "deployment_config"]
    for field in required_fields:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    # Check deployment config
    if "deployment_config" in spec:
        config = spec["deployment_config"]
        required_config_fields = ["replicas", "port", "environment", "provider"]
        for field in required_config_fields:
            if field not in config:
                errors.append(f"Missing required config field: {field}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "message": "Deployment spec is valid" if len(errors) == 0 else f"Deployment spec has {len(errors)} issues"
    }

def deploy_to_minikube(manifests_dir: str = "minikube-manifests") -> str:
    """
    Generate command to deploy to Minikube (Phase IV)
    NOTE: This just generates the command - actual execution would require additional tooling
    """
    commands = [
        f"minikube start",
        f"kubectl apply -f {manifests_dir}/",
        f"minikube service {os.listdir(manifests_dir)[0].split('.')[0].replace('service', '')}-service --url"
    ]
    
    return "\n".join([
        "# Run these commands to deploy to Minikube:",
        "# Make sure Minikube is installed and running",
        "minikube start",
        f"kubectl apply -f {manifests_dir}/",
        "# Get the service URL to access the application:",
        "minikube service <service-name> --url"
    ])

def deploy_to_doks(manifests_dir: str = "doks-manifests") -> str:
    """
    Generate command to deploy to DOKS (Phase V)
    NOTE: This just generates the command - actual execution would require additional tooling
    """
    commands = [
        "# Make sure you're logged into DigitalOcean and have a DOKS cluster created",
        f"kubectl apply -f {manifests_dir}/",
        f"kubectl get services -o wide"
    ]
    
    return "\n".join([
        "# Run these commands to deploy to DOKS:",
        "# Make sure you're logged into DigitalOcean and kubectl is configured for your DOKS cluster",
        f"kubectl apply -f {manifests_dir}/",
        "# Check the service to see the external IP/URL:",
        "kubectl get services -o wide"
    ])