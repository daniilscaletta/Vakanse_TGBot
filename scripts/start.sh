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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Docker is running
check_docker() {
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Function to check environment file
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f env.example ]; then
            cp env.example .env
            print_success ".env file created from template"
            print_warning "Please edit .env file with your actual configuration"
            exit 1
        else
            print_error ".env.example file not found. Please create .env file manually."
            exit 1
        fi
    fi

    # Check if BOT_TOKEN is set
    if ! grep -q "BOT_TOKEN=" .env || grep -q "BOT_TOKEN=$" .env; then
        print_error "BOT_TOKEN is not set in .env file"
        exit 1
    fi
}

# Function to create logs directory
create_logs_dir() {
    if [ ! -d logs ]; then
        mkdir -p logs
        print_success "Created logs directory"
    fi
}

# Function to stop existing containers
stop_containers() {
    print_status "Stopping existing containers..."
    docker-compose down --remove-orphans
    print_success "Containers stopped"
}

# Function to build and start containers
start_containers() {
    print_status "Building and starting containers..."
    docker-compose up --build -d

    if [ $? -eq 0 ]; then
        print_success "Containers started successfully"
    else
        print_error "Failed to start containers"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    docker-compose logs -f
}

# Function to show status
show_status() {
    print_status "Container status:"
    docker-compose ps
}

# Function to show health check
check_health() {
    print_status "Checking application health..."
    sleep 10  # Wait for application to start

    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Application is healthy"
        print_success "API is available at http://localhost:8000"
        print_success "Health check endpoint: http://localhost:8000/health"
    else
        print_warning "Health check failed. Application might still be starting..."
    fi
}

# Main function
main() {
    print_status "Starting Vakanse Telegram Bot..."

    # Check prerequisites
    check_docker
    check_env
    create_logs_dir

    # Stop existing containers
    stop_containers

    # Start containers
    start_containers

    # Show status
    show_status

    # Check health
    check_health

    print_success "Setup complete!"
    print_status "Use 'docker-compose logs -f' to view logs"
    print_status "Use 'docker-compose down' to stop the application"
}

# Handle command line arguments
case "${1:-}" in
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "stop")
        stop_containers
        ;;
    "restart")
        stop_containers
        start_containers
        show_status
        check_health
        ;;
    "health")
        check_health
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Start the application"
        echo "  logs       Show container logs"
        echo "  status     Show container status"
        echo "  stop       Stop containers"
        echo "  restart    Restart containers"
        echo "  health     Check application health"
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
