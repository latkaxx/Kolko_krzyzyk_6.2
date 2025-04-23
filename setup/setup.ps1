$python = "python"

# Check if "python" is available
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    $python = "python3"
}

# Check if fallback exists
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed on this system."
    exit 1
}

# Create and activate virtual environment
& $python -m venv env

# Activation differs depending on shell
& ".\env\Scripts\Activate.ps1"

# Install dependencies
pip install -r requirements.txt

