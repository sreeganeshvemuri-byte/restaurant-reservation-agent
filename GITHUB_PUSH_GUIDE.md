# 🚀 How to Push Your Project to GitHub

## Your Repository is Ready Locally! ✅

I've already initialized git and committed all your files. Now you just need to push to GitHub.

---

## Step-by-Step Guide

### Step 1: Create GitHub Repository (2 minutes)

1. **Go to GitHub**: https://github.com/new

2. **Fill in the details**:
   - **Repository name**: `restaurant-reservation-agent` (or your choice)
   - **Description**: "AI Restaurant Reservation Agent for Sarvam AI Challenge"
   - **Visibility**: ⚠️ **Private** (IMPORTANT!)
   - **Do NOT check**: "Add a README file" (we already have one)
   - **Do NOT add**: .gitignore or license (we have them)

3. **Click**: "Create repository"

4. **Copy the repository URL** shown on the next page (looks like):
   ```
   https://github.com/YOUR_USERNAME/restaurant-reservation-agent.git
   ```

---

### Step 2: Push Your Code (1 minute)

Open your terminal and run these commands:

```bash
# Navigate to project
cd /home/user/restaurant-reservation-agent

# Add your GitHub repository as remote (replace with YOUR URL)
git remote add origin https://github.com/YOUR_USERNAME/restaurant-reservation-agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**When prompted for credentials**:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (NOT your GitHub password)

---

### Step 3: Get GitHub Personal Access Token (if needed)

If you don't have a token:

1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token" → "Generate new token (classic)"
3. **Note**: "Sarvam AI Project Upload"
4. **Expiration**: 30 days (sufficient for submission)
5. **Scopes**: Check `repo` (full control of private repositories)
6. Click: "Generate token"
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when pushing

---

### Step 4: Verify Upload

After pushing, check GitHub:

1. Go to your repository URL
2. Verify all files are there:
   - ✅ README.md
   - ✅ app.py
   - ✅ agent/gemini_agent.py
   - ✅ data/restaurants.py
   - ✅ docs/ folder
   - ✅ All other files

3. **Important**: Make sure `.env` is NOT there (it should be ignored)

---

### Step 5: Add Sarvam AI Collaborators

1. In your GitHub repo, go to: **Settings** → **Collaborators**
2. Click: "Add people"
3. Add these three emails:
   - `kartik@sarvam.ai`
   - `ashish@sarvam.ai`
   - `aman@sarvam.ai`
4. Give them **Read** access
5. Click "Add [name] to this repository"

---

## Quick Command Summary

```bash
# All commands in one place:
cd /home/user/restaurant-reservation-agent

# Add remote (REPLACE WITH YOUR URL!)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "Authentication failed"
→ Use a Personal Access Token instead of password
→ Generate one at: https://github.com/settings/tokens

### "Remote origin already exists"
→ Remove it first: `git remote remove origin`
→ Then add again with correct URL

### "Permission denied"
→ Make sure you're logged into the correct GitHub account
→ Check the repository URL is correct
→ Verify the token has `repo` scope

### "Large files detected"
→ Shouldn't happen with this project
→ If it does, remove .env: `git rm --cached .env`

---

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
cd /home/user/restaurant-reservation-agent

# Login
gh auth login

# Create private repo and push
gh repo create restaurant-reservation-agent --private --source=. --push

# Add collaborators
gh api repos/YOUR_USERNAME/restaurant-reservation-agent/collaborators/kartik@sarvam.ai -X PUT
```

---

## What Happens After Push?

1. ✅ All your code is on GitHub
2. ✅ It's private (only you and collaborators can see)
3. ✅ Ready to share with Sarvam AI
4. ✅ You can continue to make changes and push updates

---

## Next Steps After GitHub Upload

1. ✅ Verify all files are uploaded
2. ✅ Add Sarvam AI collaborators
3. 🎥 Record your demo video
4. 📧 Send submission email with GitHub link

---

## Your Repository URL Format

After creation, your repository will be at:
```
https://github.com/YOUR_USERNAME/restaurant-reservation-agent
```

Share this URL in your submission email!

---

## Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify you created a **private** repository
3. Make sure you're using a Personal Access Token
4. Double-check the repository URL is correct

---

**You're almost done! Just push to GitHub and you're ready to submit! 🚀**
