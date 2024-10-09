#!/bin/bash

# Exit the script if any command fails
set -e

# Install Python 3.12
echo "Installing Python 3.12..."
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Check if Python 3.12 was installed successfully
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 could not be installed."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment 'venv_mid_sem_exam'..."
python3.12 -m venv venv_mid_sem_exam

# Activate virtual environment
echo "Activating virtual environment..."
source venv_mid_sem_exam/bin/activate

# Install required Python packages
if [ -f "requirements.txt" ]; then
    echo "Installing required Python packages..."
    pip install -r requirements.txt
else
    echo "requirements.txt file not found."
    exit 1
fi

echo "Installation completed successfully."

# Instructions to activate the virtual environment
echo "To activate the virtual environment, run:"
echo "source venv_mid_sem_exam/bin/activate"
