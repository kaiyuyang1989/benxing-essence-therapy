(() => {
  'use strict';

  const source = window.LEARNING_SOURCE;
  const byId = (id) => document.getElementById(id);
  const noteBody = byId('noteBody');
  const chapterNav = byId('chapterNav');
  const audio = byId('audioPlayer');
  const globalSeek = byId('globalSeek');
  const globalTime = byId('globalTime');
  const searchInput = byId('searchInput');
  const searchSummary = byId('searchSummary');
  let activeTab = 'notes';
  let activeMatches = [];
  let currentMatch = -1;
  let tracks = [];
  let offsets = [];
  let totalDuration = 0;
  let currentTrackIndex = 0;
  let globalPosition = 0;
  let localAudioUrls = [];
  let loadToken = 0;
  let playlistLoadId = 0;
  let isScrubbing = false;

  if (!source || typeof source.noteMarkdown !== 'string') {
    noteBody.textContent = '笔记数据未能载入，请检查 content.js。';
    return;
  }

  for (const id of ['sourceLinkTop', 'sourceLinkAudio', 'sourceLinkTranscript', 'sourceLinkFooter']) {
    byId(id).href = source.sourceUrl;
  }

  function plainMarkdown(text) {
    return text.replace(/\\([\\`*_{}\[\]()#+\-.!])/g, '$1');
  }

  function searchable(element, value) {
    element.classList.add('searchable');
    element.dataset.raw = value;
    element.textContent = value;
    return element;
  }

  function formatTime(value) {
    const seconds = Math.max(0, Math.floor(Number(value) || 0));
    const h = Math.floor(seconds / 3600);
    const m = Math.floor(seconds % 3600 / 60);
    const s = seconds % 60;
    return h ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}` : `${m}:${String(s).padStart(2, '0')}`;
  }

  function seekAudio(seconds) {
    if (!tracks.length) {
      byId('audioHelp').textContent = '录音尚未导入，当前不能按时码跳听。可先在飞书收听原音。';
      byId('audioHeading').scrollIntoView({ block: 'start' });
      return;
    }
    seekGlobal(seconds, true);
  }

  function updatePlayButton() {
    const playing = !audio.paused && !audio.ended;
    byId('playButton').textContent = playing ? '暂停' : '播放';
    byId('playButton').setAttribute('aria-label', playing ? '暂停录音' : '播放录音');
  }

  function updateGlobalTime(seconds) {
    globalPosition = Math.max(0, Math.min(totalDuration, Number(seconds) || 0));
    if (!isScrubbing) globalSeek.value = String(globalPosition);
    globalTime.textContent = `${formatTime(globalPosition)} / ${formatTime(totalDuration)}`;
    globalSeek.setAttribute('aria-valuetext', formatTime(globalPosition));
  }

  function updatePartLabel() {
    const track = tracks[currentTrackIndex];
    byId('currentPart').textContent = track ? `第 ${currentTrackIndex + 1} / ${tracks.length} 段 · ${track.label}` : '';
    byId('playlistList').querySelectorAll('li').forEach((item, index) => {
      item.classList.toggle('is-current', index === currentTrackIndex);
      if (index === currentTrackIndex) item.setAttribute('aria-current', 'true');
      else item.removeAttribute('aria-current');
    });
  }

  function playCurrent() {
    audio.play().catch(() => {
      byId('audioHelp').textContent = '浏览器暂停了播放，请再次点击播放。';
      updatePlayButton();
    });
  }

  function switchTrack(index, localSeconds, resume) {
    const track = tracks[index];
    if (!track) return;
    const local = Math.max(0, Math.min(track.duration - 0.01, Number(localSeconds) || 0));
    const sameSource = currentTrackIndex === index && audio.getAttribute('src') === track.src && audio.readyState >= 1;
    currentTrackIndex = index;
    updateGlobalTime(offsets[index] + local);
    updatePartLabel();
    if (sameSource) {
      audio.currentTime = local;
      if (resume) playCurrent();
      return;
    }

    audio.pause();
    const token = ++loadToken;
    audio.onloadedmetadata = () => {
      if (token !== loadToken) return;
      audio.currentTime = local;
      audio.playbackRate = Number(byId('playbackRate').value);
      updateGlobalTime(offsets[index] + local);
      if (resume) playCurrent();
    };
    audio.onerror = () => {
      if (token !== loadToken) return;
      byId('audioHelp').textContent = `第 ${index + 1} 段无法播放，请核对文件是否完整且浏览器支持其格式。`;
      updatePlayButton();
    };
    audio.src = track.src;
    audio.load();
  }

  function seekGlobal(seconds, resume = false) {
    if (!tracks.length) return;
    const target = Math.max(0, Math.min(totalDuration - 0.01, Number(seconds) || 0));
    let index = tracks.length - 1;
    for (let i = 0; i < tracks.length; i += 1) {
      if (target < offsets[i] + tracks[i].duration) {
        index = i;
        break;
      }
    }
    switchTrack(index, target - offsets[index], resume);
  }

  function probeDuration(src) {
    return new Promise((resolve, reject) => {
      const probe = document.createElement('audio');
      let settled = false;
      const finish = (error, duration) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        probe.removeAttribute('src');
        probe.load();
        if (error) reject(error);
        else resolve(duration);
      };
      const timer = setTimeout(() => finish(new Error('读取音频长度超时')), 30000);
      probe.preload = 'metadata';
      probe.addEventListener('loadedmetadata', () => {
        const duration = probe.duration;
        finish(null, Number.isFinite(duration) && duration > 0 ? duration : null);
      }, { once: true });
      probe.addEventListener('error', () => finish(new Error('无法打开音频文件')), { once: true });
      probe.src = src;
      probe.load();
    });
  }

  async function initializePlaylist(parts, localPreview = false, newObjectUrls = []) {
    if (!parts.length) return;
    const requestId = ++playlistLoadId;
    byId('audioStatus').textContent = '读取音频长度…';
    try {
      const prepared = await Promise.all(parts.map(async (part) => {
        const measured = await probeDuration(part.src);
        const fallback = Number(part.durationSeconds);
        const duration = measured ?? (Number.isFinite(fallback) && fallback > 0 ? fallback : null);
        if (!duration) throw new Error(`“${part.label}”没有可用的时长`);
        return { ...part, duration };
      }));
      if (requestId !== playlistLoadId) {
        newObjectUrls.forEach((url) => URL.revokeObjectURL(url));
        return;
      }
      const previousUrls = localAudioUrls;
      audio.pause();
      tracks = prepared;
      offsets = [];
      totalDuration = 0;
      for (const track of tracks) {
        offsets.push(totalDuration);
        totalDuration += track.duration;
      }
      currentTrackIndex = 0;
      globalSeek.max = String(totalDuration);
      byId('playlistList').replaceChildren();
      for (const track of tracks) {
        const item = document.createElement('li');
        item.textContent = `${track.label} · ${formatTime(track.duration)}`;
        byId('playlistList').appendChild(item);
      }
      byId('playlistDetails').hidden = tracks.length < 2;
      byId('continuousPlayer').hidden = false;
      byId('audioStatus').textContent = localPreview ? '本机试听' : '可播放';
      byId('audioStatus').classList.add('is-ready');
      byId('audioHeroStatus').textContent = localPreview ? '录音本机试听' : '录音可播放';
      byId('audioHeroStatus').classList.replace('is-pending', 'is-ready');
      const expected = Number(source.expectedTotalSeconds);
      const measured = formatTime(totalDuration);
      if (Number.isFinite(expected) && expected > 0 && Math.abs(totalDuration - expected) > 2) {
        byId('audioHelp').textContent = `导入 ${tracks.length} 段，实测连续时长 ${measured}，与原妙记显示的 ${formatTime(expected)} 不同；请核对是否缺段或有多余内容。`;
      } else {
        byId('audioHelp').textContent = `导入 ${tracks.length} 段，连续时长 ${measured}。时长接近原妙记记录，内容仍需对照原音核验。`;
      }
      switchTrack(0, 0, false);
      localAudioUrls = newObjectUrls;
      previousUrls.forEach((url) => URL.revokeObjectURL(url));
    } catch (error) {
      newObjectUrls.forEach((url) => URL.revokeObjectURL(url));
      if (requestId !== playlistLoadId) return;
      byId('audioStatus').textContent = tracks.length ? '当前音频可用' : '导入失败';
      byId('audioHelp').textContent = `音频导入失败：${error.message}。可先在飞书收听原音。`;
    }
  }

  function safeMediaPath(path) {
    return typeof path === 'string' && /^(?:\.\/)?media\/[^?#]+$/.test(path) && !path.split('/').includes('..');
  }

  function configuredAudioParts() {
    if (Array.isArray(source.audioParts) && source.audioParts.length) {
      return source.audioParts.map((part, index) => {
        const src = typeof part === 'string' ? part : part?.src;
        if (!safeMediaPath(src)) throw new Error(`第 ${index + 1} 段音频路径无效`);
        return {
          src,
          label: typeof part?.label === 'string' && part.label.trim() ? part.label.trim() : src.split('/').pop(),
          durationSeconds: typeof part === 'object' ? part.durationSeconds : null
        };
      });
    }
    if (safeMediaPath(source.audioPath)) {
      return [{ src: source.audioPath, label: source.audioPath.split('/').pop() }];
    }
    return [];
  }

  function renderNotes() {
    const lines = source.noteMarkdown.replace(/\r\n?/g, '\n').split('\n');
    let paragraph = [];
    let headingIndex = 0;

    function flushParagraph() {
      if (!paragraph.length) return;
      const text = plainMarkdown(paragraph.join('\n'));
      const p = searchable(document.createElement('p'), text);
      if (/^https?:\/\//.test(text)) p.classList.add('source-url');
      noteBody.appendChild(p);
      paragraph = [];
    }

    for (const line of lines) {
      if (!line.trim()) {
        flushParagraph();
        continue;
      }
      const heading = /^(#{1,5})\s+(.+)$/.exec(line);
      if (heading) {
        flushParagraph();
        headingIndex += 1;
        const level = heading[1].length;
        const title = plainMarkdown(heading[2]);
        const element = searchable(document.createElement(`h${Math.min(level + 1, 6)}`), title);
        element.className += ` note-heading level-${level}`;
        element.id = `note-h-${headingIndex}`;
        noteBody.appendChild(element);
        if (level <= 2) renderChapter(element, level);
        continue;
      }
      if (/^!\[[^\]]*\]\([^)]+\)\s*$/.test(line.trim())) {
        flushParagraph();
        const placeholder = document.createElement('div');
        placeholder.className = 'image-placeholder';
        placeholder.setAttribute('role', 'note');
        const message = document.createElement('div');
        const title = document.createElement('strong');
        title.textContent = '图片待补';
        const detail = document.createElement('span');
        detail.textContent = '原笔记此处有图片；临时飞书地址已过期，公开版不保留地址。';
        message.append(title, detail);
        placeholder.appendChild(message);
        noteBody.appendChild(placeholder);
        continue;
      }
      paragraph.push(line);
    }
    flushParagraph();
  }

  function renderChapter(heading, level) {
    const item = document.createElement('div');
    item.className = `toc-item level-${level}`;
    const link = document.createElement('a');
    link.className = 'toc-link';
    link.href = `#${heading.id}`;
    link.textContent = heading.dataset.raw;
    link.addEventListener('click', (event) => {
      event.preventDefault();
      setTab('notes');
      heading.scrollIntoView({ block: 'start', behavior: 'smooth' });
      history.replaceState(null, '', `#${heading.id}`);
    });
    item.appendChild(link);

    const mappedTime = source.chapterTimes?.[heading.id] ?? source.chapterTimes?.[heading.dataset.raw];
    if (Number.isFinite(mappedTime)) {
      const button = document.createElement('button');
      button.className = 'seek-button';
      button.type = 'button';
      button.textContent = formatTime(mappedTime);
      button.title = `从 ${button.textContent} 播放录音`;
      button.addEventListener('click', () => seekAudio(mappedTime));
      item.appendChild(button);
    }
    chapterNav.appendChild(item);
  }

  function setTab(name) {
    activeTab = name;
    const notes = name === 'notes';
    byId('notesPanel').hidden = !notes;
    byId('transcriptPanel').hidden = notes;
    byId('notesTab').classList.toggle('is-active', notes);
    byId('transcriptTab').classList.toggle('is-active', !notes);
    byId('notesTab').setAttribute('aria-selected', String(notes));
    byId('transcriptTab').setAttribute('aria-selected', String(!notes));
    byId('chapterNav').closest('.toc-card').hidden = !notes;
    byId('reader').classList.toggle('is-transcript', !notes);
    searchInput.closest('.search-field').hidden = !notes;
    searchSummary.hidden = !notes;
    searchCurrentPanel();
  }

  function highlight(element, query) {
    const raw = element.dataset.raw || '';
    const lower = raw.toLocaleLowerCase();
    const needle = query.toLocaleLowerCase();
    const fragment = document.createDocumentFragment();
    let index = 0;
    let count = 0;
    while (true) {
      const hit = lower.indexOf(needle, index);
      if (hit < 0) break;
      fragment.appendChild(document.createTextNode(raw.slice(index, hit)));
      const mark = document.createElement('mark');
      mark.textContent = raw.slice(hit, hit + query.length);
      fragment.appendChild(mark);
      index = hit + query.length;
      count += 1;
    }
    fragment.appendChild(document.createTextNode(raw.slice(index)));
    element.replaceChildren(fragment);
    return count;
  }

  function searchCurrentPanel() {
    const query = searchInput.value.trim();
    const all = document.querySelectorAll('.searchable');
    all.forEach((element) => {
      element.textContent = element.dataset.raw || '';
      element.classList.remove('search-current');
    });
    activeMatches = [];
    currentMatch = -1;
    if (!query) {
      searchSummary.textContent = '';
      return;
    }
    const panel = byId(activeTab === 'notes' ? 'notesPanel' : 'transcriptPanel');
    let hits = 0;
    panel.querySelectorAll('.searchable').forEach((element) => {
      const raw = element.dataset.raw || '';
      if (!raw.toLocaleLowerCase().includes(query.toLocaleLowerCase())) return;
      hits += highlight(element, query);
      activeMatches.push(element);
    });
    searchSummary.textContent = hits ? `找到 ${hits} 处，分布在 ${activeMatches.length} 段。按回车跳到下一段。` : '没有找到匹配内容。';
  }

  function jumpToNextMatch() {
    if (!activeMatches.length) return;
    if (currentMatch >= 0) activeMatches[currentMatch].classList.remove('search-current');
    currentMatch = (currentMatch + 1) % activeMatches.length;
    const element = activeMatches[currentMatch];
    element.classList.add('search-current');
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function parseTime(value) {
    if (typeof value === 'number') return Number.isFinite(value) ? value : null;
    if (typeof value !== 'string') return null;
    const parts = value.trim().replace(',', '.').split(':');
    if (parts.length < 2 || parts.length > 3 || parts.some((part) => !/^\d+(?:\.\d+)?$/.test(part))) return null;
    let seconds = 0;
    for (const part of parts) seconds = seconds * 60 + Number(part);
    return seconds;
  }

  function normalizeSegments(items) {
    return items.map((item) => {
      if (typeof item === 'string') return { start: null, text: item.trim() };
      if (!item || typeof item !== 'object') return null;
      const start = parseTime(item.start ?? item.startTime ?? item.time);
      const text = String(item.text ?? item.content ?? '').trim();
      return { start, text };
    }).filter((item) => item && item.text);
  }

  function parseSubtitle(text) {
    const blocks = text.replace(/\r\n?/g, '\n').replace(/^WEBVTT[^\n]*\n/, '').split(/\n\s*\n/);
    const segments = [];
    for (const block of blocks) {
      const lines = block.split('\n').map((line) => line.trim()).filter(Boolean);
      const timing = lines.findIndex((line) => line.includes('-->'));
      if (timing < 0) continue;
      const start = parseTime(lines[timing].split('-->')[0]);
      const content = lines.slice(timing + 1).join('\n').trim();
      if (content) segments.push({ start, text: content });
    }
    return segments;
  }

  function parsePlainText(text) {
    const lines = text.replace(/\r\n?/g, '\n').split('\n');
    const timed = [];
    for (const line of lines) {
      const match = /^\s*\[?((?:\d{1,2}:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)\]?\s*[-–]?\s*(.+)$/.exec(line);
      if (match) timed.push({ start: parseTime(match[1]), text: match[2].trim() });
    }
    return timed.length ? timed : [{ start: null, text: text.trim() }];
  }

  function renderTranscript(items, localPreview = false) {
    const segments = normalizeSegments(items);
    if (!segments.length) return false;
    const list = byId('transcriptList');
    list.replaceChildren();
    for (const segment of segments) {
      const row = document.createElement('div');
      row.className = 'transcript-cue';
      if (segment.start !== null) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'transcript-time';
        button.textContent = formatTime(segment.start);
        button.title = `跳到录音 ${button.textContent}`;
        button.addEventListener('click', () => seekAudio(segment.start));
        row.appendChild(button);
      } else {
        const label = document.createElement('span');
        label.className = 'transcript-time is-untimed';
        label.textContent = '无时码';
        row.appendChild(label);
      }
      row.appendChild(searchable(document.createElement('p'), segment.text));
      row.lastChild.classList.add('transcript-text');
      list.appendChild(row);
    }
    byId('transcriptEmpty').hidden = true;
    list.hidden = false;
    byId('transcriptHeroStatus').textContent = localPreview ? '逐字稿本机预览' : '逐字稿已收录';
    byId('transcriptHeroStatus').classList.replace('is-pending', 'is-ready');
    searchCurrentPanel();
    return true;
  }

  async function importTranscript(file) {
    if (!file) return;
    try {
      const text = await file.text();
      const extension = file.name.split('.').pop().toLowerCase();
      let segments;
      if (extension === 'json') {
        const parsed = JSON.parse(text);
        segments = Array.isArray(parsed) ? parsed : parsed.segments;
        if (!Array.isArray(segments)) throw new Error('JSON 中没有片段列表');
      } else if (extension === 'srt' || extension === 'vtt') {
        segments = parseSubtitle(text);
      } else {
        segments = parsePlainText(text);
      }
      if (!renderTranscript(segments, true)) throw new Error('文件没有可显示的文字');
    } catch (error) {
      byId('transcriptEmpty').querySelector('p').textContent = `导入失败：${error.message}。请检查文件格式。`;
    }
  }

  async function copyNotes() {
    try {
      await navigator.clipboard.writeText(source.noteMarkdown);
      byId('copyNotes').textContent = '已复制';
    } catch {
      const field = document.createElement('textarea');
      field.value = source.noteMarkdown;
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      const copied = document.execCommand('copy');
      field.remove();
      byId('copyNotes').textContent = copied ? '已复制' : '请下载本页 Markdown';
    }
    window.setTimeout(() => { byId('copyNotes').textContent = '复制笔记'; }, 2200);
  }

  renderNotes();
  if (Array.isArray(source.transcript) && source.transcript.length) renderTranscript(source.transcript);
  try {
    const configured = configuredAudioParts();
    if (configured.length) initializePlaylist(configured);
  } catch (error) {
    byId('audioHelp').textContent = `音频配置有误：${error.message}。`;
  }

  audio.addEventListener('timeupdate', () => {
    if (tracks.length && !isScrubbing) updateGlobalTime(offsets[currentTrackIndex] + audio.currentTime);
  });
  audio.addEventListener('play', updatePlayButton);
  audio.addEventListener('pause', updatePlayButton);
  audio.addEventListener('ended', () => {
    if (currentTrackIndex + 1 < tracks.length) switchTrack(currentTrackIndex + 1, 0, true);
    else {
      updateGlobalTime(totalDuration);
      updatePlayButton();
    }
  });
  byId('playButton').addEventListener('click', () => {
    if (!tracks.length) return;
    if (audio.paused) {
      if (globalPosition >= totalDuration - 0.1) seekGlobal(0, true);
      else playCurrent();
    } else audio.pause();
  });
  globalSeek.addEventListener('input', () => {
    isScrubbing = true;
    const preview = Number(globalSeek.value);
    globalTime.textContent = `${formatTime(preview)} / ${formatTime(totalDuration)}`;
    globalSeek.setAttribute('aria-valuetext', formatTime(preview));
  });
  globalSeek.addEventListener('change', () => {
    const target = Number(globalSeek.value);
    const resume = !audio.paused;
    isScrubbing = false;
    seekGlobal(target, resume);
  });
  byId('playbackRate').addEventListener('change', (event) => {
    audio.playbackRate = Number(event.target.value);
  });

  byId('notesTab').addEventListener('click', () => setTab('notes'));
  byId('transcriptTab').addEventListener('click', () => setTab('transcript'));
  searchInput.addEventListener('input', searchCurrentPanel);
  searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      jumpToNextMatch();
    }
  });
  byId('copyNotes').addEventListener('click', copyNotes);
  byId('audioFile').addEventListener('change', (event) => {
    const files = Array.from(event.target.files || []);
    if (!files.length) return;
    const collator = new Intl.Collator('zh-CN', { numeric: true, sensitivity: 'base' });
    files.sort((a, b) => collator.compare(a.name, b.name));
    const newUrls = files.map((file) => URL.createObjectURL(file));
    const parts = files.map((file, index) => ({ src: newUrls[index], label: file.name }));
    initializePlaylist(parts, true, newUrls);
  });
  byId('transcriptFile').addEventListener('change', (event) => importTranscript(event.target.files?.[0]));
})();
