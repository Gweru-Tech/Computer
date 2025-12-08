#!/usr/bin/env python3
"""
NtandoComputer Enhanced - Cloud Computer System
A web-based computer interface with HTML and Node.js deployment capabilities
Features: .ntando.store domains, eternal persistence, advanced features
"""

import os
import json
import subprocess
import shutil
import uuid
import time
import hashlib
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from werkzeug.utils import secure_filename
import threading
import zipfile
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional
import sqlite3
import schedule

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['SECRET_KEY'] = 'ntando-computer-enhanced-secret-key-2024'

# Database for eternal persistence
def init_database():
    conn = sqlite3.connect('ntando_computer.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            subscription_plan TEXT DEFAULT 'free',
            storage_used INTEGER DEFAULT 0,
            storage_limit INTEGER DEFAULT 1073741824
        )
    ''')
    
    # Applications table for eternal persistence
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            domain TEXT UNIQUE NOT NULL,
            path TEXT NOT NULL,
            url TEXT NOT NULL,
            deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'running',
            port INTEGER,
            command TEXT,
            description TEXT,
            public BOOLEAN DEFAULT TRUE,
            visits INTEGER DEFAULT 0,
            last_accessed TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Files table for eternal persistence
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            size INTEGER NOT NULL,
            type TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hash TEXT NOT NULL,
            public BOOLEAN DEFAULT FALSE,
            downloads INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id TEXT,
            event_type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            metadata TEXT,
            FOREIGN KEY (app_id) REFERENCES applications (id)
        )
    ''')
    
    # Backups table for eternal persistence
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backups (
            id TEXT PRIMARY KEY,
            app_id TEXT,
            backup_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            size INTEGER NOT NULL,
            FOREIGN KEY (app_id) REFERENCES applications (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@dataclass
class User:
    id: int
    username: str
    email: str
    api_key: str
    subscription_plan: str = 'free'
    storage_used: int = 0
    storage_limit: int = 1073741824  # 1GB default

@dataclass
class Application:
    id: str
    user_id: int
    name: str
    type: str
    domain: str
    path: str
    url: str
    deployed_at: datetime
    status: str = 'running'
    port: int = None
    command: str = None
    description: str = None
    public: bool = True
    visits: int = 0

class NtandoComputer:
    def __init__(self):
        self.apps_dir = "apps"
        self.logs_dir = "logs"
        self.storage_dir = "storage"
        self.deploy_dir = "deploy"
        self.backups_dir = "backups"
        self.config_file = "config/computer_config.json"
        self.db_file = "ntando_computer.db"
        
        # Enhanced features
        self.base_domain = ".ntando.store"
        self.eternal_storage = True
        self.backup_enabled = True
        self.analytics_enabled = True
        
        self.ensure_directories()
        self.init_database()
        self.load_config()
        self.start_background_tasks()
    
    def ensure_directories(self):
        """Create necessary directories"""
        for directory in [self.apps_dir, self.logs_dir, self.storage_dir, self.deploy_dir, self.backups_dir, "ui/templates", "ui/static", "temp"]:
            os.makedirs(directory, exist_ok=True)
    
    def init_database(self):
        """Initialize SQLite database for eternal persistence"""
        try:
            init_database()
            print("✅ Database initialized for eternal persistence")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
    
    def load_config(self):
        """Load computer configuration"""
        default_config = {
            "computer_name": "NtandoComputer Enhanced",
            "version": "2.0.0",
            "deployed_apps": {},
            "system_stats": {
                "total_apps": 0,
                "html_apps": 0,
                "nodejs_apps": 0,
                "eternal_apps": 0,
                "uptime": time.time(),
                "total_users": 0,
                "active_users": 0
            },
            "features": {
                "eternal_persistence": True,
                "custom_domains": True,
                "analytics": True,
                "backups": True,
                "marketplace": True,
                "collaboration": True
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
    
    def save_config(self):
        """Save computer configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def start_background_tasks(self):
        """Start background tasks for enhanced features"""
        def backup_task():
            """Create automatic backups for eternal persistence"""
            while True:
                try:
                    self.create_automated_backups()
                    time.sleep(3600)  # Backup every hour
                except Exception as e:
                    print(f"Backup error: {e}")
                    time.sleep(300)  # Retry in 5 minutes
        
        def analytics_task():
            """Process analytics data"""
            while True:
                try:
                    self.process_analytics()
                    time.sleep(300)  # Process every 5 minutes
                except Exception as e:
                    print(f"Analytics error: {e}")
                    time.sleep(60)
        
        # Start background threads
        backup_thread = threading.Thread(target=backup_task, daemon=True)
        analytics_thread = threading.Thread(target=analytics_task, daemon=True)
        
        backup_thread.start()
        analytics_thread.start()
        
        print("🔄 Background tasks started for eternal persistence")
    
    def generate_domain(self, app_name, app_type):
        """Generate unique .ntando.store domain"""
        base_name = app_name.lower().replace(' ', '-').replace('_', '-')
        clean_name = ''.join(c for c in base_name if c.isalnum() or c == '-')
        
        # Ensure unique domain
        counter = 1
        domain = f"{clean_name}{self.base_domain}"
        
        while self.domain_exists(domain):
            domain = f"{clean_name}-{counter}{self.base_domain}"
            counter += 1
        
        return domain
    
    def domain_exists(self, domain):
        """Check if domain already exists"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM applications WHERE domain = ?", (domain,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def save_application_to_db(self, app_info):
        """Save application to database for eternal persistence"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO applications 
            (id, user_id, name, type, domain, path, url, deployed_at, updated_at, status, port, command, description, public, visits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            app_info['id'], 
            app_info.get('user_id', 1),  # Default user
            app_info['name'],
            app_info['type'],
            app_info['domain'],
            app_info['path'],
            app_info['url'],
            app_info['deployed_at'],
            datetime.now().isoformat(),
            app_info['status'],
            app_info.get('port'),
            app_info.get('command'),
            app_info.get('description', ''),
            app_info.get('public', True),
            0
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Application {app_info['name']} saved to eternal database")
    
    def create_automated_backups(self):
        """Create automatic backups for eternal persistence"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, path FROM applications WHERE status = 'running'")
        apps = cursor.fetchall()
        
        for app_id, name, path in apps:
            if os.path.exists(path):
                backup_id = str(uuid.uuid4())[:8]
                backup_path = os.path.join(self.backups_dir, backup_id)
                
                try:
                    shutil.make_archive(backup_path, 'zip', path)
                    
                    cursor.execute('''
                        INSERT INTO backups (id, app_id, backup_path, created_at, size)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (backup_id, app_id, backup_path + '.zip', datetime.now().isoformat(), 
                          os.path.getsize(backup_path + '.zip')))
                    
                    print(f"📦 Backup created for {name}")
                except Exception as e:
                    print(f"❌ Backup failed for {name}: {e}")
        
        conn.commit()
        conn.close()
    
    def process_analytics(self):
        """Process analytics data for insights"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Update visit counts and last accessed times
        cursor.execute('''
            UPDATE applications 
            SET last_accessed = (
                SELECT MAX(timestamp) FROM analytics 
                WHERE analytics.app_id = applications.id AND event_type = 'visit'
            )
            WHERE id IN (
                SELECT DISTINCT app_id FROM analytics WHERE event_type = 'visit'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_analytics(self, app_id, event_type, metadata=None):
        """Track analytics events"""
        if not self.analytics_enabled:
            return
            
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics (app_id, event_type, ip_address, user_agent, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            app_id, 
            event_type,
            request.remote_addr if request else None,
            request.headers.get('User-Agent') if request else None,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_domain_suggestions(self, domain):
        """Get alternative domain suggestions"""
        base_name = domain.replace(self.base_domain, '')
        suggestions = []
        
        for suffix in ['app', 'web', 'site', 'online', 'demo', 'pro']:
            suggestion = f"{base_name}-{suffix}{self.base_domain}"
            if not self.domain_exists(suggestion):
                suggestions.append(suggestion)
            if len(suggestions) >= 3:
                break
        
        return suggestions
    
    def deploy_html_app(self, app_name, files, description="", public=True):
        """Deploy an HTML application with eternal persistence"""
        app_id = str(uuid.uuid4())[:8]
        domain = self.generate_domain(app_name, "html")
        app_path = os.path.join(self.apps_dir, app_id)
        
        os.makedirs(app_path, exist_ok=True)
        
        # Extract files
        if zipfile.is_zipfile(files):
            with zipfile.ZipFile(files, 'r') as zip_ref:
                zip_ref.extractall(app_path)
        else:
            # Handle single file upload
            filename = secure_filename(files.filename)
            files.save(os.path.join(app_path, filename))
        
        # Create eternal app info
        app_info = {
            "id": app_id,
            "name": app_name,
            "type": "html",
            "domain": domain,
            "path": app_path,
            "url": f"/app/{app_id}",
            "full_url": f"https://{domain}",
            "deployed_at": datetime.now().isoformat(),
            "status": "running",
            "port": 8083 + len(self.config["deployed_apps"]),
            "description": description,
            "public": public,
            "eternal": True,
            "visits": 0,
            "backup_enabled": True,
            "analytics_enabled": True
        }
        
        # Save to eternal database
        self.save_application_to_db(app_info)
        
        # Update config
        self.config["deployed_apps"][app_id] = app_info
        self.config["system_stats"]["html_apps"] += 1
        self.config["system_stats"]["total_apps"] += 1
        self.config["system_stats"]["eternal_apps"] += 1
        self.save_config()
        
        # Track deployment analytics
        self.track_analytics(app_id, "deploy", {"type": "html", "name": app_name})
        
        # Create initial backup
        self.create_app_backup(app_id)
        
        print(f"🚀 HTML App '{app_name}' deployed eternally at {domain}")
        return app_info
    
    def deploy_nodejs_app(self, app_name, files, package_json=None, description="", public=True, start_command="node server.js"):
        """Deploy a Node.js application with eternal persistence"""
        app_id = str(uuid.uuid4())[:8]
        domain = self.generate_domain(app_name, "nodejs")
        app_path = os.path.join(self.apps_dir, app_id)
        
        os.makedirs(app_path, exist_ok=True)
        
        # Extract files
        if zipfile.is_zipfile(files):
            with zipfile.ZipFile(files, 'r') as zip_ref:
                zip_ref.extractall(app_path)
        
        # Handle package.json if provided
        if package_json:
            with open(os.path.join(app_path, "package.json"), 'w') as f:
                f.write(package_json)
        
        # Install dependencies
        try:
            result = subprocess.run(['npm', 'install'], cwd=app_path, check=True, capture_output=True, text=True)
            print(f"📦 Dependencies installed: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ npm install failed: {e.stderr}")
            # Create basic package.json if needed
            if not package_json:
                basic_package = {
                    "name": app_name.lower().replace(' ', '-'),
                    "version": "1.0.0",
                    "scripts": {"start": start_command},
                    "engines": {"node": ">=16.0.0"}
                }
                with open(os.path.join(app_path, "package.json"), 'w') as f:
                    json.dump(basic_package, f, indent=2)
        
        # Create eternal app info
        app_info = {
            "id": app_id,
            "name": app_name,
            "type": "nodejs",
            "domain": domain,
            "path": app_path,
            "url": f"/app/{app_id}",
            "full_url": f"https://{domain}",
            "deployed_at": datetime.now().isoformat(),
            "status": "running",
            "port": 9000 + len(self.config["deployed_apps"]),
            "command": start_command,
            "description": description,
            "public": public,
            "eternal": True,
            "visits": 0,
            "backup_enabled": True,
            "analytics_enabled": True,
            "node_version": "18.17.0",
            "environment": "production"
        }
        
        # Save to eternal database
        self.save_application_to_db(app_info)
        
        # Update config
        self.config["deployed_apps"][app_id] = app_info
        self.config["system_stats"]["nodejs_apps"] += 1
        self.config["system_stats"]["total_apps"] += 1
        self.config["system_stats"]["eternal_apps"] += 1
        self.save_config()
        
        # Track deployment analytics
        self.track_analytics(app_id, "deploy", {"type": "nodejs", "name": app_name})
        
        # Create initial backup
        self.create_app_backup(app_id)
        
        print(f"⚡ Node.js App '{app_name}' deployed eternally at {domain}")
        return app_info
    
    def create_app_backup(self, app_id):
        """Create backup for eternal persistence"""
        if not self.backup_enabled:
            return
            
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name, path FROM applications WHERE id = ?", (app_id,))
        app = cursor.fetchone()
        
        if app and os.path.exists(app[1]):
            backup_id = str(uuid.uuid4())[:8]
            backup_path = os.path.join(self.backups_dir, backup_id)
            
            try:
                shutil.make_archive(backup_path, 'zip', app[1])
                
                cursor.execute('''
                    INSERT INTO backups (id, app_id, backup_path, created_at, size)
                    VALUES (?, ?, ?, ?, ?)
                ''', (backup_id, app_id, backup_path + '.zip', datetime.now().isoformat(), 
                      os.path.getsize(backup_path + '.zip')))
                
                conn.commit()
                print(f"📦 Initial backup created for {app[0]}")
            except Exception as e:
                print(f"❌ Initial backup failed for {app[0]}: {e}")
        
        conn.close()
    
    def restore_from_backup(self, app_id, backup_id):
        """Restore application from backup for eternal persistence"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT backup_path FROM backups WHERE app_id = ? AND id = ?", (app_id, backup_id))
        backup = cursor.fetchone()
        
        if backup and os.path.exists(backup[0]):
            cursor.execute("SELECT path FROM applications WHERE id = ?", (app_id,))
            app_path = cursor.fetchone()
            
            if app_path:
                # Remove current app directory
                if os.path.exists(app_path[0]):
                    shutil.rmtree(app_path[0])
                
                # Extract backup
                with zipfile.ZipFile(backup[0], 'r') as zip_ref:
                    zip_ref.extractall(app_path[0])
                
                print(f"🔄 App restored from backup {backup_id}")
                return True
        
        conn.close()
        return False
    
    def get_app_info(self, app_id):
        """Get application information"""
        return self.config["deployed_apps"].get(app_id)
    
    def list_apps(self):
        """List all deployed applications"""
        return self.config["deployed_apps"]
    
    def delete_app(self, app_id):
        """Delete an application"""
        if app_id in self.config["deployed_apps"]:
            app_info = self.config["deployed_apps"][app_id]
            app_type = app_info["type"]
            
            # Remove app directory
            if os.path.exists(app_info["path"]):
                shutil.rmtree(app_info["path"])
            
            # Update config
            del self.config["deployed_apps"][app_id]
            self.config["system_stats"]["total_apps"] -= 1
            if app_type == "html":
                self.config["system_stats"]["html_apps"] -= 1
            elif app_type == "nodejs":
                self.config["system_stats"]["nodejs_apps"] -= 1
            
            self.save_config()
            return True
        return False

# Initialize computer
computer = NtandoComputer()

@app.route('/')
def desktop():
    """Main computer desktop interface"""
    return render_template('desktop.html', config=computer.config)

@app.route('/deploy')
def deploy_page():
    """Deployment interface"""
    return render_template('deploy.html', config=computer.config)

@app.route('/apps')
def apps_page():
    """Applications management"""
    apps = computer.list_apps()
    return render_template('apps.html', apps=apps, config=computer.config)

@app.route('/files')
def files_page():
    """File management interface"""
    return render_template('files.html', config=computer.config)

@app.route('/terminal')
def terminal_page():
    """Terminal interface"""
    return render_template('terminal.html', config=computer.config)

@app.route('/api/deploy/html', methods=['POST'])
def deploy_html():
    """Deploy HTML application"""
    try:
        app_name = request.form.get('app_name', f'HTML App {int(time.time())}')
        files = request.files.get('files')
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        app_info = computer.deploy_html_app(app_name, files)
        return jsonify({"success": True, "app": app_info})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deploy/nodejs', methods=['POST'])
def deploy_nodejs():
    """Deploy Node.js application"""
    try:
        app_name = request.form.get('app_name', f'Node.js App {int(time.time())}')
        files = request.files.get('files')
        package_json = request.form.get('package_json')
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        app_info = computer.deploy_nodejs_app(app_name, files, package_json)
        return jsonify({"success": True, "app": app_info})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/apps')
def list_apps_api():
    """List all applications API"""
    apps = computer.list_apps()
    return jsonify(apps)

@app.route('/api/apps/<app_id>')
def get_app_api(app_id):
    """Get app information API"""
    app_info = computer.get_app_info(app_id)
    if app_info:
        return jsonify(app_info)
    return jsonify({"error": "App not found"}), 404

@app.route('/api/apps/<app_id>', methods=['DELETE'])
def delete_app_api(app_id):
    """Delete app API"""
    if computer.delete_app(app_id):
        return jsonify({"success": True})
    return jsonify({"error": "App not found"}), 404

@app.route('/app/<app_id>')
def serve_app(app_id):
    """Serve deployed application"""
    app_info = computer.get_app_info(app_id)
    if not app_info:
        return "App not found", 404
    
    app_path = app_info["path"]
    if app_info["type"] == "html":
        # Serve HTML files
        if os.path.exists(os.path.join(app_path, "index.html")):
            return send_file(os.path.join(app_path, "index.html"))
        elif os.listdir(app_path):
            # Serve first HTML file
            for file in os.listdir(app_path):
                if file.endswith('.html'):
                    return send_file(os.path.join(app_path, file))
        return "No index.html found", 404
    
    elif app_info["type"] == "nodejs":
        # Return Node.js app info page
        return render_template('nodejs_app.html', app=app_info)
    
    return "App type not supported", 400

# Enhanced API endpoints
@app.route('/api/system/info')
def system_info():
    """Get enhanced system information"""
    conn = sqlite3.connect(computer.db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM applications")
    total_apps = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applications WHERE type = 'html'")
    html_apps = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applications WHERE type = 'nodejs'")
    nodejs_apps = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(visits) FROM applications")
    total_visits = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "computer_name": computer.config["computer_name"],
        "version": computer.config["version"],
        "stats": {
            "total_apps": total_apps,
            "html_apps": html_apps,
            "nodejs_apps": nodejs_apps,
            "eternal_apps": total_apps,  # All apps are eternal now
            "total_visits": total_visits,
            "total_users": total_users,
            "uptime": time.time() - computer.config["system_stats"]["uptime"]
        },
        "features": computer.config["features"],
        "domains": {
            "base_domain": computer.base_domain,
            "total_domains": total_apps
        },
        "storage": {
            "eternal_persistence": computer.eternal_storage,
            "backup_enabled": computer.backup_enabled,
            "analytics_enabled": computer.analytics_enabled
        }
    })

@app.route('/api/deploy/html/enhanced', methods=['POST'])
def deploy_html_enhanced():
    """Enhanced HTML deployment with eternal persistence"""
    try:
        app_name = request.form.get('app_name', f'HTML App {int(time.time())}')
        description = request.form.get('description', '')
        public = request.form.get('public', 'true').lower() == 'true'
        files = request.files.get('files')
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        app_info = computer.deploy_html_app(app_name, files, description, public)
        
        return jsonify({
            "success": True, 
            "app": app_info,
            "message": f"✅ HTML App deployed eternally at {app_info['domain']}",
            "features": {
                "eternal_persistence": True,
                "custom_domain": app_info['domain'],
                "backup_enabled": True,
                "analytics_enabled": True
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deploy/nodejs/enhanced', methods=['POST'])
def deploy_nodejs_enhanced():
    """Enhanced Node.js deployment with eternal persistence"""
    try:
        app_name = request.form.get('app_name', f'Node.js App {int(time.time())}')
        description = request.form.get('description', '')
        public = request.form.get('public', 'true').lower() == 'true'
        start_command = request.form.get('start_command', 'node server.js')
        package_json = request.form.get('package_json')
        files = request.files.get('files')
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        app_info = computer.deploy_nodejs_app(app_name, files, package_json, description, public, start_command)
        
        return jsonify({
            "success": True, 
            "app": app_info,
            "message": f"⚡ Node.js App deployed eternally at {app_info['domain']}",
            "features": {
                "eternal_persistence": True,
                "custom_domain": app_info['domain'],
                "backup_enabled": True,
                "analytics_enabled": True,
                "node_version": "18.17.0"
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/apps/<app_id>/analytics')
def app_analytics(app_id):
    """Get application analytics"""
    try:
        conn = sqlite3.connect(computer.db_file)
        cursor = conn.cursor()
        
        # Get app info
        cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        app = cursor.fetchone()
        
        if not app:
            return jsonify({"error": "App not found"}), 404
        
        # Get analytics
        cursor.execute('''
            SELECT event_type, COUNT(*) as count, MAX(timestamp) as last_event
            FROM analytics 
            WHERE app_id = ?
            GROUP BY event_type
        ''', (app_id,))
        
        analytics = cursor.fetchall()
        
        # Get daily visits (last 7 days)
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as visits
            FROM analytics 
            WHERE app_id = ? AND event_type = 'visit' 
            AND timestamp > datetime('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (app_id,))
        
        daily_visits = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "app_id": app_id,
            "app_name": app[2],
            "analytics": {
                "events": dict(analytics),
                "daily_visits": dict(daily_visits),
                "total_visits": app[12] or 0,
                "last_accessed": app[13]
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/apps/<app_id>/backups')
def app_backups(app_id):
    """Get application backups"""
    try:
        conn = sqlite3.connect(computer.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, created_at, size FROM backups 
            WHERE app_id = ?
            ORDER BY created_at DESC
        ''', (app_id,))
        
        backups = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "app_id": app_id,
            "backups": [
                {"id": backup[0], "created_at": backup[1], "size": backup[2]}
                for backup in backups
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/apps/<app_id>/restore/<backup_id>', methods=['POST'])
def restore_app(app_id, backup_id):
    """Restore application from backup"""
    try:
        if computer.restore_from_backup(app_id, backup_id):
            computer.track_analytics(app_id, "restore", {"backup_id": backup_id})
            return jsonify({
                "success": True,
                "message": "Application restored successfully from backup"
            })
        else:
            return jsonify({"error": "Backup not found or restore failed"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/domains/check', methods=['POST'])
def check_domain_availability():
    """Check if a .ntando.store domain is available"""
    try:
        domain_name = request.json.get('domain', '').lower()
        if not domain_name.endswith(computer.base_domain):
            domain_name += computer.base_domain
        
        available = not computer.domain_exists(domain_name)
        
        return jsonify({
            "domain": domain_name,
            "available": available,
            "suggestions": computer.get_domain_suggestions(domain_name) if not available else []
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates')
def get_templates():
    """Get enhanced application templates"""
    templates = {
        "html": [
            {
                "id": "landing-pro",
                "name": "Professional Landing Page",
                "description": "Modern, responsive landing page with animations",
                "features": ["Responsive Design", "Animations", "Contact Form", "SEO Optimized"],
                "preview": "📄"
            },
            {
                "id": "portfolio-creative",
                "name": "Creative Portfolio",
                "description": "Stunning portfolio for designers and developers",
                "features": ["Gallery", "Project Showcase", "Skills Section", "Contact"],
                "preview": "🎨"
            },
            {
                "id": "saas-landing",
                "name": "SaaS Landing Page",
                "description": "Perfect for software and service businesses",
                "features": ["Pricing Tables", "Features Grid", "Testimonials", "CTA"],
                "preview": "💼"
            },
            {
                "id": "ecommerce-store",
                "name": "E-commerce Storefront",
                "description": "Complete online store interface",
                "features": ["Product Grid", "Shopping Cart", "Checkout", "Payment UI"],
                "preview": "🛍️"
            }
        ],
        "nodejs": [
            {
                "id": "express-api",
                "name": "Express REST API",
                "description": "Full-featured REST API with authentication",
                "features": ["RESTful Routes", "JWT Auth", "Database Integration", "API Docs"],
                "preview": "🔌"
            },
            {
                "id": "fullstack-react",
                "name": "React + Express Full Stack",
                "description": "Complete MERN stack application",
                "features": ["React Frontend", "Express Backend", "MongoDB", "Authentication"],
                "preview": "⚛️"
            },
            {
                "id": "realtime-chat",
                "name": "Real-time Chat Application",
                "description": "WebSocket-based chat with rooms",
                "features": ["Socket.io", "Multiple Rooms", "User Authentication", "Message History"],
                "preview": "💬"
            },
            {
                "id": "blog-cms",
                "name": "Blog CMS",
                "description": "Content management system for blogs",
                "features": ["Admin Panel", "Post Management", "Comments", "SEO"],
                "preview": "📝"
            }
        ]
    }
    
    return jsonify(templates)

# Track visits for analytics
@app.before_request
def track_request():
    """Track application visits for analytics"""
    if request.endpoint and request.endpoint.startswith('app_'):
        app_id = request.view_args.get('app_id')
        if app_id:
            computer.track_analytics(app_id, "visit")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)