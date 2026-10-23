/* Optional DOM integration tests: node scripts/check_interactions.cjs [path-to-jsdom] */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require(process.argv[2] || 'jsdom');
const root = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(root, 'assets/js/site.js'), 'utf8');
const projects = JSON.parse(fs.readFileSync(path.join(root, 'assets/content/projects.json'), 'utf8'));
const errors = [];

function open(file) {
  const console = new VirtualConsole();
  console.on('jsdomError', error => errors.push(error.message));
  const dom = new JSDOM(fs.readFileSync(path.join(root, file), 'utf8'), {
    url: `https://adhi-w.github.io/${file}`, runScripts: 'outside-only', virtualConsole: console,
  });
  dom.window.setInterval = dom.window.setTimeout = () => { throw new Error('Unexpected timed behavior'); };
  dom.window.eval(script);
  return dom;
}

const home = open('index.html');
const menu = home.window.document.querySelector('.menu-toggle');
const nav = home.window.document.querySelector('#site-nav');
menu.click();
assert.equal(menu.getAttribute('aria-expanded'), 'true');
assert(nav.classList.contains('is-open'));
home.window.document.dispatchEvent(new home.window.KeyboardEvent('keydown', { key: 'Escape' }));
assert.equal(menu.getAttribute('aria-expanded'), 'false');
assert(!nav.classList.contains('is-open'));
assert.equal(home.window.document.activeElement, menu);
home.window.close();

const archive = open('projects.html');
const doc = archive.window.document;
const cards = [...doc.querySelectorAll('[data-project]')];
const count = () => cards.filter(card => !card.hidden).length;
assert.equal(count(), 25);
doc.querySelector('[data-filter="Robotics"]').click();
assert.equal(count(), projects.filter(project => project.category === 'Robotics').length);
const search = doc.querySelector('#project-search');
search.value = 'nonexistent-project-xyz';
search.dispatchEvent(new archive.window.Event('input'));
assert.equal(count(), 0);
assert.equal(doc.querySelector('#no-results').hidden, false);
search.value = 'quaternions';
search.dispatchEvent(new archive.window.Event('input'));
assert.equal(count(), 2);
search.value = '';
search.dispatchEvent(new archive.window.Event('input'));
doc.querySelector('[data-filter="all"]').click();
assert.equal(count(), 25);
assert.equal(doc.querySelector('#no-results').hidden, true);
assert.equal(doc.querySelector('#project-count').textContent, '25 projects');
archive.window.close();

let checkedImages = 0;
for (const project of projects) {
  const dom = open(project.file);
  const { document, KeyboardEvent, Event } = dom.window;
  const gallery = document.querySelector('[data-gallery]');
  const previous = gallery.querySelector('[data-previous]');
  const next = gallery.querySelector('[data-next]');
  const thumbs = [...gallery.querySelectorAll('[data-slide]')];
  const current = () => Number(gallery.querySelector('.gallery-count').textContent.split('/')[0]);
  assert.equal(previous.disabled, true);
  assert.equal(current(), 1);
  assert.equal(thumbs.length, project.images.length);
  next.click();
  assert.equal(current(), 2);
  previous.click();
  assert.equal(current(), 1);
  gallery.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
  assert.equal(current(), 2);
  gallery.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowLeft', bubbles: true }));
  assert.equal(current(), 1);
  for (let i = 0; i < thumbs.length; i++) {
    thumbs[i].click();
    assert.equal(current(), i + 1);
    assert.equal(gallery.querySelector('.original-link').getAttribute('href'), project.images[i]);
    assert.equal(gallery.querySelectorAll('[aria-current="true"]').length, 1);
    assert.equal(thumbs[i].getAttribute('aria-current'), 'true');
    checkedImages++;
  }
  assert.equal(next.disabled, true);
  gallery.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
  assert.equal(current(), thumbs.length);
  thumbs[0].click();
  const stage = gallery.querySelector('.gallery-stage');
  for (const [type,x] of [['touchstart',200],['touchend',90]]) {
    const event = new Event(type, { bubbles:true });
    Object.defineProperty(event,'changedTouches',{value:[{clientX:x,clientY:100}]});
    stage.dispatchEvent(event);
  }
  assert.equal(current(), 2);
  dom.window.close();
}

const cv = open('cv.html');
let printed = false;
cv.window.print = () => { printed = true; };
cv.window.document.querySelector('[data-print]').click();
assert.equal(printed, true);
cv.window.close();
assert.deepEqual(errors, []);
console.log(`PASS: menu, Escape/focus, project filters/search/empty state, and print action.`);
console.log(`PASS: ${projects.length} galleries and ${checkedImages} images; thumbnails, arrows, boundaries, keyboard, and touch.`);
console.log('No automatic slide timers or JavaScript errors. Visual browser QA remains a separate check.');
