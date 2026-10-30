'use strict';

const nav = document.querySelector('#site-nav');
const toggle = document.querySelector('.nav-toggle');
const dialog = document.querySelector('#detail-dialog');
const { activities, gallery } = JSON.parse(document.querySelector('#site-data').textContent);
const params = new URLSearchParams(window.location.search);
let lastTrigger = null;

function closeMenu() {
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', '打开导航');
  nav.classList.remove('is-open');
}
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
  nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    toggle.focus();
  }
});
window.matchMedia('(min-width: 821px)').addEventListener('change', closeMenu);

function setupFilters(buttonSelector, cardSelector, counterSelector) {
  const buttons = [...document.querySelectorAll(buttonSelector)];
  const cards = [...document.querySelectorAll(cardSelector)];
  if (!buttons.length) return;
  const attribute = buttonSelector.includes('photo') ? 'photoFilter' : 'filter';
  const apply = value => {
    const selected = buttons.find(button => button.dataset[attribute] === value) || buttons[0];
    buttons.forEach(button => {
      const active = button === selected;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    let visible = 0;
    cards.forEach(card => {
      card.hidden = selected.dataset[attribute] !== 'all' && card.dataset.category !== selected.dataset[attribute];
      if (!card.hidden) visible++;
    });
    document.querySelector(counterSelector).textContent = `${visible} ${attribute === 'photoFilter' ? '张照片' : '项活动'}`;
    const url = new URL(window.location.href);
    if (selected.dataset[attribute] === 'all') url.searchParams.delete('category');
    else url.searchParams.set('category', selected.dataset[attribute]);
    history.replaceState(null, '', url);
  };
  buttons.forEach(button => button.addEventListener('click', () => apply(button.dataset[attribute])));
  apply(params.get('category') || 'all');
}
setupFilters('[data-filter]', '.activity-card', '#result-count');
setupFilters('[data-photo-filter]', '.gallery-card', '#photo-count');

function showDetail(item, trigger, photo = false) {
  lastTrigger = trigger;
  dialog.classList.toggle('photo-dialog', photo);
  const image = document.querySelector('#dialog-image');
  image.src = item.image;
  image.alt = photo ? item.description : item.imageAlt;
  document.querySelector('#dialog-title').textContent = item.title;
  document.querySelector('#dialog-category').textContent = item.categoryLabel + (item.period ? ` / ${item.period}` : '');
  document.querySelector('#dialog-summary').textContent = photo ? item.description : item.summary;
  const body = document.querySelector('#dialog-body');
  body.replaceChildren();
  if (!photo) {
    item.paragraphs.forEach(text => {
      const p = document.createElement('p');
      p.textContent = text;
      body.append(p);
    });
    const list = document.createElement('ul');
    item.highlights.forEach(text => {
      const li = document.createElement('li');
      li.textContent = text;
      list.append(li);
    });
    body.append(list);
  }
  document.querySelector('#dialog-source').textContent = photo ? '图片来源：社团 2026 年展示资料。' : '资料来源：社团 2026 年展示资料。本页为活动回顾，非当前报名通知。';
  dialog.showModal();
  document.body.classList.add('dialog-open');
  dialog.scrollTop = 0;
  document.querySelector('.dialog-close').focus({ preventScroll: true });
  const url = new URL(window.location.href);
  url.searchParams.set(photo ? 'photo' : 'activity', item.id);
  history.replaceState(null, '', url);
}
document.addEventListener('click', event => {
  const activityButton = event.target.closest('[data-activity]');
  const photoButton = event.target.closest('[data-photo]');
  if (activityButton) {
    const item = activities.find(item => item.id === activityButton.dataset.activity);
    if (item) showDetail(item, activityButton);
  } else if (photoButton) {
    const item = gallery.find(item => item.id === photoButton.dataset.photo);
    if (item) showDetail(item, photoButton, true);
  }
});
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const rect = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('dialog-open');
  lastTrigger?.focus({ preventScroll: true });
  const url = new URL(window.location.href);
  url.searchParams.delete('activity');
  url.searchParams.delete('photo');
  history.replaceState(null, '', url);
});
const requestedActivity = activities.find(item => item.id === params.get('activity'));
const requestedPhoto = gallery.find(item => item.id === params.get('photo'));
if (requestedActivity && document.querySelector('.activity-grid')) {
  const trigger = [...document.querySelectorAll('[data-activity]')].find(button => button.dataset.activity === requestedActivity.id);
  // A shared detail URL must always expose its return target, even with a conflicting category.
  if (trigger?.closest('.activity-card').hidden) document.querySelector('[data-filter="all"]').click();
  showDetail(requestedActivity, trigger);
} else if (requestedPhoto && document.querySelector('.gallery-grid')) {
  const trigger = [...document.querySelectorAll('[data-photo]')].find(button => button.dataset.photo === requestedPhoto.id);
  if (trigger?.closest('.gallery-card').hidden) document.querySelector('[data-photo-filter="all"]').click();
  showDetail(requestedPhoto, trigger, true);
}
