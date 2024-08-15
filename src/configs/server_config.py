import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

SERVER_HOST: Final = os.environ.get('SERVER_HOST')
SERVER_PORT: Final = int(os.environ.get('SERVER_PORT'))
