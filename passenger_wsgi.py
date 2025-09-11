import sys, os

# Add project path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application  # Flask needs "application"
