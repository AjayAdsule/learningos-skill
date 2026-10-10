// Run with: node --test tests/test_flow.cjs
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function loadModel() {
  const htmlPath = path.join(__dirname, '..', 'docs', 'index.html');
  assert.ok(fs.existsSync(htmlPath), 'Interactive guide must exist');
  const html = fs.readFileSync(htmlPath, 'utf8');
  const script = html.match(/<script id="workflow-script">([\s\S]*?)<\/script>/);
  assert.ok(script, 'Guide must contain a testable workflow script');
  const context = { module: { exports: {} } };
  vm.runInNewContext(script[1], context);
  return context.module.exports;
}

test('default journey preserves notes and ends at learning review', () => {
  const model = loadModel();
  const ids = Array.from(model.buildJourney({}), step => step.id);
  assert.deepEqual(ids, ['capture', 'clarify', 'verify', 'connect', 'organize', 'save', 'review']);
});

test('requested map and draft are optional branches after private saving', () => {
  const model = loadModel();
  const ids = Array.from(model.buildJourney({ map: true, write: true }), step => step.id);
  assert.deepEqual(ids, ['capture', 'clarify', 'verify', 'connect', 'organize', 'save', 'map', 'draft', 'review']);
});

test('publication requires both a drafting request and final approval', () => {
  const model = loadModel();
  for (const options of [{ publish: true }, { write: true }, {}]) {
    assert.equal(model.buildJourney(options).some(step => step.id === 'publish'), false);
  }
  const approved = Array.from(model.buildJourney({ write: true, publish: true }), step => step.id);
  assert.deepEqual(approved.slice(-3), ['draft', 'publish', 'review']);
});
