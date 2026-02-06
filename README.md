# The Streamic - 2026 Edition

A performance-optimized broadcast technology news aggregator with AI Impact Briefs, automated RSS updates, and GEO (Generative Engine Optimization).

## 🚀 What's New in 2026

### Core Features
- **AI Impact Briefs**: Every news item includes a 2-sentence explanation of why it matters to broadcast engineers
- **100-Item Sliding Window**: Intelligent deduplication maintains the most recent 100 unique stories
- **6-Hour Auto-Updates**: GitHub Actions workflow refreshes content automatically
- **GEO-Optimized**: JSON-LD structured data for AI search engine discovery
- **Performance-First**: Sub-1-second load times with lazy loading and optimized CSS

### Architecture Updates
- **Refined Header**: Clean, centered navigation with 7 industry-standard categories
- **Footer Navigation**: About & Contact moved to footer only
- **Enhanced Monitoring**: Real-time metrics tracking for feed health
- **Deduplication Engine**: Content-hash based duplicate detection

## 📁 Project Structure

```
streamic-2026/
├── .github/
│   └── workflows/
│       └── update.yml           # Auto-update every 6 hours
├── scripts/
│   └── fetch_rss.py             # Enhanced RSS aggregator
├── data/                        # Generated JSON feeds
│   ├── news.json               # Master feed (100 items)
│   ├── newsroom.json           # Category feeds
│   ├── playout.json
│   ├── infrastructure.json
│   ├── graphics.json
│   ├── cloud.json
│   ├── streaming.json
│   ├── audio-ai.json
│   └── metrics.json            # Monitoring data
├── assets/
│   ├── logo.png
│   └── fallback.jpg
├── index.html                   # Homepage
├── newsroom.html               # Category pages (7 total)
├── playout.html
├── infrastructure.html
├── graphics.html
├── cloud.html
├── streaming.html
├── audio-ai.html
├── about.html                   # About page
├── contact.html                 # Contact page
├── privacy.html                 # Legal pages
├── terms.html
├── disclaimer.html
├── style.css                    # Main stylesheet
├── app.js                       # Homepage loader
├── category.js                  # Category page loader
└── README.md
```

## 🛠️ Setup & Deployment

### 1. Create GitHub Repository

```bash
# Create new repo on GitHub (e.g., "thestreamic-2026")
git clone https://github.com/YOUR_USERNAME/thestreamic-2026.git
cd thestreamic-2026
```

### 2. Copy Project Files

Copy all files from the `streamic-2026/` directory to your repository:

```bash
# Copy all project files
cp -r /path/to/streamic-2026/* .
```

### 3. Make Python Script Executable

```bash
chmod +x scripts/fetch_rss.py
```

### 4. Initial Commit

```bash
git add .
git commit -m "🚀 Initial commit - The Streamic 2026"
git push origin main
```

### 5. Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Select **Deploy from a branch**
3. Choose **main** branch and **/ (root)** folder
4. Click **Save**

### 6. Run Initial RSS Build

1. Go to **Actions** tab
2. Click **Update RSS Feeds**
3. Click **Run workflow** → **Run workflow**
4. Wait for completion (creates all `data/*.json` files)

### 7. Access Your Site

Your site will be live at: `https://YOUR_USERNAME.github.io/thestreamic-2026/`

## 📊 Monitoring & Metrics

The system automatically tracks:
- Total feeds checked
- Successful/failed fetches
- Total items fetched
- Duplicates removed
- Execution time
- Error logs

View metrics in `data/metrics.json` or GitHub Actions logs.

## 🔄 How It Works

### RSS Aggregation Pipeline

```
1. GitHub Actions triggers every 6 hours (0 */6 * * *)
2. Python script fetches RSS feeds from 20+ sources
3. Parses XML/RSS data using ElementTree
4. Extracts headlines, links, images, descriptions
5. Generates AI Impact Briefs for each item
6. Deduplicates using content hashing
7. Applies 100-item sliding window (newest first)
8. Saves to JSON files in data/ directory
9. Commits changes back to repository
10. GitHub Pages serves updated content
```

### AI Impact Brief Generation

Impact briefs are generated using rule-based logic that:
- Analyzes title and description keywords
- Maps to category-specific impacts
- Explains relevance to broadcast engineers
- Keeps output to 2 sentences maximum

Example:
> "Impacts newsroom workflow efficiency and content management systems. Enables lower latency for ST 2110 workflows."

## 📰 RSS Sources by Category

### Newsroom (NRCS & MAM)
- Dalet
- Avid
- TV Technology

### Playout (Automation & MCR)
- Ross Video
- Imagine Communications
- TV Technology

### Infrastructure (ST 2110 & SDI/IP)
- SMPTE
- TV Technology
- IBC

### Graphics (Vizrt, Ross, & 3D)
- Vizrt
- Newscast Studio
- Ross Video

### Cloud (Remote Edit & SaaS)
- Frame.io
- Adobe
- TV Technology

### Streaming (CDN, OTT, & AWS)
- Streaming Media
- AWS Media
- Broadcasting & Cable

### Audio & AI (AoIP & Captions)
- Pro Sound Network
- TV Technology
- Sports Video Group

## 🎨 Customization

### Add New RSS Feed

Edit `scripts/fetch_rss.py` and add to the appropriate category:

```python
RSS_FEEDS = {
    "newsroom": [
        {"url": "https://example.com/feed.xml", "label": "Example Source"},
        # Add your source here
    ],
    # ...
}
```

### Modify Update Frequency

Edit `.github/workflows/update.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Change to your desired schedule
```

Cron examples:
- Every 3 hours: `0 */3 * * *`
- Every 12 hours: `0 */12 * * *`
- Daily at 6 AM: `0 6 * * *`

### Change Card Layout

Edit `style.css`:

```css
.card-grid {
  grid-template-columns: repeat(5, 1fr);  /* Change number of columns */
}
```

### Update Colors

```css
:root {
  --primary-blue: #0071e3;      /* Change to your brand color */
  --text-primary: #1d1d1f;
  /* ... */
}
```

## 🔍 SEO & GEO Optimization

### JSON-LD Schema
Every page includes structured data for:
- WebSite schema (homepage)
- CollectionPage schema (category pages)
- NewsArticle schema (in progress)

### Performance Optimizations
- Native lazy loading for images
- Minimal CSS (< 50KB)
- No external JavaScript dependencies
- Preconnect hints for external domains
- Service Worker ready (PWA)

### Meta Tags
- Canonical URLs
- Open Graph tags
- Twitter Cards
- Descriptive meta descriptions

## 📈 Performance Metrics

Target benchmarks:
- **First Contentful Paint**: < 1.0s
- **Time to Interactive**: < 2.0s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Lighthouse Score**: > 95

## 🐛 Troubleshooting

### Feeds Not Updating

1. Check GitHub Actions logs for errors
2. Verify RSS feed URLs are accessible
3. Check for XML parsing errors in logs
4. Ensure proper permissions (contents: write)

### Images Not Loading

1. Verify `assets/fallback.jpg` exists
2. Check image URLs in RSS feeds
3. Add CORS headers if needed
4. Use lazy loading attributes

### Categories Not Appearing

1. Verify JSON files exist in `data/` directory
2. Check JavaScript console for errors
3. Ensure category names match in JS and HTML
4. Run RSS script manually to test

## 📧 Contact

**Creator**: Prerak Mehta  
**Email**: itabmum@gmail.com  
**Purpose**: Independent broadcast technology news aggregation

## 📄 License

© 2026 The Streamic – All rights reserved.

This project aggregates content from publicly available RSS feeds. All article content remains the property of the original publishers.

---

**Built with**:
- Python 3.11
- GitHub Actions
- Vanilla JavaScript (no frameworks)
- Semantic HTML5
- Modern CSS Grid

**2026 Standards**: GEO-optimized, AI-ready, performance-first architecture.
