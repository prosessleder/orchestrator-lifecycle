#!/usr/bin/env python3
"""Package only declared publication inputs; shared helpers also audit public scope."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = 'publication-files.json'
GENERATED = ('release/paper.pdf', 'release/source-manifest.json', 'release/SHA256SUMS')


def relative_name(name):
    """Require a normalized relative filename, never an escape or credential path."""
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError(f'Unsafe publication path: {name!r}')
    if any(ord(char) < 32 or ord(char) == 127 for char in name):
        raise ValueError(f'Unsafe publication path: {name!r}')
    path = PurePosixPath(name)
    if not path.parts or path.is_absolute() or path.as_posix() != name or '..' in path.parts:
        raise ValueError(f'Unsafe publication path: {name!r}')
    if any(part == '.git' or part.startswith('.env') for part in path.parts):
        raise ValueError(f'Forbidden publication path: {name!r}')
    return name


def safe_path(root, name, required=False):
    """Reject links in every path component before opening any publication file."""
    relative_name(name)
    current = root
    for part in PurePosixPath(name).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink publication path: {name}')
    if current.exists() and not current.is_file():
        raise ValueError(f'Publication path is not a regular file: {name}')
    if required and not current.is_file():
        raise ValueError(f'Missing publication file: {name}')
    return current


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicate_keys)


def load_inventory(root=ROOT):
    data = read_json(safe_path(root, INVENTORY, required=True))
    if not isinstance(data, dict) or set(data) != {
        'format_version', 'source_files', 'repository_only_files'
    } or data['format_version'] != 1:
        raise ValueError('Expected publication inventory format 1')
    for field in ('source_files', 'repository_only_files'):
        names = data[field]
        if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
            raise ValueError(f'Expected a filename list: {field}')
        for name in names:
            relative_name(name)
        if len(names) != len(set(names)):
            raise ValueError(f'Duplicate filenames in {field}')
    required_sources = {INVENTORY, 'scripts/package_release.py', 'release/metadata.json'}
    if not required_sources.issubset(data['source_files']):
        raise ValueError('Source inventory must include its inventory, packager, and metadata')
    metadata = read_json(safe_path(root, 'release/metadata.json', required=True))
    version = metadata.get('version') if isinstance(metadata, dict) else None
    if not isinstance(version, str) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
        raise ValueError('Expected a semantic document version')
    data['prefix'] = f'orchestrator-lifecycle-{version}'
    data['archive'] = f"release/{data['prefix']}-source.zip"
    data['generated_files'] = [*GENERATED, data['archive']]
    groups = [data['source_files'], data['repository_only_files'], data['generated_files']]
    allowed = [name for group in groups for name in group]
    if len(allowed) != len(set(allowed)):
        raise ValueError('Source, repository-only, and generated file groups must be disjoint')
    data['allowed_files'] = set(allowed)
    return data


def check_repository_scope(data, root=ROOT, require_git=True):
    """Check tracked and unignored files; ignored working files are never archive inputs."""
    try:
        probe = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                               text=True, capture_output=True)
        in_repository = probe.returncode == 0 and Path(probe.stdout.strip()).resolve() == root.resolve()
    except FileNotFoundError:
        if (root / '.git').exists():
            raise ValueError('Git is required for public checkout scope checking')
        in_repository = False
    if require_git and not in_repository:
        raise ValueError('Public repository scope checking requires this directory to be a Git root')
    required = set(data['source_files'])
    if in_repository:
        required.update(data['repository_only_files'])
    for name in data['allowed_files']:
        safe_path(root, name, required=name in required)
    if in_repository:
        listing = subprocess.check_output(
            ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root)
        names = {os.fsdecode(name) for name in listing.split(b'\0') if name}
        for name in names:
            safe_path(root, name)
        undeclared = sorted(names - data['allowed_files'])
        if undeclared:
            raise ValueError('Undeclared public files: ' + ', '.join(undeclared))
    return in_repository


def digest_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_release(data, root=ROOT):
    """Require exact archive membership and matching source, archive, and PDF bytes."""
    manifest = read_json(safe_path(root, 'release/source-manifest.json', required=True))
    if not isinstance(manifest, dict) or set(manifest) != set(data['source_files']):
        raise ValueError('Source manifest does not match the explicit source inventory')
    for name, digest in manifest.items():
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'Invalid source digest: {name}')
        if digest_file(safe_path(root, name, required=True)) != digest:
            raise ValueError(f'Source manifest byte mismatch: {name}')

    checksum_path = safe_path(root, 'release/SHA256SUMS', required=True)
    checksums = {}
    for line in checksum_path.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
        if not match or match[2] in checksums:
            raise ValueError('Invalid or duplicate SHA256SUMS entry')
        checksums[match[2]] = match[1]
    outputs = ['release/paper.pdf', data['archive']]
    if set(checksums) != {PurePosixPath(name).name for name in outputs}:
        raise ValueError('SHA256SUMS must identify exactly the PDF and current source archive')
    for name in outputs:
        if digest_file(safe_path(root, name, required=True)) != checksums[PurePosixPath(name).name]:
            raise ValueError(f'Release checksum mismatch: {name}')

    prefix = data['prefix'] + '/'
    expected = {prefix + name for name in data['source_files']}
    with zipfile.ZipFile(safe_path(root, data['archive'], required=True)) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(set(names)) or set(names) != expected:
            raise ValueError('Archive membership does not match the explicit source inventory')
        for entry in entries:
            relative_name(entry.filename)
            file_type = stat.S_IFMT(entry.external_attr >> 16)
            if entry.is_dir() or file_type not in (0, stat.S_IFREG) or entry.flag_bits & 1:
                raise ValueError(f'Non-regular or encrypted archive entry: {entry.filename}')
            digest = hashlib.sha256()
            with archive.open(entry) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            if digest.hexdigest() != manifest[entry.filename[len(prefix):]]:
                raise ValueError(f'Archive source byte mismatch: {entry.filename}')


def write_atomic(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def package(root=ROOT):
    data = load_inventory(root)
    # An extracted source archive has no Git metadata or repository-only tooling.
    # Its exact source list still controls every byte included in the rebuilt ZIP.
    check_repository_scope(data, root, require_git=False)
    pdf = safe_path(root, 'release/paper.pdf', required=True)
    sources = {name: safe_path(root, name, required=True).read_bytes()
               for name in sorted(data['source_files'])}
    archive_path = safe_path(root, data['archive'])
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=archive_path.parent, delete=False) as stream:
            temporary = Path(stream.name)
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in sources.items():
                entry = zipfile.ZipInfo(data['prefix'] + '/' + name, date_time=(2026, 10, 9, 12, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(entry, content)
        temporary.replace(archive_path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    manifest = {name: hashlib.sha256(content).hexdigest() for name, content in sources.items()}
    write_atomic(safe_path(root, 'release/source-manifest.json'),
                 (json.dumps(manifest, indent=2) + '\n').encode('utf-8'))
    checksums = ''.join(f'{digest_file(path)}  {path.name}\n' for path in [pdf, archive_path])
    write_atomic(safe_path(root, 'release/SHA256SUMS'), checksums.encode('utf-8'))
    verify_release(data, root)
    print(f'Packaged {len(sources)} declared source files; archive and checksums verified')


if __name__ == '__main__':
    try:
        package()
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        raise SystemExit(str(error)) from error
