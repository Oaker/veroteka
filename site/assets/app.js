
// Тема: светлая по умолчанию, переключатель с запоминанием
const toggle = document.getElementById('themeToggle');
if (localStorage.getItem('vt-theme') === 'dark') document.documentElement.dataset.theme = 'dark';
toggle && toggle.addEventListener('click', () => {
  const d = document.documentElement.dataset.theme === 'dark';
  document.documentElement.dataset.theme = d ? '' : 'dark';
  localStorage.setItem('vt-theme', d ? 'light' : 'dark');
});

// Поиск по search-index.json
const box = document.getElementById('searchbox');
const res = document.getElementById('searchresults');
let INDEX = null;
box && box.addEventListener('input', async (e) => {
  const q = e.target.value.trim().toLowerCase();
  if (q.length < 2) { res.innerHTML = ''; return; }
  if (!INDEX) {
    try { INDEX = await (await fetch('search-index.json')).json(); } catch (err) { return; }
  }
  const hits = INDEX.filter(x =>
    x.title.toLowerCase().includes(q) || x.excerpt.toLowerCase().includes(q)
  ).slice(0, 8);
  res.innerHTML = hits.map(h =>
    '<div class="hit"><a href="' + h.url + '">' + h.title + '</a><div>' + h.excerpt.slice(0,120) + '...</div></div>'
  ).join('');
});
