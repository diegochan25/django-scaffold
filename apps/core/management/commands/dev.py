import os
import shutil
import subprocess
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


FRONTEND_DIR = settings.BASE_DIR / 'frontend'
VITE_BIN = FRONTEND_DIR / 'node_modules' / 'vite' / 'bin' / 'vite.js'

class Command(BaseCommand):
    help = 'Run the Vite dev server alongside the Django development server.'

    def add_arguments(self, parser):
        parser.add_argument('addrport', nargs='?', help='Optional port number, or ipaddr:port')

    def handle(self, *args, **options):
        # runserver's autoreloader re-runs this command in a child process with RUN_MAIN set;
        # only the parent should own the Vite process.
        if os.environ.get('RUN_MAIN') == 'true':
            return self._runserver(options)

        node = shutil.which('node')
        if node is None:
            raise CommandError('Node.js is required to run the Vite dev server.')
        if not VITE_BIN.exists():
            raise CommandError(f'Vite is not installed. Run `npm install` in {FRONTEND_DIR}.')

        vite = subprocess.Popen([node, str(VITE_BIN)], cwd=FRONTEND_DIR)
        try:
            self._runserver(options)
        finally:
            vite.terminate()
            try:
                vite.wait(timeout=5)
            except subprocess.TimeoutExpired:
                vite.kill()

    def _runserver(self, options):
        args = [options['addrport']] if options['addrport'] else []
        call_command('runserver', *args)
