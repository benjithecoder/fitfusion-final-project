#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const userKeybindingsPath = process.env.KEYBINDINGS_PATH ||
  path.join(os.homedir(), 'Library', 'Application Support', 'Code', 'User', 'keybindings.json');

function stripComments(text) {
  return text.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
}

function safeReadJsonc(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const raw = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(stripComments(raw));
  } catch (err) {
    console.error('Failed to parse keybindings.json, starting with empty array.');
    return [];
  }
}

function backup(filePath) {
  if (!fs.existsSync(filePath)) return;
  const bak = `${filePath}.bak.${Date.now()}`;
  fs.copyFileSync(filePath, bak);
  console.log('Backup created:', bak);
}

(function main() {
  console.log('Target keybindings:', userKeybindingsPath);
  const current = safeReadJsonc(userKeybindingsPath);
  backup(userKeybindingsPath);

  const desired = [
    { "key": "alt+right", "command": "editor.action.indentLines", "when": "editorTextFocus && !editorReadonly" },
    { "key": "alt+left",  "command": "editor.action.outdentLines",  "when": "editorTextFocus && !editorReadonly" },
    { "key": "cmd+right", "command": "acceptSelectedSuggestion",   "when": "suggestWidgetVisible && textInputFocus" }
  ];

  // Filter out conflicting entries for the keys we manage
  const filtered = current.filter(entry => {
    if (!entry || !entry.key) return true;
    const key = String(entry.key).toLowerCase();
    if (['cmd+right', 'alt+right', 'alt+left'].includes(key)) {
      // keep only entries that already match one of desired exactly
      return desired.some(d =>
        String(d.key).toLowerCase() === key &&
        entry.command === d.command &&
        String(entry.when || '') === String(d.when || '')
      );
    }
    return true;
  });

  // Add desired entries if missing
  desired.forEach(d => {
    const exists = filtered.some(e =>
      e && String(e.key).toLowerCase() === String(d.key).toLowerCase() &&
      e.command === d.command &&
      String(e.when || '') === String(d.when || '')
    );
    if (!exists) filtered.push(d);
  });

  const out = [
    "// Place your key bindings in this file to override the defaults",
    JSON.stringify(filtered, null, 4)
  ].join('\n');

  try {
    fs.writeFileSync(userKeybindingsPath, out, 'utf8');
    console.log('Keybindings updated successfully.');
    console.log('Restart VS Code or run "Developer: Reload Window" to apply changes.');
  } catch (err) {
    console.error('Failed to write keybindings file:', err);
  }
})();
