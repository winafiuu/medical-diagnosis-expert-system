# Deployment Guide for Render

This guide will walk you through deploying the Medical Diagnosis Expert System to Render.

## Prerequisites

1. A [Render](https://render.com) account (free tier works)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Step 1: Push Your Code to Git

Make sure all files are committed and pushed:

```bash
git add .
git commit -m "Add deployment configuration for Render"
git push origin main
```

### Step 2: Create a New Blueprint in Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click the **"New +"** button in the top right
3. Select **"Blueprint"**
4. Connect your Git repository
5. Render will automatically detect the `render.yaml` file

### Step 3: Configure the Blueprint

Render will show you two services to be created:

- **medical-diagnosis-api** (Backend + AI Engine)
- **medical-diagnosis-web** (Frontend)

### Step 4: Set Environment Variable for Frontend

Once the services are created:

1. Go to the **medical-diagnosis-web** service in your Render dashboard
2. Navigate to **Environment** in the left sidebar
3. Add the following environment variable:

   - **Key:** `VITE_API_URL`
   - **Value:** `https://medical-diagnosis-api.onrender.com` (replace with your actual backend URL)

   > **Note:** The backend URL will be shown in the **medical-diagnosis-api** service dashboard once it's deployed.

4. Click **"Save Changes"**

### Step 5: Trigger a Redeploy

After setting the environment variable:

1. Go to the **medical-diagnosis-web** service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Step 6: Access Your Application

Once both services are deployed (this takes about 5-10 minutes):

1. Frontend will be available at: `https://medical-diagnosis-web.onrender.com` (or your custom URL)
2. Backend API will be available at: `https://medical-diagnosis-api.onrender.com`

## Troubleshooting

### Backend Build Fails

- Check the build logs in the Render dashboard
- Ensure `requirements.txt` and `package.json` are correct
- Verify the Dockerfile syntax

### Frontend Can't Connect to Backend

- Verify `VITE_API_URL` is set correctly in the frontend environment variables
- Ensure the backend URL includes `https://` and does NOT include `/api` (this is added automatically in the code)
- Check CORS settings in the backend

### Python Dependencies Not Installing

- The Dockerfile uses `--break-system-packages` flag which is required for newer Python versions in Docker
- If this causes issues, you can switch to using a virtual environment in the Dockerfile

## Free Tier Limitations

Render's free tier has these limitations:

- Services spin down after 15 minutes of inactivity
- First request after spin-down will be slow (~30 seconds)
- 750 hours of runtime per month (shared across all services)

For production use, consider upgrading to a paid plan.

## Custom Domain

To add a custom domain:

1. Go to your service in the Render dashboard
2. Click **"Settings"** → **"Custom Domain"**
3. Follow the instructions to add your domain
4. Update the `VITE_API_URL` in the frontend to use your custom backend domain

## Updating Your App

To deploy updates:

1. Push changes to your Git repository
2. Render will automatically detect and deploy the changes
3. You can also trigger manual deploys from the dashboard

---

**Need help?** Check out [Render's Documentation](https://render.com/docs)
