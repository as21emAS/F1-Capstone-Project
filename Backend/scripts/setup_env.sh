#Mac/Linux
#!/bin/bash

# Check if .env already exists
if [ -f .env ]; then
    echo ".env file already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo " X Setup cancelled"
        exit 1
    fi
fi

# Copy .env.example to .env
echo "Creating .env file from .env.example..."
cp .env.example .env

# Generate a secure SECRET_KEY
echo "Generating secure SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
if [ -z "$SECRET_KEY" ]; then
    echo "Could not generate SECRET_KEY"
    echo "Please manually add a SECRET_KEY to your .env file"
else
    # Replace placeholder with actual secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-minimum-32-characters/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-minimum-32-characters/$SECRET_KEY/" .env
    fi
    echo "SECRET_KEY generated"
fi

echo ""
echo "Setup complete"
echo ""
echo "Next steps:"
echo "1. Edit Backend/.env and add your:"
echo "   - DATABASE_URL (PostgreSQL connection string)"
echo "   - OPENWEATHER_API_KEY (get free key at https://openweathermap.org/api)"
echo ""
echo "2. Install Python dependencies:"
echo "   python -m venv venv"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Set up PostgreSQL database:"
echo "   createdb f1_predictor_dev"
echo ""

# To make it executable when you have access to those systems
# (On Mac/Linux):
# chmod +x Backend/scripts/setup_env.sh
