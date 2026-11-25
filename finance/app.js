(() => {
  'use strict';

  const STORAGE_KEY = 'xiaozha-ledger-review-v1';
  const WRAP_KEY = 'xiaozha-ledger-code-wrap-v1';
  const app = document.querySelector('#app');
  const storageAvailable = (() => {
    try { const key = 'xz-storage-check'; localStorage.setItem(key, '1'); localStorage.removeItem(key); return true; }
    catch { return false; }
  })();
  const hasLocalPassword = () => {
    try { return !!localStorage.getItem(WRAP_KEY); } catch { return false; }
  };
  const state = {
    dataset: null, datasetId: '', key: null, code: '', decisions: new Map(), cards: [],
    tab: 'review', queue: 'priority', search: '', selectedKey: null,
    editOpen: false, draft: { project: '', item: '', amount: '' },
    lastAction: null, pendingImport: null, message: '', busy: false,
    backupText: '', pasteOpen: false, passwordDialog: false,
    unlockMode: hasLocalPassword() ? 'local' : 'code',
  };
  const enc = new TextEncoder();
  const dec = new TextDecoder();
  const cents = (value) => Math.round(Number(value || 0) * 100);
  const money = (value) => new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value / 100);
  const amountText = (value) => (value / 100).toFixed(2);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const b64Bytes = (value) => Uint8Array.from(atob(value), (char) => char.charCodeAt(0));
  const bytesB64 = (value) => {
    const bytes = new Uint8Array(value);
    let binary = '';
    for (let i = 0; i < bytes.length; i += 8192) binary += String.fromCharCode(...bytes.subarray(i, i + 8192));
    return btoa(binary);
  };
  const shortDate = (value) => value ? value.slice(5).replace('-', '月') + '日' : '';
  const isAlipayEntry = (entry) => entry.source_refs.some((ref) => ref.includes('支付宝'));
  const isNeutralAlipay = (row) => row.direction === '不计收支' || row.disposition === '账户往来/不计' || row.disposition === '全额退款/零净额' || cents(row.net) === 0;
  const safeFileName = (value) => String(value || '').replace(/[^0-9-]/g, '_').replace(/_+/g, '_').slice(0, 60);

  async function deriveKey(code, salt, iterations) {
    const material = await crypto.subtle.importKey('raw', enc.encode(code), 'PBKDF2', false, ['deriveKey']);
    return crypto.subtle.deriveKey({ name: 'PBKDF2', salt, iterations, hash: 'SHA-256' }, material,
      { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
  }
  async function encryptJson(value, key) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(value)));
    return { iv: bytesB64(iv), ciphertext: bytesB64(ciphertext) };
  }
  async function decryptJson(envelope, key) {
    const bytes = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64Bytes(envelope.iv) }, key, b64Bytes(envelope.ciphertext));
    return JSON.parse(dec.decode(bytes));
  }
  async function hashHex(bytes) {
    const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
    return [...digest].map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }
  function validateDataset(data) {
    if (!data || typeof data.period !== 'string' || !Array.isArray(data.entries) || !Array.isArray(data.wechat_audit) || !Array.isArray(data.alipay_audit)) return false;
    if (data.entries.length !== 103 || data.wechat_audit.length !== 102 || data.alipay_audit.length !== 394) return false;
    const ids = new Set();
    for (const row of data.entries) {
      if (!row || typeof row.id !== 'string' || ids.has(row.id) || !['收入', '支出'].includes(row.flow) || typeof row.project !== 'string' || typeof row.item !== 'string' || !Number.isFinite(row.amount) || !Array.isArray(row.source_refs)) return false;
      ids.add(row.id);
    }
    return true;
  }
  function suggestedAlipayProject(row) {
    return row.suggested_project || '待分项目';
  }
  function buildCards(data) {
    const cards = data.entries.map((entry) => {
      const alipay = isAlipayEntry(entry);
      const uncertain = /待核|候选|待票据|待分|待修正/.test(entry.confidence + entry.project);
      const source = alipay ? '支付宝 · 已在账本' : entry.source_refs.some((ref) => ref.includes('微信')) ? '微信 · 已在账本' : '原账 · 已在账本';
      return {
        key: 'E:' + entry.id, kind: 'entry', date: entry.date, title: entry.item,
        value: cents(entry.amount), flow: entry.flow, source, project: entry.project,
        question: alipay ? '这笔支付宝流水要计入公司账吗？' : '这笔的项目和用途写对了吗？',
        reason: entry.note + (entry.source_refs.length ? '\n依据：' + entry.source_refs.join('；') : ''),
        effect: alipay ? '点“是”保留在账本；点“不是”从项目收支中移除。' : '点“是”确认现有归属；点“不是”转入待分项目，金额仍保留。',
        priority: uncertain ? 4 : 2, editable: true, entry,
        searchText: [entry.item, entry.project, entry.handler, entry.note, entry.date, ...entry.source_refs].join(' ').toLowerCase(),
      };
    });
    for (const row of data.alipay_audit) {
      if (row.ledger_ids.length) continue;
      const neutral = isNeutralAlipay(row);
      const candidate = row.disposition === '待核业务候选' || row.disposition === '收入待核';
      const title = row.counterparty + (row.description && row.description !== row.counterparty ? ' · ' + row.description : '');
      const project = suggestedAlipayProject(row);
      cards.push({
        key: 'A:' + row.transaction_id, kind: 'alipay', date: row.date, title,
        value: cents(row.net), flow: row.direction, source: '支付宝 · 原始流水', project,
        question: neutral ? '这笔不计入项目收支，处理正确吗？' : '这笔是公司的收入或支出吗？',
        reason: (row.rationale || row.disposition) + (row.refund ? '；原额 ' + money(cents(row.gross)) + '，退款 ' + money(cents(row.refund)) : ''),
        effect: neutral ? '点“是”确认暂不计入；点“不是”标记待修正。' : '点“是”按退款后净额加入账本；需要时先调整项目、名称和金额。',
        priority: candidate ? 5 : 1, editable: !neutral, alipay: row,
        searchText: [title, row.date, row.rationale, row.disposition, row.transaction_id].join(' ').toLowerCase(),
      });
    }
    const refundKeys = new Set();
    for (const row of data.wechat_audit) {
      if (row.ledger_ids.length) continue;
      if (row.disposition === '全额退款往返') {
        const pairedRow = row.related_rows[0] ?? row.source_row;
        const minRow = Math.min(row.source_row, pairedRow);
        const key = 'WR:' + minRow;
        if (refundKeys.has(key)) continue;
        refundKeys.add(key);
        const related = data.wechat_audit.find((item) => item.source_row === pairedRow);
        const paid = row.direction === '支出' ? row : related || row;
        cards.push({
          key, kind: 'wechat_refund', date: row.date, title: paid.counterparty + ' · 付款与退款',
          value: cents(row.amount), flow: '退款往返', source: '微信 · 两笔流水', project: '不计项目收支',
          question: '这两笔付款和退款可以相互抵消吗？',
          reason: '微信原件第 ' + row.source_row + '、' + pairedRow + ' 行；' + (row.note || '已全额退款') + '。净额 ¥0.00。',
          effect: '整组净额为零；点“不是”标记待修正，不会重复加进账本。',
          priority: 3, editable: false,
          searchText: [paid.counterparty, row.date, row.note, row.transaction_id].join(' ').toLowerCase(),
        });
      } else {
        cards.push({
          key: 'W:' + row.source_row, kind: 'wechat_fund', date: row.date,
          title: row.counterparty + (row.description ? ' · ' + row.description : ''),
          value: cents(row.amount), flow: row.direction, source: '微信 · 资金往来', project: '不计项目收支',
          question: '这笔暂按资金往来处理，正确吗？',
          reason: (row.note || row.description || '用途待核') + '；' + row.source_account + ' → ' + row.destination_account + '。微信原件第 ' + row.source_row + ' 行。',
          effect: '点“是”确认暂不计项目收支；点“不是”标记待修正。',
          priority: 5, editable: false,
          searchText: [row.counterparty, row.date, row.note, row.description, row.transaction_id].join(' ').toLowerCase(),
        });
      }
    }
    return cards.sort((a, b) => b.priority - a.priority || b.date.localeCompare(a.date) || a.key.localeCompare(b.key));
  }
  function deriveLedger() {
    const rows = [];
    for (const entry of state.dataset.entries) {
      const decision = state.decisions.get('E:' + entry.id);
      const alipay = isAlipayEntry(entry);
      if (alipay && decision?.answer === 'no') continue;
      rows.push({
        id: entry.id, project: decision?.answer === 'no' ? decision.project || '待分项目' : decision?.project || entry.project,
        flow: entry.flow, date: entry.date, item: decision?.item || entry.item,
        value: decision?.amount_cents ?? cents(entry.amount), handler: entry.handler,
        note: entry.note, status: decision ? decision.answer === 'yes' ? '已确认' : '归属待修正' : '待核',
        source: entry.source_refs.join('；'),
      });
    }
    for (const row of state.dataset.alipay_audit) {
      if (row.ledger_ids.length || isNeutralAlipay(row)) continue;
      const decision = state.decisions.get('A:' + row.transaction_id);
      if (decision?.answer !== 'yes') continue;
      rows.push({
        id: 'A:' + row.transaction_id, project: decision.project || suggestedAlipayProject(row),
        flow: row.direction === '收入' ? '收入' : '支出', date: row.date,
        item: decision.item || row.counterparty + (row.description ? ' · ' + row.description : ''),
        value: decision.amount_cents ?? cents(row.net), handler: '支付宝',
        note: row.rationale || row.description, status: '已确认', source: '支付宝交易号 ' + row.transaction_id,
      });
    }
    return rows.sort((a, b) => a.project.localeCompare(b.project, 'zh-CN') || a.flow.localeCompare(b.flow, 'zh-CN') || a.date.localeCompare(b.date));
  }
  function csvCell(value, numeric = false) {
    const text = String(value ?? '');
    const safe = !numeric && /^[\s]*[=+\-@\t\r]/.test(text) ? "'" + text : text;
    return '"' + safe.replaceAll('"', '""') + '"';
  }
  function download(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = fileName; link.style.display = 'none';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
  }
  function exportCsv() {
    const rows = deriveLedger();
    const lines = [["类型", "项目", "收支", "日期", "条目", "金额", "经手人", "备注", "核对状态", "来源"].map((value) => csvCell(value)).join(',')];
    const append = (cells) => lines.push(cells.map((value, index) => csvCell(value, index === 5)).join(','));
    const groups = groupLedger(rows);
    let allIncome = 0, allExpense = 0;
    for (const [project, projectRows] of groups) {
      let projectIncome = 0, projectExpense = 0;
      for (const flow of ['收入', '支出']) {
        const subset = projectRows.filter((row) => row.flow === flow);
        for (const row of subset) append(['明细', row.project, row.flow, row.date, row.item, amountText(row.value), row.handler, row.note, row.status, row.source]);
        const subtotal = subset.reduce((sum, row) => sum + row.value, 0);
        if (flow === '收入') projectIncome = subtotal; else projectExpense = subtotal;
        append(['项目小计', project, flow, '', flow + '小计', amountText(subtotal), '', '', '', '']);
      }
      append(['项目小计', project, '', '', '项目差额', amountText(projectIncome - projectExpense), '', '', '', '']);
      allIncome += projectIncome; allExpense += projectExpense;
    }
    append(['全账合计', '全部项目', '收入', '', '总收入', amountText(allIncome), '', '', '', '']);
    append(['全账合计', '全部项目', '支出', '', '总支出', amountText(allExpense), '', '', '', '']);
    append(['全账合计', '全部项目', '', '', '账面差额', amountText(allIncome - allExpense), '', '', '', '']);
    download(new Blob(['\ufeff' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }), '小扎账本_核对结果_' + safeFileName(state.dataset.period) + '.csv');
    announce('已生成 WPS 可打开的账本 CSV。');
  }
  function groupLedger(rows) {
    const map = new Map();
    for (const row of rows) map.set(row.project, [...(map.get(row.project) || []), row]);
    return [...map].sort((a, b) => a[0] === '待分项目' ? 1 : b[0] === '待分项目' ? -1 : a[0].localeCompare(b[0], 'zh-CN'));
  }
  function validateDecision(value, keys) {
    return value && typeof value.key === 'string' && keys.has(value.key) && ['yes', 'no'].includes(value.answer) &&
      (value.project == null || typeof value.project === 'string' && value.project.length <= 120) &&
      (value.item == null || typeof value.item === 'string' && value.item.length <= 250) &&
      (value.amount_cents == null || Number.isSafeInteger(value.amount_cents) && value.amount_cents >= 0 && value.amount_cents <= 10_000_000_000) &&
      typeof value.updated_at === 'string';
  }
  function decisionsArray() { return [...state.decisions.values()].sort((a, b) => a.key.localeCompare(b.key)); }
  async function saveDecisions() {
    const encrypted = await encryptJson({ format: 'xz-decisions', version: 1, datasetId: state.datasetId, decisions: decisionsArray() }, state.key);
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ format: 'xz-local-state', version: 1, datasetId: state.datasetId, ...encrypted }));
  }
  async function restoreDecisions() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return;
    const envelope = JSON.parse(stored);
    if (envelope.format !== 'xz-local-state' || envelope.datasetId !== state.datasetId) {
      throw new Error('本机保存的判断属于另一版账本，请先下载旧版备份再切换。');
    }
    const payload = await decryptJson(envelope, state.key);
    const keys = new Set(state.cards.map((card) => card.key));
    if (payload.format !== 'xz-decisions' || payload.datasetId !== state.datasetId || !Array.isArray(payload.decisions) || payload.decisions.some((item) => !validateDecision(item, keys))) throw new Error('本机判断数据无法校验，请保留原文件并联系整理者。');
    state.decisions = new Map(payload.decisions.map((item) => [item.key, item]));
  }
  async function unlock(code) {
    if (!storageAvailable) throw new Error('这个浏览器不允许保存核账判断，请在手机系统浏览器中打开链接。');
    if (!crypto?.subtle) throw new Error('此浏览器未提供加密功能，请在手机浏览器中打开 HTTPS 链接。');
    if (!code || code.length < 20) throw new Error('请输入完整访问码。');
    const response = await fetch('./data.enc.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('加密账本未加载，请稍后重试。');
    const envelope = await response.json();
    if (envelope.format !== 'xz-ledger-seed' || envelope.version !== 1 || envelope.kdf !== 'PBKDF2-SHA256' || envelope.iterations !== 600000) throw new Error('账本格式不兼容。');
    const key = await deriveKey(code, b64Bytes(envelope.salt), envelope.iterations);
    let plaintext;
    try { plaintext = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64Bytes(envelope.iv) }, key, b64Bytes(envelope.ciphertext)); }
    catch { throw new Error('访问码不正确，或加密账本已损坏。'); }
    const dataset = JSON.parse(dec.decode(plaintext));
    if (!validateDataset(dataset)) throw new Error('账本数据校验失败。');
    state.dataset = dataset;
    state.datasetId = await hashHex(plaintext);
    state.key = key;
    state.code = code;
    state.cards = buildCards(dataset);
    if (state.cards.length !== 497 || new Set(state.cards.map((card) => card.key)).size !== 497) throw new Error('核对卡片数量异常。');
    try { await restoreDecisions(); }
    catch (error) {
      state.dataset = null; state.key = null; state.code = ''; state.cards = [];
      throw error;
    }
    state.message = '';
    render();
  }
  async function unlockWithLocalPassword(password) {
    const wrap = JSON.parse(localStorage.getItem(WRAP_KEY) || 'null');
    if (!wrap || wrap.format !== 'xz-code-wrap' || wrap.version !== 1 || wrap.iterations !== 600000) throw new Error('本机密码记录不存在，请改用访问码。');
    const key = await deriveKey(password, b64Bytes(wrap.salt), wrap.iterations);
    let payload;
    try { payload = await decryptJson(wrap, key); }
    catch { throw new Error('本机密码不正确。'); }
    if (payload.format !== 'xz-access-code' || typeof payload.code !== 'string') throw new Error('本机密码记录损坏，请改用访问码。');
    await unlock(payload.code);
  }
  async function setLocalPassword(password, confirm) {
    if (password !== confirm) throw new Error('两次输入的密码不一致。');
    if (password.length < 8 || password.length > 200) throw new Error('本机密码需为 8 至 200 个字符。');
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await deriveKey(password, salt, 600000);
    const encrypted = await encryptJson({ format: 'xz-access-code', code: state.code }, key);
    localStorage.setItem(WRAP_KEY, JSON.stringify({ format: 'xz-code-wrap', version: 1, iterations: 600000, salt: bytesB64(salt), ...encrypted }));
    state.passwordDialog = false;
    state.unlockMode = 'local';
    state.message = '本机密码已设置。下次在这台设备打开时可用它解锁。';
    render();
  }
  function lock() {
    state.dataset = null; state.datasetId = ''; state.key = null; state.code = '';
    state.cards = []; state.decisions = new Map(); state.lastAction = null; state.pendingImport = null;
    state.message = ''; state.backupText = ''; state.pasteOpen = false; state.passwordDialog = false;
    render();
  }
  function announce(message) { state.message = message; render(); }
  function currentQueue() {
    const lower = state.search.trim().toLowerCase();
    const selected = state.cards.filter((card) => {
      const done = state.decisions.has(card.key);
      if (state.queue === 'priority' && (done || card.priority < 3)) return false;
      if (state.queue === 'all' && done) return false;
      if (state.queue === 'done' && !done) return false;
      return !lower || card.searchText.includes(lower);
    });
    if (state.queue === 'done') selected.sort((a, b) => (state.decisions.get(b.key)?.updated_at || '').localeCompare(state.decisions.get(a.key)?.updated_at || ''));
    return selected;
  }
  function activeCard() {
    const queue = currentQueue();
    return queue.find((card) => card.key === state.selectedKey) || queue[0] || null;
  }
  function resetDraft(card) {
    const decision = card ? state.decisions.get(card.key) : null;
    state.editOpen = false;
    state.draft = { project: decision?.project || '', item: decision?.item || '', amount: decision?.amount_cents == null ? '' : amountText(decision.amount_cents) };
  }
  function selectCard(key) {
    state.selectedKey = key;
    resetDraft(state.cards.find((item) => item.key === key));
    render();
  }
  async function choose(answer) {
    if (state.busy) return;
    const card = activeCard();
    if (!card) return;
    const amountRaw = state.draft.amount.trim();
    if (state.editOpen && amountRaw && !/^\d+(\.\d{1,2})?$/.test(amountRaw)) return announce('金额须为非负数，最多两位小数。');
    const project = state.draft.project.trim();
    const item = state.draft.item.trim();
    if (state.editOpen && (project.length > 120 || item.length > 250)) return announce('项目或名称过长，请缩短后重试。');
    const previous = state.decisions.get(card.key) || null;
    const next = { key: card.key, answer,
      project: state.editOpen ? project || null : previous?.project ?? null,
      item: state.editOpen ? item || null : previous?.item ?? null,
      amount_cents: state.editOpen ? amountRaw ? cents(Number(amountRaw)) : null : previous?.amount_cents ?? null,
      updated_at: new Date().toISOString() };
    if (!validateDecision(next, new Set([card.key]))) return announce('金额超出允许范围。');
    state.busy = true;
    state.decisions.set(card.key, next);
    state.lastAction = { key: card.key, previous, title: card.title };
    state.selectedKey = null;
    state.message = '';
    render();
    try { await saveDecisions(); }
    catch {
      if (previous) state.decisions.set(card.key, previous); else state.decisions.delete(card.key);
      state.lastAction = null; state.selectedKey = card.key;
      state.message = '保存失败，刚才的判断已恢复。请检查浏览器存储空间。';
    }
    state.busy = false;
    resetDraft(activeCard());
    render();
  }
  async function undo() {
    if (!state.lastAction || state.busy) return;
    state.busy = true;
    const { key, previous } = state.lastAction;
    const current = state.decisions.get(key);
    if (previous) state.decisions.set(key, previous); else state.decisions.delete(key);
    state.lastAction = null;
    state.selectedKey = key;
    render();
    try { await saveDecisions(); state.message = '已撤销，可以重新判断。'; }
    catch { if (current) state.decisions.set(key, current); state.message = '撤销保存失败，原判断已恢复。'; }
    state.busy = false; resetDraft(activeCard()); render();
  }
  async function exportBackup() {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await deriveKey(state.code, salt, 600000);
    const payload = { format: 'xz-ledger-backup-payload', version: 1, datasetId: state.datasetId, savedAt: new Date().toISOString(), decisions: decisionsArray() };
    const encrypted = await encryptJson(payload, key);
    const envelope = { format: 'xz-ledger-backup', version: 1, kdf: 'PBKDF2-SHA256', iterations: 600000, salt: bytesB64(salt), ...encrypted };
    state.backupText = JSON.stringify(envelope);
    download(new Blob([state.backupText], { type: 'application/json' }), '小扎核账判断备份_' + new Date().toISOString().slice(0, 10) + '.json');
    state.message = '已生成加密判断备份。若微信未下载成功，可复制下方备份文本。';
    render();
  }
  async function inspectImportText(text, fileName) {
    if (!text || text.length > 5_000_000) throw new Error('备份内容过大或为空。');
    const envelope = JSON.parse(text);
    if (envelope.format !== 'xz-ledger-backup' || envelope.version !== 1 || envelope.kdf !== 'PBKDF2-SHA256' || envelope.iterations !== 600000) throw new Error('请选择本页面导出的判断备份 JSON。');
    const key = await deriveKey(state.code, b64Bytes(envelope.salt), envelope.iterations);
    let payload;
    try { payload = await decryptJson(envelope, key); }
    catch { throw new Error('备份解密失败：访问码不一致或文件损坏。'); }
    const keys = new Set(state.cards.map((card) => card.key));
    if (payload.format !== 'xz-ledger-backup-payload' || payload.datasetId !== state.datasetId || !Array.isArray(payload.decisions) || payload.decisions.some((item) => !validateDecision(item, keys))) throw new Error('备份与当前账本不匹配，已拒绝导入。');
    const incoming = new Map(payload.decisions.map((item) => [item.key, item]));
    if (incoming.size !== payload.decisions.length) throw new Error('备份有重复条目，已拒绝导入。');
    const conflicts = [];
    let fresh = 0;
    for (const [key, value] of incoming) {
      const local = state.decisions.get(key);
      if (!local) { fresh++; continue; }
      if (JSON.stringify([local.answer, local.project, local.item, local.amount_cents]) !== JSON.stringify([value.answer, value.project, value.item, value.amount_cents])) conflicts.push(key);
    }
    state.pendingImport = { incoming, conflicts, fresh, fileName };
    state.pasteOpen = false;
    render();
  }
  async function inspectImport(file) {
    if (!file || file.size > 5_000_000) throw new Error('备份文件过大或不存在。');
    await inspectImportText(await file.text(), file.name);
  }
  async function applyImport(overwrite) {
    if (!state.pendingImport || state.busy) return;
    const previous = new Map(state.decisions);
    let count = 0;
    for (const [key, value] of state.pendingImport.incoming) {
      if (!state.decisions.has(key) || overwrite && state.pendingImport.conflicts.includes(key)) { state.decisions.set(key, value); count++; }
    }
    state.busy = true;
    try {
      await saveDecisions();
      state.pendingImport = null;
      state.message = '已导入 ' + count + ' 条判断' + (overwrite ? '，冲突已按备份覆盖。' : '，已有判断保持不变。');
    } catch {
      state.decisions = previous;
      state.message = '导入保存失败，本机判断未改动。';
    }
    state.busy = false; render();
  }

  function renderLocked() {
    app.innerHTML = `
      <main class="auth-screen"><form id="unlock-form" class="auth-card">
        <div class="auth-icon" aria-hidden="true">✓</div>
        <p class="eyebrow">小扎核账台</p>
        <h1>打开账本，逐笔核对</h1>
        <p class="auth-help">${state.unlockMode === 'local' ? '输入这台设备设置的本机密码。换手机仍需访问码和判断备份。' : '输入访问码打开。账目和判断在这台设备上加密处理；请妥善保存访问码。'}</p>
        <label class="auth-field">${state.unlockMode === 'local' ? '本机密码' : '访问码'}<input id="access-code" type="password" autocomplete="off" autocapitalize="none" spellcheck="false" required minlength="${state.unlockMode === 'local' ? '8' : '20'}" placeholder="${state.unlockMode === 'local' ? '输入本机密码' : '输入完整访问码'}"></label>
        <button class="auth-button" type="submit" ${state.busy ? 'disabled' : ''}>${state.busy ? '正在解锁…' : '打开小扎账本'}</button>
        ${state.message ? `<p class="auth-message" role="alert">${esc(state.message)}</p>` : ''}
        ${hasLocalPassword() ? `<button type="button" class="text-button mode-button" data-action="switch-unlock">${state.unlockMode === 'local' ? '改用访问码' : '改用本机密码'}</button>` : ''}
        ${!storageAvailable ? '<p class="auth-message" role="alert">这个浏览器不允许保存判断，请在手机系统浏览器中打开链接。</p>' : ''}
        <p class="auth-foot">这份网页含加密账本。访问码不会写入公开网页或链接。</p>
      </form></main>`;
  }
  function renderCard(card, queue) {
    if (!card) {
      const text = state.search ? '没有找到这笔流水' : state.queue === 'priority' ? '优先账目都判断完了' : state.queue === 'all' ? '全部账目都判断完了' : '还没有完成的判断';
      return `<article class="card empty"><div class="empty-icon">✓</div><h2>${text}</h2><p>${state.search ? '换个姓名、商户或日期试试。' : state.queue === 'priority' ? '继续核对全部流水，或查看当前账本。' : '你可以随时打开已完成账目修改判断。'}</p>${state.queue === 'priority' && !state.search ? '<button data-action="all" class="secondary-button">继续全部流水</button>' : ''}</article>`;
    }
    const decision = state.decisions.get(card.key);
    const index = queue.findIndex((item) => item.key === card.key) + 1;
    const projectNames = [...new Set(state.dataset.entries.map((entry) => entry.project))].sort((a, b) => a.localeCompare(b, 'zh-CN'));
    return `<article class="card" id="active-card">
      <div class="card-top"><span class="step">${state.queue === 'done' ? '已完成' : '待判断'} · ${index} / ${queue.length}</span><span class="source-tag">${esc(card.source)}</span></div>
      <div class="card-body"><div class="question-label">请判断这一笔</div><h2 class="question">${esc(card.question)}</h2>
        <div class="transaction"><div class="transaction-header"><span class="transaction-name">${esc(card.title)}</span><strong class="transaction-amount ${card.flow === '收入' ? 'in' : 'out'}">${card.flow === '收入' ? '+' : card.flow === '支出' ? '−' : ''}${money(card.value)}</strong></div>
          <div class="transaction-meta"><span>${esc(shortDate(card.date))}</span><span>${esc(card.flow)}</span><span>建议：${esc(card.project)}</span></div></div>
        <details class="evidence"><summary>查看原始依据</summary><p>${esc(card.reason)}</p></details>
        <div class="effect">${esc(card.effect)}</div>
        ${card.editable ? `<button type="button" data-action="edit" class="edit-toggle" aria-expanded="${state.editOpen}">✎ 调整项目、名称或金额 ${state.editOpen ? '⌃' : '⌄'}</button>
          ${state.editOpen ? `<div class="edit-panel"><div class="edit-grid">
            <label>项目<input id="draft-project" list="project-options" value="${esc(state.draft.project)}" placeholder="${esc(card.project)}"><datalist id="project-options">${projectNames.map((name) => `<option value="${esc(name)}"></option>`).join('')}</datalist></label>
            <label>金额（元）<input id="draft-amount" inputmode="decimal" value="${esc(state.draft.amount)}" placeholder="${amountText(card.value)}"></label>
            <label class="wide">账目名称<input id="draft-item" value="${esc(state.draft.item)}" placeholder="${esc(card.title)}"></label>
            </div><p class="edit-hint">留空沿用原值。原始流水不会被改写。</p></div>` : ''}` : ''}
      </div>
      <div class="answer-area">${decision ? `<div class="status-banner">当前判断：${decision.answer === 'yes' ? '是' : '不是'}。下方可改判。</div>` : ''}
        <div class="answer-buttons"><button type="button" data-action="yes" class="answer-yes" ${state.busy ? 'disabled' : ''}>✓ 是，正确</button><button type="button" data-action="no" class="answer-no" ${state.busy ? 'disabled' : ''}>× 不是</button></div>
        <div class="answer-foot">点完自动进入下一笔；随时可改判或撤销。</div>
        ${state.queue !== 'done' && queue.length > 1 ? `<button type="button" class="skip-button" data-action="skip">这笔先跳过</button>` : ''}
      </div>
    </article>`;
  }
  function renderLedger(groups) {
    return `<section aria-label="当前账本">
      <div class="ledger-head"><div><h2>当前账本</h2><p>按项目分开列出收入与支出。你每点一笔，金额立即变化。</p></div>
        <div class="export-actions"><button type="button" class="export-button" data-action="export-csv">导出 WPS 账本 CSV</button><button type="button" class="secondary-button" data-action="backup">生成加密判断备份</button><button type="button" class="secondary-button" data-action="import">从文件导入</button><button type="button" class="secondary-button" data-action="import-paste">粘贴备份导入</button><button type="button" class="secondary-button" data-action="set-password">设置本机密码</button></div></div>
      <div class="project-list">${groups.map(([project, rows]) => {
        const income = rows.filter((row) => row.flow === '收入');
        const expense = rows.filter((row) => row.flow === '支出');
        const incomeCents = income.reduce((sum, row) => sum + row.value, 0);
        const expenseCents = expense.reduce((sum, row) => sum + row.value, 0);
        const line = (row) => `<div class="ledger-row"><span class="ledger-date">${esc(row.date)}</span><span class="ledger-item">${esc(row.item)}<small>${esc(row.status)} · ${esc(row.handler)}</small>${row.note ? `<small>${esc(row.note)}</small>` : ''}</span><strong class="ledger-amount">${money(row.value)}</strong></div>`;
        return `<details class="project"><summary><strong class="project-title">${esc(project)}</strong><span class="project-numbers">收入<strong>${money(incomeCents)}</strong></span><span class="project-numbers">支出<strong>${money(expenseCents)}</strong></span><span class="project-numbers net">差额<strong>${money(incomeCents - expenseCents)}</strong></span><span class="project-arrow">⌄</span></summary><div class="project-content">
          <div class="flow-heading"><span>收入 · ${income.length} 笔</span><span>${money(incomeCents)}</span></div>${income.length ? income.map(line).join('') : '<div class="ledger-empty">暂无收入</div>'}
          <div class="flow-heading out"><span>支出 · ${expense.length} 笔</span><span>${money(expenseCents)}</span></div>${expense.length ? expense.map(line).join('') : '<div class="ledger-empty">暂无支出</div>'}
        </div></details>`;
      }).join('')}</div>
      <div class="notice">原账未核条目暂时保留；微信资金往来和全额退款不自动计入项目收支；支付宝个人流水只有点“是”才新增。账面差额不是公司净利润。判断保存在本机，换手机请先下载备份并在新设备导入。手机微信内能否直接下载文件仍需实机验证。</div>
    </section>`;
  }
  function renderImportDialog() {
    if (!state.pendingImport) return '';
    const { incoming, conflicts, fresh, fileName } = state.pendingImport;
    return `<div class="dialog-backdrop"><div class="dialog" role="dialog" aria-modal="true" aria-label="检查判断备份">
      <h2>检查判断备份</h2><p class="dialog-file">${esc(fileName)}</p>
      <p>备份包含 <strong>${incoming.size}</strong> 条判断，可新增 <strong>${fresh}</strong> 条，与本机不同的判断有 <strong>${conflicts.length}</strong> 条。</p>
      <p>请选导入方式。原账及流水不会被覆盖。</p>
      <div class="dialog-actions"><button data-action="import-keep" class="auth-button" ${state.busy ? 'disabled' : ''}>仅补充未判断条目</button>
        ${conflicts.length ? `<button data-action="import-overwrite" class="secondary-button" ${state.busy ? 'disabled' : ''}>用备份覆盖 ${conflicts.length} 条冲突</button>` : ''}
        <button data-action="import-cancel" class="text-button">取消</button></div>
    </div></div>`;
  }
  function renderBackupDialog() {
    if (!state.backupText) return '';
    return `<div class="dialog-backdrop"><div class="dialog" role="dialog" aria-modal="true" aria-label="加密判断备份">
      <h2>加密判断备份已生成</h2><p>若手机微信没有下载文件，点“复制备份文本”，保存到你自己的文档。下次可粘贴导入。</p>
      <textarea id="backup-text" readonly spellcheck="false" aria-label="完整加密判断备份文本">${esc(state.backupText)}</textarea>
      <div class="dialog-actions"><button type="button" class="auth-button" data-action="copy-backup">复制备份文本</button><button type="button" class="text-button" data-action="close-backup">完成</button></div>
    </div></div>`;
  }
  function renderPasteDialog() {
    if (!state.pasteOpen) return '';
    return `<div class="dialog-backdrop"><div class="dialog" role="dialog" aria-modal="true" aria-label="粘贴判断备份">
      <h2>粘贴加密判断备份</h2><p>粘贴之前复制的完整文本，然后检查新增和冲突。</p>
      <textarea id="import-paste-text" spellcheck="false" placeholder="在此粘贴完整备份文本"></textarea>
      <div class="dialog-actions"><button type="button" class="auth-button" data-action="check-paste">检查备份</button><button type="button" class="text-button" data-action="close-paste">取消</button></div>
    </div></div>`;
  }
  function renderPasswordDialog() {
    if (!state.passwordDialog) return '';
    return `<div class="dialog-backdrop"><form id="password-form" class="dialog" role="dialog" aria-modal="true" aria-label="设置本机密码">
      <h2>设置本机密码</h2><p>以后在这台设备可用自设密码打开。换手机或浏览器缓存清除后，仍需原访问码。</p>
      <label class="auth-field">本机密码<input id="new-password" type="password" autocomplete="new-password" required minlength="8" placeholder="至少 8 个字符"></label>
      <label class="auth-field">再输入一次<input id="confirm-password" type="password" autocomplete="new-password" required minlength="8"></label>
      <div class="dialog-actions"><button type="submit" class="auth-button">保存本机密码</button><button type="button" class="text-button" data-action="close-password">取消</button></div>
    </form></div>`;
  }
  function render() {
    if (!state.dataset) return renderLocked();
    const ledger = deriveLedger();
    const groups = groupLedger(ledger);
    const totalIncome = ledger.filter((row) => row.flow === '收入').reduce((sum, row) => sum + row.value, 0);
    const totalExpense = ledger.filter((row) => row.flow === '支出').reduce((sum, row) => sum + row.value, 0);
    const pending = ledger.filter((row) => row.project === '待分项目').reduce((sum, row) => sum + (row.flow === '收入' ? row.value : -row.value), 0);
    const reviewed = state.cards.filter((card) => state.decisions.has(card.key)).length;
    const priorityRemaining = state.cards.filter((card) => card.priority >= 3 && !state.decisions.has(card.key)).length;
    const queue = currentQueue();
    const card = activeCard();
    app.innerHTML = `<main class="shell">
      <header class="topbar"><div class="brand"><span class="brand-mark">✓</span><span>小扎核账台</span></div><div class="topbar-actions"><span class="period">${esc(state.dataset.period)}</span><button type="button" class="signout-button" data-action="lock">锁定</button></div></header>
      <div class="layout ${state.tab === 'review' ? 'review-mode' : ''}">
        <div class="intro"><div><p class="eyebrow">ONE BY ONE · 一笔一笔来</p><h1>每笔点一下，账本就清楚一点。</h1><p>看清用途，点“是”或“不是”，项目金额会即刻变化。</p></div><button type="button" class="overview-link" data-action="${state.tab === 'review' ? 'ledger' : 'review'}">${state.tab === 'review' ? '查看当前账本' : '继续核对'}</button></div>
        <section class="stats" aria-label="核账进度与汇总">
          <div class="stat primary"><div class="stat-label">已判断</div><div class="stat-value">${reviewed} <span class="stat-sub">/ ${state.cards.length} 笔</span></div><div class="progress-track" role="progressbar" aria-valuenow="${reviewed}" aria-valuemin="0" aria-valuemax="${state.cards.length}"><span class="progress-fill" style="width:${reviewed / state.cards.length * 100}%"></span></div></div>
          <div class="stat"><div class="stat-label">当前收入</div><div class="stat-value">${money(totalIncome)}</div><div class="stat-note">含尚待确认的原账</div></div>
          <div class="stat"><div class="stat-label">当前支出</div><div class="stat-value">${money(totalExpense)}</div><div class="stat-note">按退款后金额统计</div></div>
          <div class="stat"><div class="stat-label">当前账面差额</div><div class="stat-value">${money(totalIncome - totalExpense)}</div><div class="stat-note">待分项目净额 ${money(pending)}</div></div>
        </section>
        <nav class="tabs" aria-label="主视图"><button type="button" class="tab ${state.tab === 'review' ? 'active' : ''}" data-action="review">逐笔核对</button><button type="button" class="tab ${state.tab === 'ledger' ? 'active' : ''}" data-action="ledger">当前账本</button></nav>
        ${state.message ? `<div class="status-banner" role="status">${esc(state.message)} <button type="button" data-action="clear-message" aria-label="关闭提示">×</button></div>` : ''}
        ${state.tab === 'review' ? `<div class="review-grid"><section class="left-column" aria-label="待核账目">
          <div class="toolbar"><div class="segment" role="group" aria-label="流水范围"><button type="button" class="${state.queue === 'priority' ? 'active' : ''}" data-action="priority">优先待核 ${priorityRemaining}</button><button type="button" class="${state.queue === 'all' ? 'active' : ''}" data-action="all">全部待核 ${state.cards.length - reviewed}</button><button type="button" class="${state.queue === 'done' ? 'active' : ''}" data-action="done">已完成 ${reviewed}</button></div><div class="search-wrap"><span class="search-icon">⌕</span><input id="search" type="search" value="${esc(state.search)}" placeholder="搜索姓名、商户或日期" aria-label="搜索账目"></div></div>
          ${renderCard(card, queue)}
          ${state.queue === 'done' && queue.length > 1 ? `<div class="side-panel done-list"><h2>已判断的账目</h2><p>点一笔即可改判。</p><div class="recent-list">${queue.slice(0, 40).map((item) => `<button type="button" class="recent-item" data-select="${esc(item.key)}"><span class="answer-chip ${state.decisions.get(item.key)?.answer === 'no' ? 'no' : ''}">${state.decisions.get(item.key)?.answer === 'yes' ? '是' : '不是'}</span><span class="recent-text">${esc(item.title)}</span></button>`).join('')}</div>${queue.length > 40 ? '<p>可搜索更早的账目。</p>' : ''}</div>` : ''}
        </section><aside><div class="side-panel"><h2>账本正在变清楚</h2><p>你的判断会立刻反映在金额里。</p><div class="side-line"><span>项目收入</span><strong>${money(totalIncome)}</strong></div><div class="side-line"><span>项目支出</span><strong>${money(totalExpense)}</strong></div><div class="side-line total"><span>账面差额</span><strong>${money(totalIncome - totalExpense)}</strong></div><div class="hint-box">待分项目净额 ${money(pending)}，需要继续核实归属。</div></div></aside></div>` : renderLedger(groups)}
      </div>
      ${state.lastAction ? `<div class="undo-bar" role="status"><span>${state.busy ? '正在保存这一笔…' : '这一笔已保存在本机'}</span><button type="button" data-action="undo" ${state.busy ? 'disabled' : ''}>↶ 撤销上一步</button></div>` : ''}
      <nav class="mobile-nav ${state.tab === 'review' && card ? 'mobile-actions' : ''}" aria-label="手机快速操作">
        ${state.tab === 'review' && card ? `<button type="button" class="mobile-yes" data-action="yes" ${state.busy ? 'disabled' : ''}>✓<span>是，正确</span></button><button type="button" class="mobile-no" data-action="no" ${state.busy ? 'disabled' : ''}>×<span>不是</span></button><button type="button" class="mobile-ledger" data-action="ledger">▤<span>账本</span></button>` : `<button type="button" data-action="review">✓<span>逐笔核对</span></button><button type="button" data-action="ledger">▤<span>当前账本</span></button>`}
      </nav>
      <input id="import-file" type="file" accept=".json,application/json" hidden>
      ${renderImportDialog()}${renderBackupDialog()}${renderPasteDialog()}${renderPasswordDialog()}
    </main>`;
  }

  app.addEventListener('submit', async (event) => {
    if (event.target.id !== 'unlock-form') return;
    event.preventDefault();
    const code = document.querySelector('#access-code').value.trim();
    state.busy = true; state.message = ''; render();
    try { if (state.unlockMode === 'local') await unlockWithLocalPassword(code); else await unlock(code); }
    catch (error) { state.message = error instanceof Error ? error.message : '无法打开账本。'; state.busy = false; render(); return; }
    state.busy = false; render();
  });
  app.addEventListener('submit', async (event) => {
    if (event.target.id !== 'password-form') return;
    event.preventDefault();
    const password = document.querySelector('#new-password').value;
    const confirm = document.querySelector('#confirm-password').value;
    try { await setLocalPassword(password, confirm); }
    catch (error) { announce(error instanceof Error ? error.message : '本机密码保存失败。'); }
  });
  let searchComposing = false;
  app.addEventListener('compositionstart', (event) => { if (event.target.id === 'search') searchComposing = true; });
  app.addEventListener('compositionend', (event) => {
    if (event.target.id !== 'search') return;
    searchComposing = false;
    state.search = event.target.value; state.selectedKey = null;
    render(); document.querySelector('#search')?.focus();
  });
  app.addEventListener('input', (event) => {
    const id = event.target.id;
    if (id === 'search') {
      state.search = event.target.value; state.selectedKey = null;
      if (searchComposing) return;
      const start = event.target.selectionStart;
      render();
      const next = document.querySelector('#search');
      next?.focus();
      try { next?.setSelectionRange(start, start); } catch { /* type=search on some browsers */ }
    } else if (id === 'draft-project') state.draft.project = event.target.value;
    else if (id === 'draft-item') state.draft.item = event.target.value;
    else if (id === 'draft-amount') state.draft.amount = event.target.value;
  });
  app.addEventListener('change', async (event) => {
    if (event.target.id !== 'import-file') return;
    try { await inspectImport(event.target.files?.[0]); }
    catch (error) { announce(error instanceof Error ? error.message : '无法读取备份。'); }
  });
  app.addEventListener('click', async (event) => {
    const selected = event.target.closest('[data-select]');
    if (selected) return selectCard(selected.dataset.select);
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const action = button.dataset.action;
    if (['priority', 'all', 'done'].includes(action)) {
      state.queue = action; state.selectedKey = null; state.search = ''; resetDraft(null); render();
    } else if (['review', 'ledger'].includes(action)) {
      state.tab = action; state.selectedKey = null; resetDraft(null); render(); window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (action === 'yes' || action === 'no') await choose(action);
    else if (action === 'edit') { state.editOpen = !state.editOpen; render(); }
    else if (action === 'skip') {
      const queue = currentQueue(); const card = activeCard(); const index = queue.findIndex((item) => item.key === card?.key);
      if (index >= 0) selectCard(queue[(index + 1) % queue.length].key);
    } else if (action === 'undo') await undo();
    else if (action === 'lock') lock();
    else if (action === 'switch-unlock') { state.unlockMode = state.unlockMode === 'local' ? 'code' : 'local'; state.message = ''; render(); }
    else if (action === 'clear-message') { state.message = ''; render(); }
    else if (action === 'export-csv') exportCsv();
    else if (action === 'backup') {
      try { await exportBackup(); } catch { announce('备份生成失败，请稍后重试。'); }
    } else if (action === 'import') document.querySelector('#import-file').click();
    else if (action === 'import-paste') { state.pasteOpen = true; render(); }
    else if (action === 'check-paste') {
      try { await inspectImportText(document.querySelector('#import-paste-text').value.trim(), '粘贴的加密备份'); }
      catch (error) { announce(error instanceof Error ? error.message : '无法读取备份。'); }
    }
    else if (action === 'close-paste') { state.pasteOpen = false; render(); }
    else if (action === 'copy-backup') {
      try { await navigator.clipboard.writeText(state.backupText); state.message = '加密备份文本已复制。'; state.backupText = ''; render(); }
      catch { const area = document.querySelector('#backup-text'); area.focus(); area.select(); }
    }
    else if (action === 'close-backup') { state.backupText = ''; render(); }
    else if (action === 'set-password') { state.passwordDialog = true; render(); }
    else if (action === 'close-password') { state.passwordDialog = false; render(); }
    else if (action === 'import-cancel') { state.pendingImport = null; render(); }
    else if (action === 'import-keep') await applyImport(false);
    else if (action === 'import-overwrite') await applyImport(true);
  });
  renderLocked();
})();
