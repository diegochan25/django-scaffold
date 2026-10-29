from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django_vite.templatetags.django_vite import vite_asset, vite_hmr_client
from django.utils.html import format_html
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader, pass_context
from config.settings.base import BASE_DIR

JINJA2_DIR = BASE_DIR / 'jinja2'
GLOBAL_PREFIX = 'global'
APP_PREFIX = 'app.'
DELIMITER = '::'


def _current_app_label(context):
    filename = context.environment.loader.get_source(context.environment, context.name)[1]
    if filename is None:
        raise RuntimeError(f"Cannot resolve the app of template '{context.name}'")

    filename = Path(filename).resolve()
    matches = [
        config for config in apps.get_app_configs()
        if filename.is_relative_to(Path(config.path).resolve())
    ]
    if not matches:
        raise RuntimeError(f"Template '{context.name}' does not belong to an installed app")

    return max(matches, key=lambda config: len(config.path)).label


def _app_resolver(kind):
    @pass_context
    def resolve(context, path):
        return f'{APP_PREFIX}{_current_app_label(context)}{DELIMITER}{kind}/{path}'
    return resolve


def _global_resolver(kind):
    def resolve(path):
        return f'{GLOBAL_PREFIX}{DELIMITER}{kind}/{path}'
    return resolve


layout = _app_resolver('layouts')
macro = _app_resolver('macros')
partial = _app_resolver('partials')

global_layout = _global_resolver('layouts')
global_macro = _global_resolver('macros')
global_partial = _global_resolver('partials')

def vite_assets(path='src/main.js'):
    return format_html('{}{}', vite_hmr_client(), vite_asset(path))


def browser_reload():
    if not apps.is_installed('django_browser_reload'):
        return ''
    from django_browser_reload.jinja import django_browser_reload_script
    return django_browser_reload_script()


def _scoped_loader():
    mapping = {GLOBAL_PREFIX: FileSystemLoader(JINJA2_DIR)}
    for config in apps.get_app_configs():
        mapping[f'{APP_PREFIX}{config.label}'] = FileSystemLoader(Path(config.path) / 'jinja2' / config.label)
    return PrefixLoader(mapping, delimiter=DELIMITER)

def environment(**options):
    options['loader'] = ChoiceLoader([options['loader'], _scoped_loader()])
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'layout': layout,
        'macro': macro,
        'partial': partial,
        'global_layout': global_layout,
        'global_macro': global_macro,
        'global_partial': global_partial,
        'vite_assets': vite_assets,
        'browser_reload': browser_reload,
        'now': timezone.now,
        'DEBUG': settings.DEBUG
    })
    return env
