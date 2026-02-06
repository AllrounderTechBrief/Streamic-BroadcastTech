# Deployment Guide - The Streamic 2026

## Quick Start (5 Minutes)

### Prerequisites
- GitHub account
- Git installed locally
- Basic command line knowledge

### Step-by-Step Deployment

#### 1. Create GitHub Repository
```bash
# On GitHub, create a new repository named "thestreamic"
# Then clone it locally
git clone https://github.com/YOUR_USERNAME/thestreamic.git
cd thestreamic
```

#### 2. Copy Project Files
```bash
# Copy all files from the streamic-2026 package
cp -r /path/to/streamic-2026/* .
```

#### 3. Add Your Assets
```bash
# Add your logo and fallback image
cp /path/to/your/logo.png assets/logo.png
cp /path/to/your/fallback.jpg assets/fallback.jpg
```

#### 4. Commit and Push
```bash
git add .
git commit -m "🚀 Deploy The Streamic 2026"
git push origin main
```

#### 5. Enable GitHub Pages
1. Go to repository **Settings**
2. Navigate to **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / **/ (root)**
5. Click **Save**

#### 6. Run Initial RSS Fetch
1. Go to **Actions** tab
2. Click **Update RSS Feeds**
3. Click **Run workflow** button
4. Select **main** branch
5. Click **Run workflow**
6. Wait 2-3 minutes for completion

#### 7. Access Your Site
```
https://YOUR_USERNAME.github.io/thestreamic/
```

## Custom Domain Setup

### Add Custom Domain
1. In repository **Settings** → **Pages**
2. Enter your custom domain (e.g., `thestreamic.com`)
3. Click **Save**

### Configure DNS
Add these records to your DNS provider:

```
Type    Name    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     YOUR_USERNAME.github.io
```

### Enable HTTPS
1. Wait 24 hours for DNS propagation
2. Check **Enforce HTTPS** in Pages settings

## Monitoring Setup

### GitHub Actions Logs
- Go to **Actions** tab
- View each workflow run
- Check for errors in logs

### Metrics Dashboard
View `data/metrics.json` for:
```json
{
  "total_feeds_checked": 21,
  "successful_fetches": 20,
  "failed_fetches": 1,
  "total_items_fetched": 847,
  "duplicates_removed": 152,
  "items_after_dedup": 695,
  "execution_time_seconds": 45.2,
  "last_run": "2026-02-06T12:00:00Z"
}
```

### Set Up Alerts (Optional)
Create `.github/workflows/alert.yml`:
```yaml
name: Alert on Failure

on:
  workflow_run:
    workflows: ["Update RSS Feeds"]
    types:
      - completed

jobs:
  alert:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - name: Send notification
        run: echo "RSS update failed! Check logs."
        # Add your notification service here
```

## Customization Guide

### Change Update Frequency
Edit `.github/workflows/update.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 */3 * * *'  # Every 3 hours
  # - cron: '0 6 * * *'    # Daily at 6 AM
```

### Add New RSS Sources
Edit `scripts/fetch_rss.py`:
```python
RSS_FEEDS = {
    "newsroom": [
        {"url": "https://example.com/feed.xml", "label": "Example"},
        # Add more sources here
    ]
}
```

### Modify Card Layout
Edit `style.css`:
```css
.card-grid {
  grid-template-columns: repeat(5, 1fr);  /* 5 cards per row */
}

/* Change to 4 cards per row: */
.card-grid {
  grid-template-columns: repeat(4, 1fr);
}
```

### Update Contact Email
Replace `itabmum@gmail.com` in:
- `contact.html`
- `about.html`
- `privacy.html`
- `terms.html`
- `disclaimer.html`

## Troubleshooting

### RSS Feeds Not Updating
```bash
# Check GitHub Actions logs
# Verify RSS feed URLs are accessible
curl -I https://www.tvtechnology.com/rss.xml

# Test script locally
python scripts/fetch_rss.py
```

### Images Not Loading
```bash
# Verify assets exist
ls -la assets/

# Check file permissions
chmod 644 assets/*

# Test fallback image
curl -I https://YOUR_USERNAME.github.io/thestreamic/assets/fallback.jpg
```

### Categories Not Appearing
```bash
# Verify JSON files exist
ls -la data/

# Check for JavaScript errors in browser console
# Verify category names match in JS and HTML files
```

### Performance Issues
```bash
# Optimize images
# Install imagemagick if needed
brew install imagemagick  # macOS
sudo apt install imagemagick  # Linux

# Compress images
mogrify -resize 1200x675 -quality 85 assets/*.jpg
mogrify -resize 1200x675 -quality 85 assets/*.png
```

## Maintenance

### Weekly Tasks
- [ ] Check GitHub Actions logs for errors
- [ ] Review `data/metrics.json` for anomalies
- [ ] Verify all RSS sources are accessible

### Monthly Tasks
- [ ] Update RSS source list
- [ ] Review and update Impact Brief templates
- [ ] Check for broken external links
- [ ] Optimize image sizes

### Quarterly Tasks
- [ ] Review analytics (if added)
- [ ] Update legal pages
- [ ] Audit security dependencies
- [ ] Performance audit with Lighthouse

## Support

### Common Issues
1. **401/403 Errors**: Some RSS feeds block GitHub IPs. Contact the publisher.
2. **XML Parse Errors**: RSS feed may have invalid XML. Report to publisher.
3. **Slow Updates**: GitHub Actions queue can be delayed during peak times.

### Getting Help
- GitHub Issues: Create an issue in your repository
- Email: itabmum@gmail.com
- Documentation: See README.md

## Security

### Best Practices
- ✅ Keep GitHub Actions up to date
- ✅ Review workflow logs regularly
- ✅ Use HTTPS for all external feeds
- ✅ Validate XML before parsing
- ✅ Sanitize user input (if added)

### Dependency Updates
```bash
# Python dependencies are minimal (stdlib only)
# No package updates required

# Periodically update GitHub Actions:
# Check .github/workflows/update.yml for latest versions
```

## Performance Optimization

### Lighthouse Score Goals
- Performance: > 95
- Accessibility: 100
- Best Practices: > 95
- SEO: 100

### Optimization Checklist
- [x] Lazy loading images
- [x] Minimal CSS (< 50KB)
- [x] No external JS dependencies
- [x] Preconnect hints
- [x] Compressed assets
- [ ] Service Worker (optional)
- [ ] WebP images (optional)

## Backup & Recovery

### Backup Strategy
```bash
# GitHub already provides backups
# For local backups:
git clone --mirror https://github.com/YOUR_USERNAME/thestreamic.git

# Backup data files
cp -r data/ backup/data-$(date +%Y%m%d)/
```

### Recovery
```bash
# Restore from backup
git clone https://github.com/YOUR_USERNAME/thestreamic.git
cd thestreamic

# Re-run RSS fetch
git push origin main  # Triggers workflow
```

---

**Deployment Time**: ~5 minutes  
**Maintenance Time**: ~15 minutes/week  
**Cost**: Free (GitHub Pages)
