#Mac/Linux
#!/bin/bash

# Check if .env already exists
if [ -f .env ]; then
    echo ".env file already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "X Setup cancelled"
        exit 1
    fi
fi

# Copy .env.example to .env
echo "Creating .env file from .env.example..."
cp .env.example .env

echo ""
echo "Setup complete"
echo ""
echo "Next steps:"
echo "1. Review Frontend/.env (default values should work for local development)"
echo ""
echo "2. Install Node dependencies:"
echo "   npm install"
echo ""
echo "3. Start development server:"
echo "   npm run dev"
echo ""

# To make it executable when you have access to those systems
# (On Mac/Linux):
# chmod +x Frontend/scripts/setup_env.sh
