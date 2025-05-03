import logging
import yaml

# Carrega configurações do YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Configura o logger
logging.basicConfig(
    filename=config['logging']['file'],
    level=getattr(logging, config['logging']['level']),
    format=config['logging']['format']
)

logger = logging.getLogger(__name__)
