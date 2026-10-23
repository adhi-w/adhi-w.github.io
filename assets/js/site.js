(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.textContent = open ? 'Close' : 'Menu';
    nav.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      menu.click(); menu.focus();
    }
  });
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  document.querySelectorAll('[data-enhanced]').forEach(element => element.hidden = false);
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-project]')];
  const search = document.querySelector('#project-search');
  if (cards.length && search) {
    let category = 'all';
    const update = () => {
      let count = 0;
      const query = search.value.trim().toLocaleLowerCase();
      cards.forEach(card => {
        const visible = (category === 'all' || card.dataset.category === category) && card.dataset.search.includes(query);
        card.hidden = !visible; if (visible) count++;
      });
      document.querySelector('#project-count').textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
      document.querySelector('#no-results').hidden = count > 0;
    };
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.filter;
      filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      update();
    }));
    search.addEventListener('input', update);
  }
  const gallery = document.querySelector('[data-gallery]');
  if (!gallery) return;
  const items = JSON.parse(document.querySelector('#gallery-data').textContent);
  const stage = gallery.querySelector('.gallery-stage');
  const photo = stage.querySelector('img');
  const original = gallery.querySelector('.original-link');
  const thumbs = [...gallery.querySelectorAll('[data-slide]')];
  const previous = gallery.querySelector('[data-previous]');
  const next = gallery.querySelector('[data-next]');
  let current = 0;
  const show = index => {
    current = Math.max(0, Math.min(items.length - 1, index));
    const item = items[current];
    photo.srcset = item.srcset;
    photo.src = item.src;
    photo.alt = item.caption;
    photo.width = item.width; photo.height = item.height;
    stage.querySelector('a').href = item.original;
    original.href = item.original;
    gallery.querySelector('.gallery-count').textContent = `${current + 1} / ${items.length}`;
    gallery.querySelector('.gallery-caption').textContent = item.caption;
    thumbs.forEach((thumb, index) => thumb.setAttribute('aria-current', String(index === current)));
    previous.disabled = current === 0; next.disabled = current === items.length - 1;
  };
  thumbs.forEach((thumb, index) => thumb.addEventListener('click', event => { event.preventDefault(); show(index); }));
  previous.addEventListener('click', () => show(current - 1));
  next.addEventListener('click', () => show(current + 1));
  gallery.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  let touchStart;
  stage.addEventListener('touchstart', event => {
    touchStart = { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY };
  }, { passive: true });
  stage.addEventListener('touchend', event => {
    if (!touchStart) return;
    const dx = event.changedTouches[0].clientX - touchStart.x;
    const dy = event.changedTouches[0].clientY - touchStart.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(current + (dx < 0 ? 1 : -1));
    touchStart = undefined;
  }, { passive: true });
  show(0);
})();
