(()=>{
  const FALLBACK = 'data:image/svg+xml;utf8,'+
    encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="400" height="220"><rect width="100%" height="100%" fill="#0f1115"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="#94a3b8" font-family="Inter,Arial" font-size="22">No Image</text></svg>`);

  const esc = (s='') => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',''':'&#39;'}[c]));

  function card(i){
    const img = i.imageUrl ? `<img src="${esc(i.imageUrl)}" onerror="this.src='${FALLBACK}'" alt="">` : `<img src="${FALLBACK}" alt="">`;
    return `
      <article class="card">
        <a class="card-media" href="${esc(i.link||'#')}" target="_blank" rel="noopener">${img}</a>
        <div class="card-body">
          <div class="card-kicker">${esc(i.source||'')}</div>
          <h3 class="card-title"><a href="${esc(i.link||'#')}" target="_blank" rel="noopener">${esc(i.title||'Untitled')}</a></h3>
          ${i.summary?`<p class="card-text">${esc(i.summary)}</p>`:''}
        </div>
      </article>`;
  }

  async function load(url){
    try{
      // bust cache hourly (matches the cron) to avoid stale JSON
      const bust = `ts=${new Date().getUTCFullYear()}${(new Date().getUTCMonth()+1).toString().padStart(2,'0')}${new Date().getUTCDate().toString().padStart(2,'0')}${new Date().getUTCHours().toString().padStart(2,'0')}`;
      const res = await fetch(`${url}?${bust}`, {cache:'no-store'});
      if(!res.ok) throw new Error('HTTP '+res.status);
      return await res.json();
    }catch(e){
      console.error('Feed load failed for', url, e);
      return [];
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Year in footer
    const y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

    document.querySelectorAll('[data-grid]').forEach(async grid => {
      const url = grid.getAttribute('data-feed');
      const items = await load(url);
      grid.innerHTML = (items||[]).slice(0, 12).map(card).join('') ||
        `<article class="card"><div class="card-body"><h3 class="card-title">No items</h3><p class="card-text">Feed: ${esc(url)}</p></div></article>`;
    });
  });
})();
