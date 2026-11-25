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

document.querySelector('#year')?.replaceChildren(String(new Date().getFullYear()));

const mediaList = document.querySelector('#media-list');
if (mediaList) {
  fetch('media.json')
    .then(response => {
      if (!response.ok) throw new Error('无法读取节目列表');
      return response.json();
    })
    .then(data => {
      const items = Array.isArray(data.items) ? data.items : [];
      mediaList.replaceChildren();
      for (const item of items) {
        let url;
        try { url = new URL(item.url); } catch { continue; }
        if (url.protocol !== 'https:') continue;
        const card = document.createElement('a');
        card.className = `media-card ${item.kind === 'video' ? 'video' : 'audio'}`;
        card.href = url.href;
        card.target = '_blank';
        card.rel = 'noopener noreferrer';

        const meta = document.createElement('div');
        meta.className = 'media-kind';
        const label = document.createElement('span');
        label.textContent = `${item.kind === 'video' ? 'VIDEO' : 'AUDIO'} / ${item.language || ''}`;
        const icon = document.createElement('strong');
        icon.setAttribute('aria-hidden', 'true');
        icon.textContent = item.kind === 'video' ? '▷' : '♫';
        meta.append(label, icon);
        const title = document.createElement('h3');
        title.textContent = item.title || '';
        const originalTitle = document.createElement('p');
        originalTitle.className = 'original-title';
        originalTitle.textContent = item.originalTitle || '';
        const description = document.createElement('p');
        description.textContent = item.description || '';
        const footer = document.createElement('div');
        footer.className = 'media-card-footer';
        const source = document.createElement('span');
        source.textContent = item.source || '';
        const action = document.createElement('b');
        action.textContent = item.kind === 'video' ? '去观看 ↗' : '去收听 ↗';
        footer.append(source, action);
        card.append(meta, title, originalTitle, description, footer);
        mediaList.append(card);
      }
      if (!mediaList.children.length) throw new Error('节目列表为空');
    })
    .catch(() => {
      mediaList.replaceChildren();
      const fallback = document.createElement('p');
      fallback.className = 'media-loading';
      fallback.textContent = '节目列表暂时无法载入。请稍后刷新，或先到「扎根本性」公众号浏览。';
      mediaList.append(fallback);
    });
}

if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => {
    element.classList.add('will-reveal');
    observer.observe(element);
  });
}
