@echo off
echo ========================================
echo   AI Sales Video Generator - GitHub Push
echo ========================================
echo.

echo Step 1: Create GitHub Repository
echo --------------------------------
echo 1. Go to: https://github.com/new
echo 2. Repository name: ai-sales-video-generator
echo 3. Description: AI-powered sales video generator using OpenAI and Hedra AI
echo 4. Make it Public (recommended)
echo 5. DO NOT add README, .gitignore, or license
echo 6. Click "Create repository"
echo.

echo Step 2: Copy your repository URL
echo --------------------------------
echo After creating, copy the URL that looks like:
echo https://github.com/YOUR_USERNAME/ai-sales-video-generator.git
echo.

pause
echo.

set /p REPO_URL="Paste your repository URL here: "

echo.
echo Step 3: Pushing to GitHub...
echo --------------------------------

git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   SUCCESS! Your project is on GitHub!
echo ========================================
echo.
echo Your repository includes:
echo - Complete AI Sales Video Generator app
echo - 39 files with 5000+ lines of code
echo - Professional documentation
echo - Working OpenAI integration
echo - Hedra AI video generation system
echo.
echo Share your repository URL to showcase your work!
echo.
pause
