from os import getcwd
import re
import shutil
import tomlkit
from pathlib import Path
from typer import Typer, secho


BASE_DIR = Path(__file__).resolve().parent.parent

app = Typer()

@app.command('cp')
def copy(name: str, dest: Path | None = None, desc: str | None = None):
    if re.match(r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', name, re.IGNORECASE) is None:
        secho(f"'{name}' is not a valid package name.", fg='red', err=True)
        exit(1)
    dest = Path(dest).resolve() if dest is not None else BASE_DIR.parent / name
    if dest.exists() and dest.stat().st_size:
        secho(f"Directory '{dest}' exists and is not empty.", fg='red', err=True)
        exit(1)
    shutil.copytree(BASE_DIR, dest, ignore=shutil.ignore_patterns('*pyc', '__pycache__', '.git', '.venv', 'dist', 'scripts'))
    with open(dest / 'README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"# {name}\n")
    pyproject_toml = tomlkit.parse((dest / 'pyproject.toml').read_text(encoding='utf-8'))
    pyproject_toml['project']['name'] = name
    cli_deps = ('tomlkit', 'typer')
    dependencies = tomlkit.array().multiline(True)
    dependencies.extend(
        dep for dep in pyproject_toml['project']['dependencies']
        if not str(dep).strip().startswith(cli_deps)
    )
    pyproject_toml['project']['dependencies'] = dependencies

    if desc is not None:
        pyproject_toml['project']['description'] = desc

    pyproject_toml.pop('build-system', None)
    pyproject_toml.pop('tool', None)
    pyproject_toml['project'].pop('scripts', None)

    with open(dest / 'pyproject.toml', 'w', encoding='utf-8') as file:
        file.write(tomlkit.dumps(pyproject_toml))

    secho(f"Django project '{name}' successfully created at '{dest.parent}'", fg='white')

@app.command('--version')
def version():
    version = tomlkit.parse((BASE_DIR / 'pyproject.toml').read_text(encoding='utf-8'))['project']['version'] or '0.1.0'
    secho(f"Django scaffold version {version}.")

def main():
    app()

if __name__ == '__main__':
    main()
