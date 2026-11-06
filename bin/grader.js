#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const { resolve } = require('node:path');
const python = process.env.GRADER_PYTHON || 'python3';
const cwd = resolve(__dirname, '..');
const env = { ...process.env, PYTHONPATH: [cwd, process.env.PYTHONPATH || ''].filter(Boolean).join(require('node:path').delimiter) };
const result = spawnSync(python, ['-m', 'grader', ...process.argv.slice(2)], { stdio: 'inherit', env });
if (result.error) { console.error(`Grader requires Python 3.11+: ${result.error.message}`); process.exit(127); }
process.exit(result.status === null ? 2 : result.status);
