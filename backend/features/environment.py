# features/environment.py

import sys
import os

def before_scenario(context, scenario):
    # Initialize product_info before each scenario
    context.product_info = {}

# environment.py

def before_all(context):
    # Calculate the path to the 'src' directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_path = os.path.join(project_root, 'src')
    
    # Add the 'src' directory to the Python path if it's not already there
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Now you can import modules from 'src'
    from src.util.config import load_configuration
    config_path = os.path.join(src_path, 'config', 'halal_config.json')
    load_configuration(config_path)
    print('Configuration loaded')
