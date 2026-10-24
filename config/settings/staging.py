from pathlib import Path
from environ import Env

Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env.staging')

from config.settings.base import *