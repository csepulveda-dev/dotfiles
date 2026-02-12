#!/bin/bash

# Core Bookings Quality Check Script
# Runs comprehensive code quality validation and automated fixes

set -e

PROJECT_ROOT=$(pwd)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔍 Starting Core Bookings quality check..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a Gradle project
if [ ! -f "build.gradle" ] && [ ! -f "build.gradle.kts" ]; then
    print_error "Not in a Gradle project root directory"
    exit 1
fi

# Parse command line arguments
RUN_DETEKT=true
RUN_TESTS=true
RUN_COVERAGE=true
UPDATE_LOCKS=false
AUTO_FIX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --detekt-only)
            RUN_TESTS=false
            RUN_COVERAGE=false
            shift
            ;;
        --tests-only)
            RUN_DETEKT=false
            RUN_COVERAGE=false
            shift
            ;;
        --update-locks)
            UPDATE_LOCKS=true
            shift
            ;;
        --fix)
            AUTO_FIX=true
            shift
            ;;
        --no-detekt)
            RUN_DETEKT=false
            shift
            ;;
        *)
            print_warning "Unknown option $1"
            shift
            ;;
    esac
done

# Update Gradle lockfiles if requested
if [ "$UPDATE_LOCKS" = true ]; then
    print_status "Updating Gradle lockfiles..."
    ./gradlew dependencies --write-locks
    print_success "Gradle lockfiles updated"
fi

# Run Detekt static analysis
if [ "$RUN_DETEKT" = true ]; then
    print_status "Running Detekt static analysis..."
    
    if [ "$AUTO_FIX" = true ]; then
        print_status "Auto-fixing Detekt issues..."
        ./gradlew detekt --auto-correct || {
            print_warning "Detekt auto-fix completed with warnings"
        }
    fi
    
    ./gradlew detekt || {
        print_error "Detekt found issues that need manual attention"
        echo "Run with --fix to apply automatic fixes"
        exit 1
    }
    
    print_success "Detekt analysis passed"
fi

# Run tests
if [ "$RUN_TESTS" = true ]; then
    print_status "Running tests..."
    
    ./gradlew test || {
        print_error "Tests failed"
        exit 1
    }
    
    print_success "All tests passed"
fi

# Run test coverage analysis
if [ "$RUN_COVERAGE" = true ]; then
    print_status "Generating test coverage report..."
    
    ./gradlew jacocoTestReport || {
        print_warning "Coverage report generation encountered issues"
    }
    
    # Check for coverage threshold (if configured)
    if ./gradlew jacocoTestCoverageVerification 2>/dev/null; then
        print_success "Test coverage meets threshold"
    else
        print_warning "Test coverage below threshold"
    fi
fi

# Architecture tests (if they exist)
if ./gradlew tasks --all | grep -q "architectureTest"; then
    print_status "Running architecture tests..."
    
    ./gradlew architectureTest || {
        print_error "Architecture tests failed"
        exit 1
    }
    
    print_success "Architecture tests passed"
fi

# Final summary
echo ""
print_success "✅ Quality check completed successfully!"
echo ""
echo "Summary of checks performed:"
[ "$RUN_DETEKT" = true ] && echo "  ✅ Detekt static analysis"
[ "$RUN_TESTS" = true ] && echo "  ✅ Unit tests"
[ "$RUN_COVERAGE" = true ] && echo "  ✅ Test coverage analysis"
[ "$UPDATE_LOCKS" = true ] && echo "  ✅ Gradle lockfiles updated"

echo ""
echo "To view detailed reports:"
echo "  • Detekt: build/reports/detekt/detekt.html"
echo "  • Test results: build/reports/tests/test/index.html"
echo "  • Coverage: build/reports/jacoco/test/html/index.html"