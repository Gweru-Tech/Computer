# 🚀 Deploy NtandoComputer on Render.com

This guide will help you deploy NtandoComputer on Render.com for production use.

## 📋 Prerequisites

- A Render.com account (Free tier available)
- Git repository with NtandoComputer code
- Basic understanding of web services

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Push to GitHub

1. Fork or create a new repository on GitHub
2. Push your NtandoComputer code to the repository

```bash
git init
git add .
git commit -m "Initial commit - NtandoComputer"
git branch -M main
git remote add origin https://github.com/yourusername/ntandocomputer.git
git push -u origin main
```

### Step 2: Create Render Service

1. Log in to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Service Configuration:**
- **Name**: `ntandocomputer`
- **Environment**: `Python 3`
- **Branch**: `main`
- **Root Directory**: `ntandocomputer`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT computer:app`

**Advanced Settings:**
- **Health Check Path**: `/api/system/info`
- **Auto-Deploy**: Enabled

### Step 3: Configure Environment

Add these environment variables:
- `FLASK_ENV=production`
- `PYTHON_VERSION=3.11.0`

### Step 4: Deploy

Click "Create Web Service" and Render will automatically deploy your application!

## 🔧 Configuration Options

### Using render.yaml (Recommended)

Create a `render.yaml` file in your repository root for automatic configuration:

```yaml
services:
  - type: web
    name: ntandocomputer
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT computer:app
    healthCheck:
      path: /api/system/info
    envVars:
      - key: FLASK_ENV
        value: production
    disk:
      name: ntandocomputer-storage
      mountPath: /workspace/ntandocomputer/storage
      sizeGB: 1
```

### Custom Domain

1. Go to your service settings on Render
2. Click "Custom Domains"
3. Add your domain (e.g., `yourcomputer.yourdomain.com`)
4. Configure DNS as instructed by Render

## 📊 Features Available on Render

### ✅ Production Features
- **HTTPS**: Automatic SSL certificates
- **Auto-scaling**: Available on paid plans
- **Custom domains**: Supported on all plans
- **Environment variables**: Secure configuration
- **Persistent storage**: For uploaded files and apps
- **Health checks**: Automatic monitoring
- **Logs**: Built-in log management

### 🌟 Enhanced Capabilities
- **Global CDN**: Fast content delivery
- **Auto-deploys**: Zero-downtime deployments
- **Preview environments**: Test changes before production
- **Collaboration**: Team access controls

## 🛠️ Post-Deployment Setup

### 1. Verify Deployment

Once deployed, your NtandoComputer will be available at:
`https://ntandocomputer.onrender.com`

Check the health endpoint:
`https://ntandocomputer.onrender.com/api/system/info`

### 2. Configure Storage

Render provides persistent storage for:
- **Deployed applications** (`/workspace/ntandocomputer/apps`)
- **User files** (`/workspace/ntandocomputer/storage`)
- **System logs** (`/workspace/ntandocomputer/logs`)
- **Configuration** (`/workspace/ntandocomputer/config`)

### 3. Set Up Monitoring

Render provides built-in monitoring:
- **Response time**: Track performance
- **Error rates**: Monitor issues
- **Resource usage**: CPU and memory
- **Uptime**: Service availability

## 🔒 Security Considerations

### Production Security
- **HTTPS**: Enabled by default
- **Environment variables**: Secure secret management
- **Network isolation**: Container-based security
- **Regular updates**: Keep dependencies current

### Recommended Security Practices
1. **Regular backups**: Export important data
2. **Access controls**: Limit admin access
3. **Monitor logs**: Watch for suspicious activity
4. **Update dependencies**: Security patches

## 📈 Scaling Options

### Free Plan (Default)
- **RAM**: 512 MB
- **CPU**: Shared
- **Bandwidth**: 100 GB/month
- **Storage**: 1 GB persistent disk

### Paid Plans
- **Starter**: $7/month
  - RAM: 1 GB
  - CPU: 1 vCPU
  - More bandwidth and storage

- **Standard**: $25/month
  - RAM: 2 GB
  - CPU: 2 vCPU
  - Better performance

- **Pro**: $100/month
  - RAM: 8 GB
  - CPU: 4 vCPU
  - Auto-scaling included

## 🐛 Troubleshooting

### Common Issues

**Build Fails**
```bash
# Check requirements.txt
pip install -r requirements.txt --dry-run
```

**Service Won't Start**
```bash
# Test locally
gunicorn --bind 0.0.0.0:5000 computer:app
```

**Health Check Failing**
- Verify `/api/system/info` is accessible
- Check Flask app is properly configured
- Review Render logs for errors

**Storage Issues**
- Check disk space in Render dashboard
- Verify file permissions
- Review storage configuration

### Debug Steps

1. **Check Build Logs**: Render dashboard → Logs
2. **Verify Environment**: Check env variables
3. **Test Locally**: Match production environment
4. **Review Configuration**: Validate render.yaml
5. **Contact Support**: Render's excellent support team

## 🔄 Continuous Deployment

### Auto-Deploy Setup
1. Enable auto-deploy in service settings
2. Push to main branch → Auto-deployment
3. Preview branches → Test environments

### Deployment Strategies
- **Blue-Green**: Zero downtime deployments
- **Canary**: Gradual rollout
- **Feature flags**: Controlled releases

## 📚 Additional Resources

### Documentation
- [Render Python Docs](https://render.com/docs/deploy-python-flask)
- [Render Configuration](https://render.com/docs/render-yaml)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

### Community
- [Render Discord](https://discord.gg/render)
- [GitHub Discussions](https://github.com/render-inc/render/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/render)

### Advanced Features
- **Background workers**: For long-running tasks
- **Cron jobs**: Scheduled tasks
- **PostgreSQL**: Managed database
- **Redis**: Caching and session storage

## 🎯 Production Checklist

Before going live with your NtandoComputer:

- [ ] Deploy to staging environment
- [ ] Test all features (deploy, apps, files, terminal)
- [ ] Verify health checks
- [ ] Set up custom domain
- [ ] Configure monitoring alerts
- [ ] Test backup procedures
- [ ] Review security settings
- [ ] Document maintenance procedures

## 🎉 Success!

Once deployed, your NtandoComputer will provide:
- **Web-based computer interface**
- **HTML and Node.js application deployment**
- **File management system**
- **Terminal access**
- **Application monitoring**
- **Persistent storage**

Users can access it anywhere in the world with a simple web browser!

---

**Need help?** Check out the [Render documentation](https://render.com/docs) or contact their support team.