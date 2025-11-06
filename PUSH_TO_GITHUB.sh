#!/bin/bash

echo "============================================"
echo "   Push to GitHub - Interactive Script"
echo "============================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Not in the correct directory"
    echo "Please run: cd /home/user/restaurant-reservation-agent"
    exit 1
fi

echo "✅ Repository initialized locally"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " username

# Get repository name
read -p "Enter repository name (default: restaurant-reservation-agent): " repo_name
repo_name=${repo_name:-restaurant-reservation-agent}

# Construct URL
repo_url="https://github.com/$username/$repo_name.git"

echo ""
echo "📋 Repository URL: $repo_url"
echo ""
read -p "Is this correct? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled. Please run the script again."
    exit 1
fi

echo ""
echo "🚀 Adding remote and pushing..."
echo ""

# Remove existing remote if any
git remote remove origin 2>/dev/null

# Add remote
git remote add origin "$repo_url"

# Push
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📌 Your repository: https://github.com/$username/$repo_name"
    echo ""
    echo "Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Settings → Collaborators → Add people"
    echo "3. Add: kartik@sarvam.ai, ashish@sarvam.ai, aman@sarvam.ai"
    echo "4. Record your demo video"
    echo "5. Submit to Sarvam AI!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "1. Repository doesn't exist on GitHub - create it first at https://github.com/new"
    echo "2. Authentication failed - use a Personal Access Token (not password)"
    echo "3. No permission - check you're logged into the correct account"
    echo ""
    echo "See GITHUB_PUSH_GUIDE.md for detailed instructions"
fi
