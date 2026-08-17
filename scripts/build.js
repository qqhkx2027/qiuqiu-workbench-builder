// workbench-builder · build.js
// Generate N style variants from ONE source.html template, then smoke-test every renderer.
//
// Usage:
//   node build.js [source.html] [dist/]
// Defaults (relative to this script):
//   source = ../assets/qiqiu-workbench-source.html   (or ./source.html / ../source.html)
//   dist   = ../dist
//
// source.html must contain the tokens: {{THEME}}  {{PREFIX}}  {{TITLE}}
// Each produced file isolates its data via a unique localStorage prefix.
// A Node `vm` smoke test runs EVERY render* function on EVERY variant — this is
// the only thing that catches the "THEME token not replaced → icons fall back to
// emoji" bug, because a minimal-only smoke test passes silently.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const here = __dirname;
const srcArg = process.argv[2] || null;
const distArg = process.argv[3] || null;

function findSrc() {
  if (srcArg && fs.existsSync(srcArg)) return srcArg;
  const candidates = [
    path.join(here, '..', 'assets', 'qiqiu-workbench-source.html'),
    path.join(process.cwd(), 'source.html'),
    path.join(here, '..', 'source.html'),
    path.join(here, 'source.html'),
  ];
  return candidates.find(c => c && fs.existsSync(c)) || null;
}
const SRC = findSrc();
if (!SRC) { console.error('Cannot find source.html. Pass it as the first arg.'); process.exit(1); }
const DIST = distArg || path.join(here, '..', 'dist');
fs.mkdirSync(DIST, { recursive: true });

// ---- Variant definitions: add/remove styles here. New theme checklist:
//   1) add an entry below  2) add a `data-theme="<theme>"` CSS block in source.html
//   3) add an entry to ICON_IMGS['<theme>'] in assets/icons/icons.js  ----
const VARIANTS = [
  { theme: 'minimal',     prefix: 'wb_minimal_',     title: '秋秋工作台' },
  { theme: 'pink',        prefix: 'wb_pink_',        title: '秋秋工作台' },
  { theme: 'dark',        prefix: 'wb_dark_',        title: '秋秋工作台' },
  { theme: 'cinnamoroll', prefix: 'wb_cinnamoroll_', title: '秋秋工作台' },
  { theme: 'popmart',     prefix: 'wb_popmart_',     title: '秋秋工作台' },
  { theme: 'kuromi',      prefix: 'wb_kuromi_',      title: '秋秋工作台' },
];

// Sub-tabs to click through per module, so the smoke test exercises every branch.
// Keys must match state.tabs.<module>; values are the tab keys.
const SUBTABS = {
  health: ['record', 'fortune', 'answer', 'happy'],
  media:  ['mustread', 'mine', 'english', 'drum', 'food'],
  ledger: ['record', 'invest'],
};

function build(v) {
  const html = fs.readFileSync(SRC, 'utf8')
    .replace(/\{\{THEME\}\}/g, v.theme)
    .replace(/\{\{PREFIX\}\}/g, v.prefix)
    .replace(/\{\{TITLE\}\}/g, v.title);
  if (/\{\{(?:THEME|PREFIX|TITLE)\}\}|\{(?:THEME|PREFIX|TITLE)\}/.test(html)) {
    throw new Error('Unresolved template token in ' + SRC);
  }
  return html;
}

// ---- Build files ----
VARIANTS.forEach(v => {
  fs.writeFileSync(path.join(DIST, v.theme + '.html'), build(v));
});
fs.writeFileSync(path.join(DIST, 'index.html'), build(VARIANTS[0]));
console.log('Built variants:', VARIANTS.map(v => v.theme).join(', '), '→', DIST);

// ---- Smoke test (DOM-stubbed vm) on EVERY variant ----
function smoke(html, label) {
  const script = html.split('<script>')[1].split('</script>')[0];
  const store = {};
  const localStorage = {
    getItem: k => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; },
  };
  function makeEl() {
    const el = {
      _html: '', _text: '', style: {},
      classList: { add(){}, remove(){}, toggle(){}, contains(){return false;} },
      set innerHTML(v){ this._html = v; }, get innerHTML(){ return this._html; },
      set textContent(v){ this._text = v; }, get textContent(){ return this._text; },
      set value(v){ this._val = v; }, get value(){ return this._val || ''; },
      set onclick(f){ this._onclick = f; }, get onclick(){ return this._onclick; },
      appendChild(){}, querySelectorAll(){ return []; }, focus(){}, click(){},
    };
    return el;
  }
  const elements = {};
  const document = {
    getElementById: id => (elements[id] = elements[id] || makeEl()),
    querySelectorAll: () => [],
    createElement: () => makeEl(),
    addEventListener(){},
  };
  const sandbox = {
    localStorage, document,
    scrollTo(){}, open(){}, setInterval: () => 0, setTimeout: () => 0,
    console, Date, Math, JSON,
    Blob: function(){}, URL: { createObjectURL: () => '' },
    confirm: () => true, FileReader: function(){},
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);

  try {
    // Assert THEME token was actually replaced — catches the fallback-to-emoji bug.
    if (!new RegExp("const THEME='" + label + "'").test(script)) {
      throw new Error("THEME token NOT replaced (icon fallback to emoji bug)");
    }
    vm.runInContext(script, sandbox);
    // auto-discover every global render* function
    const renderFns = Object.getOwnPropertyNames(sandbox)
      .filter(n => n.startsWith('render') && typeof sandbox[n] === 'function');
    if (!renderFns.length) throw new Error('No render* functions found');
    const crudFns = ['addTodo','editTodo','addGoal','editGoal','addTrip','editTrip','addSchedule','editSchedule','addAINews','editAINews','addFinNews','editFinNews','addLedger','editLedger','addMedia','editMedia','addDrum','editDrum','addFood','editFood','addDiaryItem','removeItem'];
    crudFns.forEach(name => {
      if (typeof sandbox[name] !== 'function') throw new Error('Missing CRUD function: ' + name);
    });
    renderFns.forEach(name => {
      sandbox[name]();
      console.log('OK  ' + name + '  (content length: ' + (elements['content'] ? elements['content']._html.length : 0) + ')');
    });
    Object.keys(SUBTABS).forEach(mod => {
      (SUBTABS[mod] || []).forEach(t => {
        vm.runInContext("state.tabs." + mod + "='" + t + "';render" + mod.charAt(0).toUpperCase() + mod.slice(1) + "();", sandbox);
        console.log('OK  render' + mod + '/' + t + '  (len ' + elements['content']._html.length + ')');
      });
    });
    console.log(label.toUpperCase() + ' SMOKE TEST PASSED');
  } catch (e) {
    console.error(label.toUpperCase() + ' SMOKE TEST FAILED:', e.message);
    console.error(e.stack);
    process.exit(1);
  }
}

VARIANTS.forEach(v => smoke(build(v), v.theme));
console.log('ALL VARIANTS PASSED');
