#!/bin/bash

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

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.9+ first."
        exit 1
    fi

    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $python_version found"
}

# Function to create virtual environment
create_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    # Upgrade pip
    pip install --upgrade pip

    # Install production dependencies
    pip install -r requirements.txt

    # Install development dependencies
    pip install -r requirements-dev.txt

    print_success "Dependencies installed"
}

# Function to setup pre-commit hooks
setup_precommit() {
    print_status "Setting up pre-commit hooks..."

    # Install pre-commit hooks
    pre-commit install

    # Run pre-commit on all files
    pre-commit run --all-files

    print_success "Pre-commit hooks configured"
}

# Function to format code
format_code() {
    print_status "Formatting code..."

    # Run black
    black app/ tests/

    # Run isort
    isort app/ tests/

    print_success "Code formatted"
}

# Function to run linting
run_linting() {
    print_status "Running linting..."

    # Run flake8
    flake8 app/ tests/

    # Run mypy
    mypy app/

    print_success "Linting completed"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."

    # Run pytest with coverage
    pytest tests/ -v --cov=app --cov-report=term-missing

    print_success "Tests completed"
}

# Function to create .env file
create_env() {
    if [ ! -f .env ]; then
        print_status "Creating .env file..."
        if [ -f env.example ]; then
            cp env.example .env
            print_success ".env file created from template"
            print_warning "Please edit .env file with your actual configuration"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    else
        print_warning ".env file already exists"
    fi
}

# Main function
main() {
    print_status "Setting up development environment..."

    # Check prerequisites
    check_python

    # Create virtual environment
    create_venv

    # Activate virtual environment
    activate_venv

    # Install dependencies
    install_dependencies

    # Setup pre-commit hooks
    setup_precommit

    # Format code
    format_code

    # Run linting
    run_linting

    # Run tests
    run_tests

    # Create .env file
    create_env

    print_success "Development environment setup complete!"
    print_status "To activate the virtual environment: source venv/bin/activate"
    print_status "To run the application: python -m app.main"
    print_status "To run tests: pytest"
    print_status "To format code: black app/ tests/ && isort app/ tests/"
    print_status "To run linting: flake8 app/ tests/ && mypy app/"
}

# Handle command line arguments
case "${1:-}" in
    "format")
        activate_venv
        format_code
        ;;
    "lint")
        activate_venv
        run_linting
        ;;
    "test")
        activate_venv
        run_tests
        ;;
    "precommit")
        activate_venv
        setup_precommit
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Setup complete development environment"
        echo "  format     Format code with black and isort"
        echo "  lint       Run linting with flake8 and mypy"
        echo "  test       Run tests with pytest"
        echo "  precommit  Setup pre-commit hooks"
        echo "  help       Show this help message"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
