const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.site-nav');
const copy = ({
  'zh-CN': {open:'打开导航',close:'关闭导航',poster:'课程海报',records:n=>`显示 ${n} 条教学记录`,watch:'去观看 ↗',listen:'去收听 ↗',empty:'节目列表为空',fetch:'无法读取节目列表',fallback:'节目列表暂时无法载入。请稍后刷新，或先到「扎根本性」公众号浏览。'},
  en: {open:'Open menu',close:'Close menu',poster:'course poster',records:n=>`${n} teaching records shown`,watch:'Watch ↗',listen:'Listen ↗',empty:'The media list is empty',fetch:'Unable to load the media list',fallback:'The media list is temporarily unavailable. Please refresh later.'},
  fr: {open:'Ouvrir le menu',close:'Fermer le menu',poster:'affiche de la formation',records:n=>`${n} étapes affichées`,watch:'Regarder ↗',listen:'Écouter ↗',empty:'La liste des médias est vide',fetch:'Impossible de charger la liste des médias',fallback:'La liste des médias est temporairement indisponible. Réessayez plus tard.'}
})[document.documentElement.lang] || ({open:'Open menu',close:'Close menu',poster:'course poster',records:n=>`${n} records shown`,watch:'Watch ↗',listen:'Listen ↗',empty:'The media list is empty',fetch:'Unable to load the media list',fallback:'The media list is temporarily unavailable.'});

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? copy.open : copy.close);
  nav.classList.toggle('is-open', !isOpen);
});

nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', copy.open);
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
    posterImage.alt = button.dataset.title + ' ' + copy.poster;
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

const journeyFilters = [...document.querySelectorAll('[data-journey-filter]')];
if (journeyFilters.length) {
  const cards = [...document.querySelectorAll('.journey-card[data-track]')];
  const years = [...document.querySelectorAll('.journey-year')];
  const status = document.querySelector('#journey-filter-status');
  const applyJourneyFilter = filter => {
    let shown = 0;
    cards.forEach(card => {
      card.hidden = filter !== 'all' && !card.dataset.track.split(' ').includes(filter);
      if (!card.hidden) shown += 1;
    });
    years.forEach(year => { year.hidden = !year.querySelector('.journey-card:not([hidden])'); });
    journeyFilters.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.journeyFilter === filter));
    });
    if (status) status.textContent = copy.records(shown);
  };
  journeyFilters.forEach(button => {
    button.addEventListener('click', () => applyJourneyFilter(button.dataset.journeyFilter));
  });
  const showHashTarget = () => {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target || !target.closest('.journey-main')) return;
    if (target.hidden || target.closest('.journey-year[hidden]')) applyJourneyFilter('all');
    if (target.classList.contains('journey-card')) {
      const details = target.querySelector('details');
      if (details) details.open = true;
    }
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  };
  applyJourneyFilter('all');
  if (location.hash) showHashTarget();
  window.addEventListener('hashchange', showHashTarget);
}

const mediaList = document.querySelector('#media-list');
if (mediaList) {
  fetch('media.json')
    .then(response => {
      if (!response.ok) throw new Error(copy.fetch);
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
        action.textContent = item.kind === 'video' ? copy.watch : copy.listen;
        footer.append(source, action);
        card.append(meta, title, originalTitle, description, footer);
        mediaList.append(card);
      }
      if (!mediaList.children.length) throw new Error(copy.empty);
    })
    .catch(() => {
      mediaList.replaceChildren();
      const fallback = document.createElement('p');
      fallback.className = 'media-loading';
      fallback.textContent = copy.fallback;
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
