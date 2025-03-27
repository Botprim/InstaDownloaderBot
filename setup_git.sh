#!/bin/bash

# GitHub Repository Details
GITHUB_USER="Botprim"  # 👈 Apna GitHub Username Yaha Dalna
REPO_NAME="InstaDownloaderBot"  # 👈 Apne Repository Ka Naam Dalna
GIT_REMOTE="https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Check if Git is Installed
if ! [ -x "$(command -v git)" ]; then
  echo "❌ Error: Git is not installed." >&2
  exit 1
fi

# Initialize Git & Push Code
echo "🚀 Initializing Git Repository..."
git init
git add .
git commit -m "Initial commit"

# Setup Main Branch
git branch -M main

# Add Remote & Push Code
echo "🔗 Connecting to GitHub..."
git remote add origin "$GIT_REMOTE"
git push -u origin main

echo "✅ GitHub Repo Setup Complete! Check your repository at: https://github.com/$GITHUB_USER/$REPO_NAME"
