const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.site-nav');

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? '打开导航' : '关闭导航');
  nav.classList.toggle('is-open', !isOpen);
});

nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', '打开导航');
  nav.classList.remove('is-open');
}));

const dialog = document.querySelector('#poster-dialog');
const posterImage = document.querySelector('#poster-image');
const posterTitle = document.querySelector('#poster-title');
const posterOriginal = document.querySelector('#poster-original');
let lastTrigger = null;

document.querySelectorAll('.poster-open').forEach(button => {
  button.addEventListener('click', () => {
    lastTrigger = button;
    posterImage.src = button.dataset.poster;
    posterImage.alt = button.dataset.title + '课程海报';
    posterTitle.textContent = button.dataset.title;
    posterOriginal.href = button.dataset.poster;
    dialog.showModal();
  });
});

document.querySelector('#poster-close')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', event => {
  if (event.target === dialog) dialog.close();
});
dialog?.addEventListener('close', () => {
  posterImage.removeAttribute('src');
  lastTrigger?.focus();
});

document.querySelector('#year').textContent = new Date().getFullYear();
