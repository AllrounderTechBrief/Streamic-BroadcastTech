# Quick Start Guide - 5 Minutes to Deploy

## ⚡ Super Quick Setup

```bash
# 1. Clone your new GitHub repository
git clone https://github.com/YOUR_USERNAME/thestreamic.git
cd thestreamic

# 2. Copy all project files
cp -r /path/to/streamic-2026/* .

# 3. Add your assets (logo and fallback image)
cp /path/to/logo.png assets/
cp /path/to/fallback.jpg assets/

# 4. Commit and push
git add .
git commit -m "🚀 Deploy The Streamic 2026"
git push origin main

# 5. Enable GitHub Pages
# Go to Settings → Pages → Source: main / (root) → Save

# 6. Run initial RSS fetch
# Go to Actions → Update RSS Feeds → Run workflow

# Done! Your site is live at:
# https://YOUR_USERNAME.github.io/thestreamic/
```

## 📦 What You Get

### Files Included
- ✅ 7 category pages with refined navigation
- ✅ Homepage with dynamic content loading
- ✅ About & Contact pages
- ✅ Monitoring dashboard
- ✅ Legal pages (privacy, terms, disclaimer)
- ✅ Python RSS aggregator with AI impact briefs
- ✅ GitHub Actions workflow (6-hour updates)
- ✅ Performance-optimized CSS
- ✅ Responsive JavaScript
- ✅ Complete documentation

### Features Active
- ✅ Automated RSS updates every 6 hours
- ✅ AI Impact Briefs for each article
- ✅ 100-item sliding window with deduplication
- ✅ Real-time monitoring metrics
- ✅ GEO-optimized structured data
- ✅ Sub-1-second load times
- ✅ Mobile-responsive design
- ✅ 5 cards per row layout

## 🎯 Next Steps

### 1. Customize Your Site (5 minutes)
```bash
# Update contact email
find . -name "*.html" -exec sed -i 's/itabmum@gmail.com/your@email.com/g' {} +

# Customize colors (optional)
nano style.css  # Edit CSS variables

# Review RSS sources
nano scripts/fetch_rss.py  # Add/remove sources
```

### 2. Add Your Branding (2 minutes)
```bash
# Create logo (48px height)
convert your-logo.svg -resize x48 assets/logo.png

# Create fallback image (1200x675px)
convert -size 1200x675 xc:'#f5f5f7' \
  -gravity center \
  -pointsize 48 \
  -fill '#6e6e73' \
  -annotate +0+0 'The Streamic' \
  assets/fallback.jpg
```

### 3. Test Your Site (3 minutes)
```bash
# Local preview (Python 3)
python -m http.server 8000

# Open http://localhost:8000 in browser
# Test all pages
# Verify responsive design
```

### 4. Monitor Performance (ongoing)
```bash
# Check monitoring dashboard
open https://YOUR_USERNAME.github.io/thestreamic/monitoring.html

# View GitHub Actions logs
open https://github.com/YOUR_USERNAME/thestreamic/actions

# Run Lighthouse audit
# Chrome DevTools → Lighthouse → Generate report
```

## 🔧 Common Customizations

### Change Update Frequency
```yaml
# Edit .github/workflows/update.yml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours
```

### Add New RSS Source
```python
# Edit scripts/fetch_rss.py
RSS_FEEDS = {
    "newsroom": [
        {"url": "https://newsite.com/feed", "label": "New Site"},
    ]
}
```

### Modify Card Layout
```css
/* Edit style.css */
.card-grid {
  grid-template-columns: repeat(4, 1fr);  /* 4 cards instead of 5 */
}
```

## 📊 Monitoring Your Site

### Check Feed Health
Visit: `https://YOUR_USERNAME.github.io/thestreamic/monitoring.html`

Metrics tracked:
- Total feeds checked
- Success/failure rates
- Items fetched
- Duplicates removed
- Execution times
- Error logs

### GitHub Actions Status
Visit: `https://github.com/YOUR_USERNAME/thestreamic/actions`

Watch for:
- ✅ Green checkmarks (successful runs)
- ❌ Red X's (failures - check logs)
- 🟡 Yellow dots (in progress)

## 🐛 Troubleshooting

### Feeds Not Updating
```bash
# Check GitHub Actions logs
# Verify RSS URLs are accessible
curl -I https://www.tvtechnology.com/rss.xml

# Test locally
python scripts/fetch_rss.py
```

### Images Not Loading
```bash
# Verify assets exist
ls -la assets/

# Check image URLs in browser DevTools
# Update fallback.jpg if needed
```

### Categories Empty
```bash
# Verify JSON files exist
ls -la data/

# Check browser console for errors
# Run RSS script manually first
```

## 📈 Performance Tips

### Optimize Images
```bash
# Install imagemagick
brew install imagemagick  # macOS
sudo apt install imagemagick  # Linux

# Compress images
mogrify -resize 1200x675 -quality 85 assets/*.jpg
mogrify -quality 85 assets/*.png
```

### Run Lighthouse Audit
```
1. Open Chrome DevTools (F12)
2. Click Lighthouse tab
3. Select categories
4. Click "Generate report"
5. Target: All scores > 90
```

## 🚀 Going Live

### Enable Custom Domain
```bash
# 1. Add custom domain in GitHub Pages settings
# 2. Configure DNS records:
#    A    @    185.199.108.153
#    A    @    185.199.109.153
#    A    @    185.199.110.153
#    A    @    185.199.111.153
#    CNAME www  YOUR_USERNAME.github.io
# 3. Wait 24 hours for DNS propagation
# 4. Enable "Enforce HTTPS"
```

### Submit to Search Engines
```bash
# Create sitemap.xml (optional)
# Submit to Google Search Console
# Submit to Bing Webmaster Tools
# Verify structured data with Google's Rich Results Test
```

## 📧 Get Help

- **Documentation**: See README.md, DEPLOYMENT.md, FEATURES.md
- **GitHub Issues**: Create an issue in your repo
- **Email**: itabmum@gmail.com
- **Community**: Share your deployment!

## ✅ Success Checklist

After deployment, verify:
- [ ] Homepage loads with content
- [ ] All 7 category pages work
- [ ] Monitoring dashboard shows metrics
- [ ] Images load (or fallback to placeholder)
- [ ] Mobile responsive design works
- [ ] RSS updates run automatically
- [ ] Lighthouse score > 90

---

**Deployment Time**: 5 minutes  
**Customization**: 15 minutes  
**Total**: 20 minutes to fully customized site

**Built for**: Broadcast engineers | **Powered by**: GitHub Pages | **Cost**: $0
