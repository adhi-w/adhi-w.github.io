/* Optional DOM integration tests: node scripts/check_interactions.cjs [path-to-jsdom] */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require(process.argv[2] || 'jsdom');
const root = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(root, 'assets/js/site.js'), 'utf8');
const projects = JSON.parse(fs.readFileSync(path.join(root, 'assets/content/projects.json'), 'utf8'));
const errors = [];

function open(file, reducedMotion = false) {
  const console = new VirtualConsole();
  console.on('jsdomError', error => errors.push(error.message));
  const dom = new JSDOM(fs.readFileSync(path.join(root, file), 'utf8'), {
    url: `https://adhi-w.github.io/${file}`, runScripts: 'outside-only', virtualConsole: console,
  });
  dom.window.setInterval = dom.window.setTimeout = () => { throw new Error('Unexpected timed behavior'); };
  dom.window.matchMedia = () => ({ matches: reducedMotion, addEventListener() {} });
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
const motion = home.window.document.querySelector('[data-motion-toggle]');
assert.equal(motion.getAttribute('aria-pressed'), 'true');
motion.click();
assert.equal(motion.getAttribute('aria-pressed'), 'false');
assert(!home.window.document.documentElement.classList.contains('motion-enabled'));
assert.equal(home.window.localStorage.getItem('background-motion'), 'paused');
motion.click();
assert.equal(motion.getAttribute('aria-pressed'), 'true');
home.window.close();
const reduced = open('index.html', true);
assert(!reduced.window.document.documentElement.classList.contains('motion-enabled'));
assert.equal(reduced.window.document.querySelector('[data-motion-toggle]').disabled, true);
reduced.window.close();

const archive = open('projects.html');
const doc = archive.window.document;
const cards = [...doc.querySelectorAll('[data-project]')];
const count = () => cards.filter(card => !card.hidden).length;
assert.equal(count(), projects.length);
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
assert.equal(count(), projects.length);
assert.equal(doc.querySelector('#no-results').hidden, true);
assert.equal(doc.querySelector('#project-count').textContent, `${projects.length} projects`);
doc.querySelector('[data-filter="VR & XR"]').click();
search.value = 'latency';
search.dispatchEvent(new archive.window.Event('input'));
assert(cards.find(card => card.textContent.includes('Latency-driven foveation')).hidden === false);
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
const degrees = [...cv.window.document.querySelectorAll('#education .timeline-item')];
assert.equal(degrees.length, 3);
assert(degrees[0].textContent.includes('May 2024'));
assert(degrees[0].textContent.includes('In progress'));
assert(!cv.window.document.querySelector('#education').textContent.includes('University of Oulu'));
for (const degree of degrees.slice(1)) {
  assert.equal(degree.querySelector('.date'), null);
  assert(!/\b(?:19|20)\d{2}\b|GPA/.test(degree.textContent));
}
assert(cv.window.document.querySelector('#experience .timeline-item').textContent.includes('November 2023'));
let printed = false;
cv.window.print = () => { printed = true; };
cv.window.document.querySelector('[data-print]').click();
assert.equal(printed, true);
cv.window.close();
for (const kind of ['xr', 'research']) {
  const resume = open(`resume-${kind}.html`);
  assert([...resume.window.document.querySelectorAll('.resume-sheet h3')].some(heading => heading.textContent.trim() === 'Researcher · Immersive Telepresence'));
  assert(resume.window.document.querySelector(`a[download]`).href.endsWith(`resume-${kind}.pdf`));
  let resumePrinted = false;
  resume.window.print = () => { resumePrinted = true; };
  resume.window.document.querySelector('[data-print]').click();
  assert(resumePrinted);
  resume.window.close();
}
const contact = open('contact.html');
assert(contact.window.document.querySelector('.contact-aside a[href="https://www.linkedin.com/in/adhi-w/"]'));
const emailLink = contact.window.document.querySelector('[data-email-link]');
assert(!emailLink.href.startsWith('mailto:'));
assert.equal(emailLink.hidden, false);
emailLink.addEventListener('click', event => event.preventDefault());
emailLink.click();
const expectedAddress = ['adhi', 'cwidagdo'].join('.') + '@' + ['gmail', 'com'].join('.');
assert.equal(emailLink.href, 'mailto:' + expectedAddress);
contact.window.close();
assert.deepEqual(errors, []);
console.log(`PASS: menu, Escape/focus, filters/search, CV and resume print actions, LinkedIn, click-to-email, motion toggle, and reduced motion.`);
console.log(`PASS: ${projects.length} galleries and ${checkedImages} images; thumbnails, arrows, boundaries, keyboard, and touch.`);
console.log('No automatic slide timers or JavaScript errors. Visual browser QA remains a separate check.');
