#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Vakanse Telegram Bot - Quick Start${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file from template...${NC}"
    cp env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your Telegram bot token${NC}"
    echo ""
fi

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}🐳 Docker detected - Using Docker deployment${NC}"
    echo ""
    echo "Available commands:"
    echo "  ./scripts/start.sh          - Start the application"
    echo "  ./scripts/start.sh logs     - View logs"
    echo "  ./scripts/start.sh stop     - Stop the application"
    echo "  ./scripts/start.sh status   - Check status"
    echo ""
    echo "Or use Makefile commands:"
    echo "  make docker-run             - Start application"
    echo "  make docker-logs            - View logs"
    echo "  make docker-stop            - Stop application"
    echo "  make status                 - Check status"
    echo ""
else
    echo -e "${YELLOW}🐍 Docker not detected - Using local development setup${NC}"
    echo ""
    echo "Available commands:"
    echo "  ./scripts/dev-setup.sh      - Setup development environment"
    echo "  python -m app.main          - Run application locally"
    echo ""
    echo "Or use Makefile commands:"
    echo "  make dev-setup              - Setup development environment"
    echo "  make install                - Install dependencies"
    echo "  make test                   - Run tests"
    echo "  make format                 - Format code"
    echo "  make lint                   - Run linting"
    echo ""
fi

echo -e "${GREEN}📚 For more information, see README.md${NC}"
echo ""
echo -e "${BLUE}🎯 Next steps:${NC}"
echo "1. Edit .env file with your Telegram bot token"
echo "2. Choose your deployment method (Docker or local)"
echo "3. Start the application"
echo ""
