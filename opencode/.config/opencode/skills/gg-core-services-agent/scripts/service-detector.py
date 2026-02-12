#!/usr/bin/env python3

"""
GlossGenius Core Service Context Detector

Automatically detects the current core service context from:
1. Repository directory name (core-{service})
2. Package structure analysis (com.glossgenius.core.{service})
3. Explicit service parameter override
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional, Set
import re

class ServiceDetector:
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root or os.getcwd())
        self.known_services = {
            'bookings', 'payments', 'users', 'inventory', 
            'notifications', 'analytics', 'integrations',
            'reviews', 'marketing', 'reporting', 'search'
        }
        
    def detect_service(self, explicit_service: Optional[str] = None) -> Dict:
        """Detect current core service context."""
        detection_result = {
            "service": None,
            "confidence": 0.0,
            "method": None,
            "package_base": None,
            "repository_path": str(self.project_root),
            "available_services": list(self.known_services)
        }
        
        # 1. Explicit override has highest priority
        if explicit_service:
            if explicit_service in self.known_services:
                detection_result.update({
                    "service": explicit_service,
                    "confidence": 1.0,
                    "method": "explicit_override",
                    "package_base": f"com.glossgenius.core.{explicit_service}"
                })
                return detection_result
            else:
                print(f"Warning: Unknown service '{explicit_service}'. Using auto-detection.")
        
        # 2. Repository name detection
        repo_service = self._detect_from_repository()
        if repo_service:
            detection_result.update({
                "service": repo_service,
                "confidence": 0.9,
                "method": "repository_name",
                "package_base": f"com.glossgenius.core.{repo_service}"
            })
            return detection_result
        
        # 3. Package structure analysis
        package_service = self._detect_from_packages()
        if package_service:
            detection_result.update({
                "service": package_service,
                "confidence": 0.8,
                "method": "package_analysis",
                "package_base": f"com.glossgenius.core.{package_service}"
            })
            return detection_result
        
        # 4. Build file analysis
        gradle_service = self._detect_from_gradle()
        if gradle_service:
            detection_result.update({
                "service": gradle_service,
                "confidence": 0.7,
                "method": "gradle_analysis",
                "package_base": f"com.glossgenius.core.{gradle_service}"
            })
            return detection_result
        
        # 5. Fallback: check for any core-* pattern in path
        path_service = self._detect_from_path()
        if path_service:
            detection_result.update({
                "service": path_service,
                "confidence": 0.6,
                "method": "path_analysis",
                "package_base": f"com.glossgenius.core.{path_service}"
            })
            return detection_result
        
        # No detection possible
        detection_result.update({
            "service": None,
            "confidence": 0.0,
            "method": "no_detection",
            "error": "Could not detect core service context"
        })
        
        return detection_result
    
    def _detect_from_repository(self) -> Optional[str]:
        """Detect service from repository directory name."""
        repo_name = self.project_root.name
        
        # Match core-{service} pattern
        match = re.match(r'^core-([a-zA-Z][a-zA-Z0-9_]*)$', repo_name)
        if match:
            service = match.group(1).lower()
            # Exclude core-api
            if service != 'api' and (service in self.known_services or self._looks_like_service(service)):
                return service
        
        return None
    
    def _detect_from_packages(self) -> Optional[str]:
        """Detect service from package structure in Kotlin files."""
        kotlin_files = list(self.project_root.rglob("*.kt"))
        
        services_found = set()
        for kotlin_file in kotlin_files[:20]:  # Sample first 20 files
            try:
                content = kotlin_file.read_text(encoding='utf-8')
                # Look for package declarations
                package_matches = re.findall(
                    r'package\s+com\.glossgenius\.core\.([a-zA-Z][a-zA-Z0-9_]*)',
                    content
                )
                for match in package_matches:
                    service = match.lower()
                    if service != 'api' and (service in self.known_services or self._looks_like_service(service)):
                        services_found.add(service)
            except (UnicodeDecodeError, OSError):
                continue
        
        # Return most common service found
        if services_found:
            return max(services_found, key=lambda s: self._count_service_references(s))
        
        return None
    
    def _detect_from_gradle(self) -> Optional[str]:
        """Detect service from Gradle build configuration."""
        gradle_files = [
            self.project_root / "build.gradle",
            self.project_root / "build.gradle.kts"
        ]
        
        for gradle_file in gradle_files:
            if gradle_file.exists():
                try:
                    content = gradle_file.read_text()
                    
                    # Look for project name or package references
                    name_matches = re.findall(r'name\s*[=:]\s*["\']core-([a-zA-Z][a-zA-Z0-9_]*)["\']', content)
                    for match in name_matches:
                        service = match.lower()
                        if service != 'api' and (service in self.known_services or self._looks_like_service(service)):
                            return service
                    
                    # Look for main class references
                    main_matches = re.findall(r'com\.glossgenius\.core\.([a-zA-Z][a-zA-Z0-9_]*)', content)
                    for match in main_matches:
                        service = match.lower()
                        if service != 'api' and (service in self.known_services or self._looks_like_service(service)):
                            return service
                            
                except (UnicodeDecodeError, OSError):
                    continue
        
        return None
    
    def _detect_from_path(self) -> Optional[str]:
        """Detect service from any core-* pattern in the full path."""
        path_str = str(self.project_root.resolve())
        
        # Look for core-{service} anywhere in path
        matches = re.findall(r'/core-([a-zA-Z][a-zA-Z0-9_]*)', path_str)
        for match in matches:
            service = match.lower()
            if service != 'api' and (service in self.known_services or self._looks_like_service(service)):
                return service
        
        return None
    
    def _looks_like_service(self, name: str) -> bool:
        """Heuristic to determine if a name looks like a service name."""
        # Basic validation
        if len(name) < 3 or len(name) > 20:
            return False
        
        # Should be alphabetic (with possible underscores)
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            return False
        
        # Exclude obvious non-services
        excluded = {'test', 'tests', 'main', 'src', 'build', 'gradle', 'lib', 'libs'}
        if name.lower() in excluded:
            return False
        
        return True
    
    def _count_service_references(self, service: str) -> int:
        """Count references to a service in the codebase."""
        kotlin_files = list(self.project_root.rglob("*.kt"))
        count = 0
        
        for kotlin_file in kotlin_files[:10]:  # Sample files
            try:
                content = kotlin_file.read_text(encoding='utf-8')
                count += len(re.findall(rf'\.{service}\.', content, re.IGNORECASE))
            except (UnicodeDecodeError, OSError):
                continue
        
        return count
    
    def generate_context(self, detection_result: Dict) -> Dict:
        """Generate complete service context information."""
        if not detection_result["service"]:
            return detection_result
        
        service = detection_result["service"]
        
        context = {
            **detection_result,
            "service_info": {
                "name": service,
                "display_name": service.title(),
                "package_base": f"com.glossgenius.core.{service}",
                "token_prefix": self._to_pascal_case(service),
                "table_prefix": service.lower(),
            },
            "patterns": {
                "domain_package": f"com.glossgenius.core.{service}.models",
                "store_package": f"com.glossgenius.core.{service}.stores", 
                "handler_package": f"com.glossgenius.core.{service}.handlers",
                "operations_package": f"com.glossgenius.core.{service}.operations",
            },
            "database": {
                "schema_prefix": service.lower(),
                "table_naming": "snake_case",
                "token_column": "token",
                "business_token_column": "business_token",
            }
        }
        
        return context
    
    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return ''.join(word.capitalize() for word in snake_str.split('_'))

def main():
    parser = argparse.ArgumentParser(description="Detect GlossGenius core service context")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--service", help="Explicit service override")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--context", action="store_true", help="Generate full context")
    
    args = parser.parse_args()
    
    detector = ServiceDetector(args.project_root)
    detection = detector.detect_service(args.service)
    
    if args.context:
        result = detector.generate_context(detection)
    else:
        result = detection
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["service"]:
            print(f"Detected service: {result['service']}")
            print(f"Method: {result['method']}")
            print(f"Confidence: {result['confidence']:.1%}")
            if result.get("package_base"):
                print(f"Package base: {result['package_base']}")
        else:
            print("Could not detect service context")
            if result.get("error"):
                print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()