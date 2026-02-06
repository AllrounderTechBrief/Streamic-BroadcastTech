/* =========================================================
   THE STREAMIC – Homepage Loader (2026 Edition)
   Features: Impact briefs, lazy loading, performance optimizations
========================================================= */

(() => {
  /* ---------- Card Renderer with Impact Brief ---------- */
  function renderCard(item) {
    const a = document.createElement('a');
    a.className = 'card';
    a.href = item.link || '#';
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    
    // Image
    const fig = document.createElement('figure');
    fig.className = 'card-image';
    const img = document.createElement('img');
    img.alt = item.source ? `Image from ${item.source}` : 'News image';
    img.loading = 'lazy'; // Native lazy loading
    img.src = item.image || 'assets/fallback.jpg';
    img.addEventListener('error', () => { 
      img.src = 'assets/fallback.jpg'; 
    });
    fig.appendChild(img);
    a.appendChild(fig);
    
    // Body
    const body = document.createElement('div');
    body.className = 'card-body';
    
    const h3 = document.createElement('h3');
    h3.textContent = item.title || 'Untitled';
    
    const source = document.createElement('span');
    source.className = 'source';
    source.textContent = item.source || '';
    
    body.appendChild(h3);
    body.appendChild(source);
    
    // Impact Brief (2026 feature)
    if (item.impactBrief) {
      const impactBrief = document.createElement('p');
      impactBrief.className = 'impact-brief';
      impactBrief.textContent = item.impactBrief;
      body.appendChild(impactBrief);
    }
    
    a.appendChild(body);
    
    return a;
  }
  
  // Export for use in category pages
  window.__streamicRenderCard = renderCard;
  
  /* ---------- Normalize Item ---------- */
  const normalize = (item) => ({
    title: item.title || item.headline || 'Untitled',
    link: item.link || item.url || '#',
    source: item.source || item.site || '',
    image: item.image || item.imageUrl || item.thumbnail || '',
    impactBrief: item.impactBrief || ''
  });
  
  /* ---------- Category to JSON File Mapping ---------- */
  const FEED_MAP = {
    'newsroom': 'data/newsroom.json',
    'playout': 'data/playout.json',
    'infrastructure': 'data/infrastructure.json',
    'graphics': 'data/graphics.json',
    'cloud': 'data/cloud.json',
    'streaming': 'data/streaming.json',
    'audio-ai': 'data/audio-ai.json'
  };
  
  /* ---------- Load Homepage Sections ---------- */
  function loadHomepage() {
    document.querySelectorAll('.home-section').forEach((section) => {
      const grid = section.querySelector('.card-grid');
      if (!grid || !grid.id) return;
      
      // Extract category from grid ID (e.g., "grid-newsroom" -> "newsroom")
      const categoryId = grid.id.replace('grid-', '');
      const feedUrl = FEED_MAP[categoryId];
      
      if (!feedUrl) {
        console.warn(`No feed mapping for category: ${categoryId}`);
        return;
      }
      
      // Fetch and render with error handling
      fetch(feedUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          return response.json();
        })
        .then(items => {
          if (!Array.isArray(items)) {
            console.error(`Invalid data format for ${feedUrl}`);
            return;
          }
          
          // Take first 10 items for homepage
          items.slice(0, 10).map(normalize).forEach(item => {
            grid.appendChild(renderCard(item));
          });
        })
        .catch(error => {
          console.error(`Failed to load ${feedUrl}:`, error);
          // Show user-friendly error
          const errorDiv = document.createElement('div');
          errorDiv.style.cssText = 'grid-column: 1/-1; text-align: center; color: #999; padding: 20px;';
          errorDiv.textContent = 'Unable to load content. Please try again later.';
          grid.appendChild(errorDiv);
        });
    });
  }
  
  /* ---------- Mobile Navigation Toggle ---------- */
  function initMobileNav() {
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.nav-links');
    
    if (toggle && links) {
      toggle.addEventListener('click', () => {
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !isExpanded);
        links.classList.toggle('active');
      });
      
      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !links.contains(e.target)) {
          toggle.setAttribute('aria-expanded', 'false');
          links.classList.remove('active');
        }
      });
    }
  }
  
  /* ---------- Performance: Intersection Observer for Cards ---------- */
  function initIntersectionObserver() {
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src || img.src;
            imageObserver.unobserve(img);
          }
        });
      }, {
        rootMargin: '50px'
      });
      
      // Observe all lazy-loaded images
      document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  }
  
  /* ---------- Initialize ---------- */
  if (document.querySelector('.home')) {
    if (document.readyState !== 'loading') {
      loadHomepage();
      initMobileNav();
      initIntersectionObserver();
    } else {
      document.addEventListener('DOMContentLoaded', () => {
        loadHomepage();
        initMobileNav();
        initIntersectionObserver();
      });
    }
  }
  
  /* ---------- Service Worker Registration (PWA-ready) ---------- */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch(() => {
        // Silently fail if no service worker available
      });
    });
  }
})();
