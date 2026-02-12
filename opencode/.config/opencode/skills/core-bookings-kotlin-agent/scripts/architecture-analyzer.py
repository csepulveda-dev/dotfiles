#!/usr/bin/env python3

"""
Core Bookings Architecture Analyzer

Analyzes Kotlin codebase for architecture compliance and provides recommendations
for migrating from current Handler->Store->Client pattern to target
Handler->Operations->Stores pattern.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import re

class ArchitectureAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.src_root = self.project_root / "src" / "main" / "kotlin"
        
        # Package patterns
        self.handler_pattern = r".*\.handlers\..*"
        self.operations_pattern = r".*\.operations\..*"
        self.store_pattern = r".*\.stores\..*"
        self.client_pattern = r".*\.clients\..*"
        self.model_pattern = r".*\.models\..*"
        
    def analyze(self, package_filter: Optional[str] = None) -> Dict:
        """Analyze the codebase architecture."""
        print("🔍 Analyzing Core Bookings architecture...")
        
        kotlin_files = self._find_kotlin_files(package_filter)
        
        analysis = {
            "summary": {
                "total_files": len(kotlin_files),
                "handlers": 0,
                "operations": 0,
                "stores": 0,
                "clients": 0,
                "models": 0,
                "other": 0
            },
            "architecture_violations": [],
            "missing_operations": [],
            "migration_opportunities": [],
            "token_usage": {
                "token_first": 0,
                "guid_only": 0,
                "dual_support": 0
            },
            "testing_coverage": {
                "has_tests": 0,
                "missing_tests": 0,
                "architecture_tests": False
            },
            "conventions": {
                "follows_naming": 0,
                "violates_naming": 0,
                "uses_immutable_collections": 0,
                "uses_mutable_collections": 0
            }
        }
        
        for file_path in kotlin_files:
            self._analyze_file(file_path, analysis)
        
        self._check_architecture_tests(analysis)
        
        return analysis
    
    def _find_kotlin_files(self, package_filter: Optional[str]) -> List[Path]:
        """Find all Kotlin files in the project."""
        kotlin_files = []
        
        if not self.src_root.exists():
            print(f"❌ Source directory not found: {self.src_root}")
            return kotlin_files
        
        for file_path in self.src_root.rglob("*.kt"):
            if package_filter and package_filter not in str(file_path):
                continue
            kotlin_files.append(file_path)
        
        return kotlin_files
    
    def _analyze_file(self, file_path: Path, analysis: Dict):
        """Analyze a single Kotlin file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            print(f"⚠️  Could not read file (encoding issue): {file_path}")
            return
        
        # Determine file category
        relative_path = str(file_path.relative_to(self.project_root))
        category = self._categorize_file(relative_path)
        analysis["summary"][category] += 1
        
        # Check naming conventions
        if self._follows_naming_convention(file_path.name, category):
            analysis["conventions"]["follows_naming"] += 1
        else:
            analysis["conventions"]["violates_naming"] += 1
        
        # Analyze content
        self._analyze_file_content(content, relative_path, analysis)
        
        # Check for corresponding test file
        if self._has_test_file(file_path):
            analysis["testing_coverage"]["has_tests"] += 1
        else:
            analysis["testing_coverage"]["missing_tests"] += 1
    
    def _categorize_file(self, file_path: str) -> str:
        """Categorize a file based on its path."""
        if re.match(self.handler_pattern, file_path):
            return "handlers"
        elif re.match(self.operations_pattern, file_path):
            return "operations"
        elif re.match(self.store_pattern, file_path):
            return "stores"
        elif re.match(self.client_pattern, file_path):
            return "clients"
        elif re.match(self.model_pattern, file_path):
            return "models"
        else:
            return "other"
    
    def _follows_naming_convention(self, filename: str, category: str) -> bool:
        """Check if file follows naming conventions."""
        conventions = {
            "handlers": r".*Handler\.kt$",
            "operations": r".*Operations?\.kt$",
            "stores": r".*Store\.kt$",
            "clients": r".*Client\.kt$",
            "models": r"^[A-Z][a-zA-Z]*\.kt$"
        }
        
        if category not in conventions:
            return True
        
        return bool(re.match(conventions[category], filename))
    
    def _analyze_file_content(self, content: str, file_path: str, analysis: Dict):
        """Analyze the content of a Kotlin file."""
        # Check for token usage patterns
        if "Token" in content and "GUID" in content:
            analysis["token_usage"]["dual_support"] += 1
        elif "Token" in content:
            analysis["token_usage"]["token_first"] += 1
        elif "UUID" in content or "GUID" in content:
            analysis["token_usage"]["guid_only"] += 1
        
        # Check for collection types
        if re.search(r"MutableList|MutableMap|MutableSet", content):
            analysis["conventions"]["uses_mutable_collections"] += 1
        elif re.search(r"\bList<|Map<|Set<", content):
            analysis["conventions"]["uses_immutable_collections"] += 1
        
        # Check architecture violations
        if "handlers" in file_path.lower():
            self._check_handler_violations(content, file_path, analysis)
        elif "stores" in file_path.lower():
            self._check_store_violations(content, file_path, analysis)
    
    def _check_handler_violations(self, content: str, file_path: str, analysis: Dict):
        """Check for architecture violations in handler files."""
        # Handlers should not directly import from clients
        if re.search(r"import.*\.clients\.", content):
            analysis["architecture_violations"].append({
                "file": file_path,
                "type": "handler_to_client",
                "message": "Handler directly imports client - should go through operations/stores"
            })
        
        # Check if handler directly calls stores (should have operations layer)
        if re.search(r"\.stores\.", content) and "operations" not in content.lower():
            analysis["missing_operations"].append({
                "file": file_path,
                "message": "Handler directly uses store - missing operations layer"
            })
    
    def _check_store_violations(self, content: str, file_path: str, analysis: Dict):
        """Check for architecture violations in store files."""
        # Check for business logic in stores (should be in operations)
        business_logic_patterns = [
            r"if\s*\([^)]*\)\s*{[^}]*business",
            r"when\s*\([^)]*\)\s*{[^}]*calculate",
            r"validate[A-Z]\w*\(",
        ]
        
        for pattern in business_logic_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                analysis["migration_opportunities"].append({
                    "file": file_path,
                    "type": "extract_business_logic",
                    "message": "Business logic found in store - should be moved to operations"
                })
                break
    
    def _has_test_file(self, file_path: Path) -> bool:
        """Check if a corresponding test file exists."""
        relative_path = file_path.relative_to(self.src_root)
        test_paths = [
            self.project_root / "src" / "test" / "kotlin" / relative_path.with_name(f"{relative_path.stem}Test.kt"),
            self.project_root / "src" / "test" / "kotlin" / relative_path.parent / f"{relative_path.stem}Test.kt"
        ]
        
        return any(test_path.exists() for test_path in test_paths)
    
    def _check_architecture_tests(self, analysis: Dict):
        """Check if architecture tests exist."""
        arch_test_patterns = [
            "ArchitectureTest.kt",
            "ArchUnitTest.kt",
            "*ArchTest.kt"
        ]
        
        for pattern in arch_test_patterns:
            if list(self.project_root.rglob(pattern)):
                analysis["testing_coverage"]["architecture_tests"] = True
                break
    
    def generate_migration_plan(self, analysis: Dict) -> List[Dict]:
        """Generate a migration plan based on the analysis."""
        plan = []
        
        # Step 1: Create missing operations layer
        if analysis["summary"]["operations"] == 0 and analysis["summary"]["stores"] > 0:
            plan.append({
                "step": 1,
                "title": "Create Operations Layer",
                "description": "Extract business logic from stores into operations layer",
                "commands": ["/cb-create-operations <feature-name> for each store"],
                "files_affected": analysis["summary"]["stores"]
            })
        
        # Step 2: Fix architecture violations
        if analysis["architecture_violations"]:
            plan.append({
                "step": 2,
                "title": "Fix Architecture Violations",
                "description": "Remove direct dependencies between inappropriate layers",
                "violations": analysis["architecture_violations"]
            })
        
        # Step 3: Migrate to token-first APIs
        if analysis["token_usage"]["guid_only"] > 0:
            plan.append({
                "step": 3,
                "title": "Migrate to Token-First APIs",
                "description": "Convert GUID-only APIs to token-first with GUID support",
                "commands": ["/cb-create-store <entity> --with-guid"]
            })
        
        # Step 4: Add missing tests
        if analysis["testing_coverage"]["missing_tests"] > 0:
            plan.append({
                "step": 4,
                "title": "Add Missing Tests",
                "description": f"Create tests for {analysis['testing_coverage']['missing_tests']} files",
                "commands": ["/cb-testing-suite <class-name>"]
            })
        
        # Step 5: Add architecture tests
        if not analysis["testing_coverage"]["architecture_tests"]:
            plan.append({
                "step": 5,
                "title": "Add Architecture Tests",
                "description": "Create ArchUnit tests to enforce layer boundaries",
                "commands": ["/cb-testing-suite --architecture"]
            })
        
        return plan
    
    def print_report(self, analysis: Dict):
        """Print a formatted analysis report."""
        print("\n" + "="*60)
        print("🏗️  CORE BOOKINGS ARCHITECTURE ANALYSIS REPORT")
        print("="*60)
        
        # Summary
        print(f"\n📊 SUMMARY:")
        summary = analysis["summary"]
        print(f"  Total files analyzed: {summary['total_files']}")
        print(f"  Handlers: {summary['handlers']}")
        print(f"  Operations: {summary['operations']}")
        print(f"  Stores: {summary['stores']}")
        print(f"  Clients: {summary['clients']}")
        print(f"  Models: {summary['models']}")
        print(f"  Other: {summary['other']}")
        
        # Architecture status
        print(f"\n🏛️  ARCHITECTURE STATUS:")
        if summary["operations"] == 0 and summary["stores"] > 0:
            print("  ❌ Missing operations layer (current: Handler->Store->Client)")
            print("  🎯 Target: Handler->Operations->Stores")
        elif summary["operations"] > 0:
            print("  ✅ Operations layer present (target architecture)")
        
        # Token usage
        print(f"\n🏷️  TOKEN USAGE:")
        token = analysis["token_usage"]
        print(f"  Token-first: {token['token_first']}")
        print(f"  Dual support: {token['dual_support']}")
        print(f"  GUID-only: {token['guid_only']}")
        
        # Violations
        if analysis["architecture_violations"]:
            print(f"\n⚠️  ARCHITECTURE VIOLATIONS ({len(analysis['architecture_violations'])}):")
            for violation in analysis["architecture_violations"]:
                print(f"  • {violation['file']}: {violation['message']}")
        
        # Migration opportunities
        if analysis["migration_opportunities"]:
            print(f"\n🔄 MIGRATION OPPORTUNITIES ({len(analysis['migration_opportunities'])}):")
            for opportunity in analysis["migration_opportunities"]:
                print(f"  • {opportunity['file']}: {opportunity['message']}")
        
        # Testing coverage
        print(f"\n🧪 TESTING COVERAGE:")
        testing = analysis["testing_coverage"]
        print(f"  With tests: {testing['has_tests']}")
        print(f"  Missing tests: {testing['missing_tests']}")
        print(f"  Architecture tests: {'✅' if testing['architecture_tests'] else '❌'}")
        
        # Conventions
        print(f"\n📋 CONVENTIONS:")
        conv = analysis["conventions"]
        print(f"  Follows naming: {conv['follows_naming']}")
        print(f"  Violates naming: {conv['violates_naming']}")
        print(f"  Immutable collections: {conv['uses_immutable_collections']}")
        print(f"  Mutable collections: {conv['uses_mutable_collections']}")
        
        if conv['uses_mutable_collections'] > 0:
            print("  ⚠️  Found mutable collections - should use immutable List/Map")

def main():
    parser = argparse.ArgumentParser(description="Analyze Core Bookings architecture")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--package", help="Filter by package name")
    parser.add_argument("--migration-plan", action="store_true", help="Generate migration plan")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    analyzer = ArchitectureAnalyzer(args.project_root)
    analysis = analyzer.analyze(args.package)
    
    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        analyzer.print_report(analysis)
        
        if args.migration_plan:
            plan = analyzer.generate_migration_plan(analysis)
            if plan:
                print("\n" + "="*60)
                print("🗺️  MIGRATION PLAN")
                print("="*60)
                
                for step in plan:
                    print(f"\nStep {step['step']}: {step['title']}")
                    print(f"  {step['description']}")
                    if 'commands' in step:
                        print("  Commands:")
                        for cmd in step['commands']:
                            print(f"    {cmd}")
                    if 'violations' in step:
                        print(f"  Files to fix: {len(step['violations'])}")
            else:
                print("\n✅ No migration needed - architecture is compliant!")

if __name__ == "__main__":
    main()