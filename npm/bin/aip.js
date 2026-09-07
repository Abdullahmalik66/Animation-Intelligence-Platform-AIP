#!/usr/bin/env node
/**
 * npx aip-cli check .
 *
 * AIP is written in Python (stdlib only, no dependencies). This shim finds a
 * Python 3.10+, installs AIP once into a private venv under the user's cache
 * directory, and delegates.
 *
 * It never writes into the user's project. The only thing it creates is
 * ~/.cache/aip/venv, and only on first run.
 */
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const VERSION = require('../package.json').version;
const IS_WINDOWS = process.platform === 'win32';

function cacheDir() {
  if (process.env.AIP_HOME) return process.env.AIP_HOME;
  const base =
    process.env.XDG_CACHE_HOME ||
    (process.platform === 'darwin'
      ? path.join(os.homedir(), 'Library', 'Caches')
      : path.join(os.homedir(), '.cache'));
  return path.join(base, 'aip');
}

const VENV = path.join(cacheDir(), 'venv');
const VENV_PYTHON = IS_WINDOWS
  ? path.join(VENV, 'Scripts', 'python.exe')
  : path.join(VENV, 'bin', 'python');

/** Return the first python on PATH that is >= 3.10, or null. */
function findPython() {
  const candidates = IS_WINDOWS
    ? ['python', 'python3', 'py']
    : ['python3', 'python', 'python3.13', 'python3.12', 'python3.11', 'python3.10'];

  for (const exe of candidates) {
    const probe = spawnSync(
      exe,
      ['-c', 'import sys; print("%d.%d" % sys.version_info[:2])'],
      { encoding: 'utf8' }
    );
    if (probe.status !== 0 || !probe.stdout) continue;
    const [major, minor] = probe.stdout.trim().split('.').map(Number);
    if (major === 3 && minor >= 10) return exe;
  }
  return null;
}

function fail(message) {
  process.stderr.write(`aip: ${message}\n`);
  process.exit(127);
}

function ensureInstalled() {
  if (fs.existsSync(VENV_PYTHON)) return VENV_PYTHON;

  const python = findPython();
  if (!python) {
    fail(
      'AIP needs Python 3.10 or newer, and none was found on your PATH.\n' +
        '  macOS:   brew install python\n' +
        '  Ubuntu:  sudo apt install python3\n' +
        '  Windows: https://python.org/downloads\n' +
        '\n' +
        'Already have Python somewhere else? Run: pipx install aip'
    );
  }

  process.stderr.write('aip: first run — installing (once, ~5s)\n');

  const venv = spawnSync(python, ['-m', 'venv', VENV], { stdio: 'inherit' });
  if (venv.status !== 0) {
    fail(`could not create a virtualenv at ${VENV}. Try: pipx install aip`);
  }

  const install = spawnSync(
    VENV_PYTHON,
    ['-m', 'pip', 'install', '--quiet', '--disable-pip-version-check', `aip==${VERSION}`],
    { stdio: 'inherit' }
  );
  if (install.status !== 0) {
    // Leave no broken venv behind for the next run to trip over.
    fs.rmSync(VENV, { recursive: true, force: true });
    fail('installation failed. Are you online? Try: pipx install aip');
  }

  return VENV_PYTHON;
}

const python = ensureInstalled();
const run = spawnSync(python, ['-m', 'aip', ...process.argv.slice(2)], {
  stdio: 'inherit',
});
process.exit(run.status === null ? 1 : run.status);
