# Pre-Deployment Checklist

## 📋 Before You Deploy

### Assets
- [ ] Add `assets/logo.png` (48px height)
- [ ] Add `assets/fallback.jpg` (1200x675px, <100KB)
- [ ] Optimize images for web
- [ ] Test assets on mobile devices

### Configuration
- [ ] Update email in all HTML files (replace itabmum@gmail.com)
- [ ] Customize colors in `style.css` (optional)
- [ ] Review RSS sources in `scripts/fetch_rss.py`
- [ ] Set desired update frequency in `.github/workflows/update.yml`

### Content
- [ ] Review About page content
- [ ] Customize hero text
- [ ] Update footer copyright year
- [ ] Review legal pages

### GitHub Setup
- [ ] Create GitHub repository
- [ ] Enable GitHub Pages
- [ ] Set up custom domain (optional)
- [ ] Configure branch protection (optional)

## 🚀 After Deployment

### Initial Testing
- [ ] Run RSS workflow manually
- [ ] Verify all JSON files created
- [ ] Check homepage loads correctly
- [ ] Test all category pages
- [ ] Verify mobile responsiveness

### Performance
- [ ] Run Lighthouse audit
- [ ] Check page load times
- [ ] Test on slow connections
- [ ] Verify lazy loading works

### Monitoring
- [ ] Check monitoring dashboard
- [ ] Review feed health metrics
- [ ] Set up alerts (optional)
- [ ] Bookmark GitHub Actions page

### SEO
- [ ] Submit sitemap to Google
- [ ] Verify in Google Search Console
- [ ] Check robots.txt
- [ ] Test structured data

## 🔄 Ongoing Maintenance

### Daily
- [ ] Check for GitHub Actions errors

### Weekly
- [ ] Review monitoring metrics
- [ ] Check for broken RSS feeds
- [ ] Verify content quality

### Monthly
- [ ] Update RSS sources
- [ ] Review analytics
- [ ] Optimize images
- [ ] Update dependencies

### Quarterly
- [ ] Performance audit
- [ ] Security review
- [ ] Content strategy review
- [ ] Update documentation

---

**Deployment Time**: ~5 minutes  
**Setup Time**: ~15 minutes  
**Weekly Maintenance**: ~15 minutes
