#!/bin/bash
# Universal Deployment Scripts for NtandoComputer Enhanced
# Supports: Render.com, Heroku, AWS, Azure, GCP, Docker, VPS

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11 or higher."
        exit 1
    fi
    
    print_status "Dependencies check passed!"
}

# Function to setup local environment
setup_local() {
    print_header "Setting up Local Development Environment"
    
    print_status "Creating virtual environment..."
    python3 -m venv ntando_env
    source ntando_env/bin/activate
    
    print_status "Installing dependencies..."
    pip install -r requirements_universal.txt
    
    print_status "Creating storage directories..."
    mkdir -p storage/{apps,users,backups,logs,temp,desktops,packages,media}
    
    print_status "Initializing database..."
    python3 -c "
from computer_enhanced import UniversalComputerSystem
computer = UniversalComputerSystem()
print('Database initialized successfully!')
"
    
    print_status "Starting local server..."
    python3 computer_enhanced.py
}

# Function to deploy to Render.com
deploy_render() {
    print_header "Deploying to Render.com"
    
    print_warning "Make sure you have the Render CLI installed and authenticated."
    
    print_status "Preparing for Render deployment..."
    
    # Create render.yaml if it doesn't exist
    if [ ! -f render.yaml ]; then
        cp deploy_universal.yaml render.yaml
        print_status "Created render.yaml configuration file"
    fi
    
    print_status "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
    
    print_status "Pushing to Render..."
    # Note: This would require the user to have Render CLI setup
    echo "To complete Render deployment:"
    echo "1. Run: git remote add render <your-render-git-url>"
    echo "2. Run: git push render main"
    echo "3. Or use the Render web dashboard to connect your repository"
    
    print_status "Render deployment preparation complete!"
}

# Function to deploy to Heroku
deploy_heroku() {
    print_header "Deploying to Heroku"
    
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is not installed. Please install it first."
        exit 1
    fi
    
    print_status "Creating Heroku app..."
    heroku create ntandocomputer-universal
    
    print_status "Setting environment variables..."
    heroku config:set DEPLOYMENT_ENV=heroku
    heroku config:set FLASK_ENV=production
    heroku config:set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    print_status "Deploying to Heroku..."
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    print_status "Heroku deployment complete!"
}

# Function to deploy with Docker
deploy_docker() {
    print_header "Deploying with Docker"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    print_status "Building Docker image..."
    docker build -f Dockerfile_universal -t ntandocomputer-universal .
    
    print_status "Running Docker container..."
    docker run -d \
        --name ntandocomputer-universal \
        -p 5001:5001 \
        -v $(pwd)/storage:/app/storage \
        -e DEPLOYMENT_ENV=docker \
        -e SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))") \
        ntandocomputer-universal
    
    print_status "Docker deployment complete!"
    print_status "Access your NtandoComputer at: http://localhost:5001"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_header "Deploying with Docker Compose"
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install it first."
        exit 1
    fi
    
    print_status "Starting services with Docker Compose..."
    docker-compose -f docker-compose_universal.yml up -d
    
    print_status "Docker Compose deployment complete!"
    print_status "Access your NtandoComputer at: http://localhost:5001"
    print_status "Redis is available at: localhost:6379"
    print_status "PostgreSQL is available at: localhost:5432"
}

# Function to deploy to VPS
deploy_vps() {
    print_header "Deploying to VPS"
    
    print_warning "This script assumes you have SSH access to your VPS."
    
    echo "Enter your VPS IP address:"
    read vps_ip
    
    echo "Enter your VPS username:"
    read vps_user
    
    print_status "Deploying to VPS at $vps_ip..."
    
    # Create deployment script for VPS
    cat > vps_deploy.sh << 'EOF'
#!/bin/bash
# VPS Deployment Script

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor

# Create ntando user
sudo useradd -m -s /bin/bash ntando
sudo usermod -aG sudo ntando

# Setup application directory
sudo -u ntando mkdir -p /home/ntando/ntandocomputer
cd /home/ntando/ntandocomputer

# Clone or copy application files
# git clone <your-repo> .

# Setup virtual environment
sudo -u ntando python3 -m venv ntando_env
sudo -u ntando ntando_env/bin/pip install -r requirements_universal.txt

# Create storage directories
sudo -u ntando mkdir -p storage/{apps,users,backups,logs,temp,desktops,packages,media}

# Setup systemd service
sudo tee /etc/systemd/system/ntandocomputer.service > /dev/null << 'EOS'
[Unit]
Description=NtandoComputer Universal
After=network.target

[Service]
Type=simple
User=ntando
WorkingDirectory=/home/ntando/ntandocomputer
Environment=DEPLOYMENT_ENV=vps
Environment=FLASK_ENV=production
ExecStart=/home/ntando/ntandocomputer/ntando_env/bin/python computer_enhanced.py
Restart=always

[Install]
WantedBy=multi-user.target
EOS

# Enable and start service
sudo systemctl enable ntandocomputer
sudo systemctl start ntandocomputer

echo "VPS deployment complete!"
EOF
    
    # Copy and execute deployment script on VPS
    scp vps_deploy.sh ${vps_user}@${vps_ip}:~/
    ssh ${vps_user}@${vps_ip} "chmod +x ~/vps_deploy.sh && ~/vps_deploy.sh"
    
    print_status "VPS deployment complete!"
    print_status "Access your NtandoComputer at: http://$vps_ip:5001"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  local           Setup local development environment"
    echo "  render          Deploy to Render.com"
    echo "  heroku          Deploy to Heroku"
    echo "  docker          Deploy with Docker"
    echo "  docker-compose  Deploy with Docker Compose"
    echo "  vps             Deploy to VPS"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local"
    echo "  $0 docker"
    echo "  $0 render"
}

# Main script logic
case "${1:-help}" in
    local)
        check_dependencies
        setup_local
        ;;
    render)
        check_dependencies
        deploy_render
        ;;
    heroku)
        check_dependencies
        deploy_heroku
        ;;
    docker)
        check_dependencies
        deploy_docker
        ;;
    docker-compose)
        check_dependencies
        deploy_docker_compose
        ;;
    vps)
        check_dependencies
        deploy_vps
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac