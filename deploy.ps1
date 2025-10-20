# Vercel Deployment Commands
# Run these commands to deploy your app to Vercel

# Step 1: Commit all changes
Write-Host "📦 Committing changes..." -ForegroundColor Cyan
git add .
git commit -m "Configure for Vercel deployment - all files ready"
git push origin master

Write-Host "`n✅ Changes pushed to GitHub!" -ForegroundColor Green
Write-Host "`n🚀 Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to: https://vercel.com/new"
Write-Host "2. Import your repository: shriram1206/AI-Agent"
Write-Host "3. Add environment variables (see DEPLOYMENT_CHECKLIST.md)"
Write-Host "4. Click Deploy!"
Write-Host "`n📖 Full guide: See VERCEL_READY.md" -ForegroundColor Cyan

# Optional: If you have Vercel CLI installed
$hasVercelCLI = Get-Command vercel -ErrorAction SilentlyContinue
if ($hasVercelCLI) {
    Write-Host "`n💡 You have Vercel CLI installed!" -ForegroundColor Green
    $response = Read-Host "`nDeploy now using CLI? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "`n🚀 Deploying to Vercel..." -ForegroundColor Cyan
        vercel --prod
    }
} else {
    Write-Host "`n💡 Tip: Install Vercel CLI for faster deployments:" -ForegroundColor Yellow
    Write-Host "npm install -g vercel"
}
