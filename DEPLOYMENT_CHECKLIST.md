# 🚀 Quick Deployment Checklist

## ✅ Pre-Deployment (Local)

- [x] Fixed `api/index.py` - WSGI entry point
- [x] Unified all `requirements*.txt` files
- [x] Updated `vercel.json` configuration
- [x] Created `.vercelignore` file
- [x] Verified no code errors
- [ ] **Commit changes to Git**
  ```powershell
  git add .
  git commit -m "Ready for Vercel deployment"
  git push origin master
  ```

## 🔧 Vercel Setup

- [ ] Go to https://vercel.com/new
- [ ] Import your GitHub repository: `shriram1206/AI-Agent`
- [ ] Configure project:
  - Framework: **Other**
  - Root Directory: **./** (default)
  - Build/Output: **leave empty**

## 🔐 Environment Variables

Add these in Vercel Dashboard:

```env
Name: PERPLEXITY_API_KEY
Value: pplx-your-api-key-here
Environments: ✓ Production ✓ Preview ✓ Development

Name: SECRET_KEY  
Value: your-random-32-character-secret-key
Environments: ✓ Production ✓ Preview ✓ Development

Name: DATABASE_URL
Value: sqlite:///thomas.db
Environments: ✓ Production ✓ Preview ✓ Development
```

**Get API Key:** https://www.perplexity.ai/settings/api

## 🚀 Deploy

- [ ] Click **"Deploy"** button
- [ ] Wait 30-60 seconds
- [ ] Check build logs for any errors
- [ ] Note your deployment URL: `https://your-project.vercel.app`

## 🧪 Testing (After Deployment)

Visit your Vercel URL and test:

- [ ] Homepage loads without errors
- [ ] Create new account (Signup)
- [ ] Login with credentials
- [ ] Send test message: "Hello Thomas, tell me about Python"
- [ ] Verify response is formatted (markdown, bold, bullets)
- [ ] Click "News" button - check news loads
- [ ] Create new conversation
- [ ] Switch between conversations
- [ ] Logout and login again
- [ ] Test on mobile device

## ⚠️ Known Issues & Solutions

### If you get database errors:
- SQLite doesn't persist on Vercel (serverless)
- **Solution:** Use Vercel Postgres, Supabase, or PlanetScale
- See `VERCEL_READY.md` for detailed database setup

### If static files don't load:
- Clear browser cache
- Check Vercel build logs
- Verify `vercel.json` routes

### If API key errors:
- Double-check `PERPLEXITY_API_KEY` in Vercel environment variables
- Verify key is valid at https://www.perplexity.ai/settings/api
- Redeploy after adding variables

## 🎯 Post-Deployment

- [ ] Monitor first 24 hours for any issues
- [ ] Check Vercel Analytics for traffic
- [ ] Review Function Logs for errors
- [ ] Consider setting up external database for production
- [ ] (Optional) Add custom domain

## 📊 Performance Expectations

- ⚡ Deploy time: 30-60 seconds
- 🌍 Page load: < 2 seconds
- 💬 Message response: 5-10 seconds
- 🔄 No cold starts (Vercel advantage)

## 🆘 Need Help?

- Full guide: See `VERCEL_READY.md`
- Vercel docs: https://vercel.com/docs
- Check logs: Vercel Dashboard → Deployments → View Logs

---

**Status:** ✅ All files configured and ready for deployment!

**Next step:** Commit changes and deploy on Vercel!
