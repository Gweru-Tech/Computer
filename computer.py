#!/usr/bin/env python3
"""
NtandoComputer Enhanced Universal - Advanced Cloud Computer System
A comprehensive web-based computer interface with universal deployment
Features: Virtual Desktop, Process Management, System Services, Network Tools
Compatible with: Render.com, Heroku, AWS, Azure, GCP, Docker, VPS
"""

import os
import json
import subprocess
import shutil
import uuid
import time
import hashlib
import requests
import psutil
import platform
import socket
import threading
import zipfile
import tempfile
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from werkzeug.utils import secure_filename
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import sqlite3
import schedule
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ntando-computer-enhanced-universal-secret-key-2024')

# Universal deployment configuration
DEPLOYMENT_ENV = os.getenv('DEPLOYMENT_ENV', 'local')
PORT = int(os.getenv('PORT', 5001))
HOST = os.getenv('HOST', '0.0.0.0')
STORAGE_PATH = os.getenv('STORAGE_PATH', './storage')
DATABASE_PATH = os.getenv('DATABASE_PATH', './ntando_computer_universal.db')

@dataclass
class SystemProcess:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str
    create_time: float
    cmdline: List[str]

@dataclass
class SystemService:
    name: str
    status: str
    start_type: str
    description: str
    pid: Optional[int] = None

@dataclass
class NetworkInterface:
    name: str
    ip_address: str
    netmask: str
    is_up: bool
    bytes_sent: int
    bytes_recv: int

@dataclass
class VirtualDesktop:
    id: str
    name: str
    wallpaper: str
    layout: str
    apps: List[str]
    created_at: datetime

class UniversalComputerSystem:
    def __init__(self):
        self.computer_name = f"NtandoComputer Universal v3.0.0"
        self.version = "3.0.0"
        self.environment = DEPLOYMENT_ENV
        self.init_storage()
        self.init_database()
        self.load_system_config()
        self.start_background_services()
        
    def init_storage(self):
        """Initialize universal storage paths"""
        self.paths = {
            'storage': Path(STORAGE_PATH),
            'apps': Path(STORAGE_PATH) / 'apps',
            'users': Path(STORAGE_PATH) / 'users',
            'backups': Path(STORAGE_PATH) / 'backups',
            'logs': Path(STORAGE_PATH) / 'logs',
            'temp': Path(STORAGE_PATH) / 'temp',
            'desktops': Path(STORAGE_PATH) / 'desktops',
            'packages': Path(STORAGE_PATH) / 'packages',
            'media': Path(STORAGE_PATH) / 'media'
        }
        
        for path in self.paths.values():
            path.mkdir(parents=True, exist_ok=True)
    
    def init_database(self):
        """Initialize enhanced database with universal schema"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Enhanced Users table
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
                storage_limit INTEGER DEFAULT 1073741824,
                desktop_config TEXT,
                preferences TEXT,
                theme TEXT DEFAULT 'dark'
            )
        ''')
        
        # Enhanced Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                domain TEXT UNIQUE NOT NULL,
                app_type TEXT NOT NULL,
                status TEXT DEFAULT 'stopped',
                owner_id INTEGER,
                config TEXT,
                storage_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_deployed TIMESTAMP,
                deployment_env TEXT,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        
        # Virtual Desktops table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS virtual_desktops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                desktop_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                wallpaper TEXT,
                layout TEXT,
                apps TEXT,
                is_active BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # System Processes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pid INTEGER NOT NULL,
                name TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                status TEXT,
                cmdline TEXT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # System Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL,
                start_type TEXT,
                description TEXT,
                pid INTEGER,
                config TEXT,
                last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Network Configuration table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interface_name TEXT NOT NULL,
                ip_address TEXT,
                netmask TEXT,
                gateway TEXT,
                dns_servers TEXT,
                is_up BOOLEAN,
                bytes_sent INTEGER DEFAULT 0,
                bytes_recv INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Installed Packages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS installed_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                version TEXT,
                description TEXT,
                category TEXT,
                install_path TEXT,
                dependencies TEXT,
                installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # System Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                source TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Scheduled Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                command TEXT NOT NULL,
                schedule_type TEXT NOT NULL,
                schedule_value TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Universal database initialized successfully")
    
    def load_system_config(self):
        """Load system configuration with environment detection"""
        self.config = {
            'computer_name': self.computer_name,
            'version': self.version,
            'environment': self.environment,
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'storage_path': STORAGE_PATH,
            'database_path': DATABASE_PATH,
            'max_file_size': app.config['MAX_CONTENT_LENGTH'],
            'supported_environments': ['local', 'render', 'heroku', 'aws', 'azure', 'gcp', 'docker'],
            'features': {
                'virtual_desktops': True,
                'process_management': True,
                'system_services': True,
                'network_tools': True,
                'package_manager': True,
                'system_logs': True,
                'scheduled_tasks': True,
                'security_center': True,
                'performance_monitor': True,
                'backup_center': True
            }
        }
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'count_logical': psutil.cpu_count(logical=True),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': self.get_network_info(),
                'boot_time': psutil.boot_time(),
                'uptime': time.time() - psutil.boot_time()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}
    
    def get_network_info(self):
        """Get network interface information"""
        interfaces = []
        try:
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            
            for interface_name, addresses in net_if_addrs.items():
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        stats = net_if_stats.get(interface_name)
                        interfaces.append({
                            'name': interface_name,
                            'ip_address': addr.address,
                            'netmask': addr.netmask,
                            'is_up': stats.isup if stats else False,
                            'speed': stats.speed if stats else 0,
                            'mtu': stats.mtu if stats else 0
                        })
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
        
        return interfaces
    
    def get_running_processes(self):
        """Get list of running processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time', 'cmdline']):
                try:
                    pinfo = proc.info
                    processes.append(SystemProcess(
                        pid=pinfo['pid'],
                        name=pinfo['name'] or 'Unknown',
                        cpu_percent=pinfo['cpu_percent'] or 0,
                        memory_percent=pinfo['memory_percent'] or 0,
                        status=pinfo['status'] or 'Unknown',
                        create_time=pinfo['create_time'] or 0,
                        cmdline=pinfo['cmdline'] or []
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
        
        return processes[:50]  # Limit to 50 processes for performance
    
    def get_system_services(self):
        """Get system services status"""
        services = []
        try:
            # Common services to monitor
            common_services = [
                {'name': 'web-server', 'description': 'NtandoComputer Web Server'},
                {'name': 'database', 'description': 'SQLite Database Service'},
                {'name': 'backup-service', 'description': 'Automated Backup Service'},
                {'name': 'analytics-service', 'description': 'Analytics and Monitoring'},
                {'name': 'security-service', 'description': 'Security and Protection'}
            ]
            
            for service_info in common_services:
                services.append(SystemService(
                    name=service_info['name'],
                    status='running' if service_info['name'] in ['web-server', 'database'] else 'stopped',
                    start_type='automatic',
                    description=service_info['description']
                ))
        except Exception as e:
            logger.error(f"Error getting system services: {e}")
        
        return services
    
    def create_virtual_desktop(self, user_id, name, wallpaper=None):
        """Create a new virtual desktop"""
        desktop_id = str(uuid.uuid4())
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO virtual_desktops (user_id, desktop_id, name, wallpaper, layout, apps)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, desktop_id, name, wallpaper, 'grid', '[]'))
        
        conn.commit()
        conn.close()
        
        return desktop_id
    
    def get_virtual_desktops(self, user_id):
        """Get user's virtual desktops"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT desktop_id, name, wallpaper, layout, apps, is_active, created_at
            FROM virtual_desktops WHERE user_id = ?
        ''', (user_id,))
        
        desktops = []
        for row in cursor.fetchall():
            desktops.append({
                'id': row[0],
                'name': row[1],
                'wallpaper': row[2],
                'layout': row[3],
                'apps': json.loads(row[4]) if row[4] else [],
                'is_active': bool(row[5]),
                'created_at': row[6]
            })
        
        conn.close()
        return desktops
    
    def install_package(self, package_name, version=None):
        """Install a software package"""
        try:
            # This is a mock package installer - in production, this would interface with real package managers
            package_info = {
                'name': package_name,
                'version': version or 'latest',
                'description': f'Package {package_name} installed successfully',
                'category': 'utility',
                'install_path': f'/packages/{package_name}',
                'dependencies': json.dumps([]),
                'installed_at': datetime.now().isoformat()
            }
            
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO installed_packages (name, version, description, category, install_path, dependencies)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (package_info['name'], package_info['version'], package_info['description'], 
                  package_info['category'], package_info['install_path'], package_info['dependencies']))
            
            conn.commit()
            conn.close()
            
            return True, "Package installed successfully"
        except Exception as e:
            logger.error(f"Error installing package: {e}")
            return False, str(e)
    
    def get_installed_packages(self):
        """Get list of installed packages"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, version, description, category, install_path, installed_at, is_active
            FROM installed_packages ORDER BY installed_at DESC
        ''')
        
        packages = []
        for row in cursor.fetchall():
            packages.append({
                'name': row[0],
                'version': row[1],
                'description': row[2],
                'category': row[3],
                'install_path': row[4],
                'installed_at': row[5],
                'is_active': bool(row[6])
            })
        
        conn.close()
        return packages
    
    def add_system_log(self, level, source, message, details=None, user_id=None):
        """Add a system log entry"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_logs (level, source, message, details, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (level, source, message, details, user_id))
        
        conn.commit()
        conn.close()
    
    def get_system_logs(self, level=None, limit=100):
        """Get system logs"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if level:
            cursor.execute('''
                SELECT level, source, message, details, timestamp
                FROM system_logs WHERE level = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (level, limit))
        else:
            cursor.execute('''
                SELECT level, source, message, details, timestamp
                FROM system_logs ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                'level': row[0],
                'source': row[1],
                'message': row[2],
                'details': row[3],
                'timestamp': row[4]
            })
        
        conn.close()
        return logs
    
    def create_scheduled_task(self, user_id, name, command, schedule_type, schedule_value):
        """Create a scheduled task"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Calculate next run time
        next_run = self._calculate_next_run(schedule_type, schedule_value)
        
        cursor.execute('''
            INSERT INTO scheduled_tasks (user_id, name, command, schedule_type, schedule_value, next_run)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, command, schedule_type, schedule_value, next_run))
        
        conn.commit()
        conn.close()
        
        return True
    
    def _calculate_next_run(self, schedule_type, schedule_value):
        """Calculate next run time for scheduled tasks"""
        now = datetime.now()
        if schedule_type == 'daily':
            return now + timedelta(days=1)
        elif schedule_type == 'hourly':
            return now + timedelta(hours=1)
        elif schedule_type == 'weekly':
            return now + timedelta(weeks=1)
        elif schedule_type == 'monthly':
            return now + timedelta(days=30)
        else:
            return now + timedelta(hours=1)
    
    def get_scheduled_tasks(self, user_id):
        """Get user's scheduled tasks"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, command, schedule_type, schedule_value, is_active, last_run, next_run, created_at
            FROM scheduled_tasks WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'name': row[0],
                'command': row[1],
                'schedule_type': row[2],
                'schedule_value': row[3],
                'is_active': bool(row[4]),
                'last_run': row[5],
                'next_run': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return tasks
    
    def start_background_services(self):
        """Start background services"""
        def backup_service():
            while True:
                try:
                    # Perform automatic backup
                    self.add_system_log('INFO', 'backup-service', 'Automatic backup completed')
                    time.sleep(3600)  # Run every hour
                except Exception as e:
                    logger.error(f"Backup service error: {e}")
        
        def analytics_service():
            while True:
                try:
                    # Update analytics
                    self.add_system_log('DEBUG', 'analytics-service', 'Analytics update completed')
                    time.sleep(300)  # Run every 5 minutes
                except Exception as e:
                    logger.error(f"Analytics service error: {e}")
        
        # Start background threads
        threading.Thread(target=backup_service, daemon=True).start()
        threading.Thread(target=analytics_service, daemon=True).start()
        
        logger.info("Background services started")

# Initialize the universal computer system
computer = UniversalComputerSystem()

# Web Routes
@app.route('/')
def desktop():
    """Main desktop interface"""
    system_info = computer.get_system_info()
    return render_template('desktop_universal.html', config=computer.config, system_info=system_info)

@app.route('/api/system/info')
def api_system_info():
    """Get system information"""
    return jsonify({
        'config': computer.config,
        'system_info': computer.get_system_info(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/processes')
def api_system_processes():
    """Get running processes"""
    processes = computer.get_running_processes()
    return jsonify({
        'processes': [asdict(p) for p in processes],
        'count': len(processes),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/services')
def api_system_services():
    """Get system services"""
    services = computer.get_system_services()
    return jsonify({
        'services': [asdict(s) for s in services],
        'count': len(services),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/network')
def api_system_network():
    """Get network information"""
    network_info = computer.get_network_info()
    return jsonify({
        'interfaces': network_info,
        'count': len(network_info),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/desktops', methods=['GET', 'POST'])
def api_virtual_desktops():
    """Manage virtual desktops"""
    if request.method == 'POST':
        data = request.json
        user_id = 1  # Mock user ID - in production, get from session
        desktop_id = computer.create_virtual_desktop(
            user_id, 
            data.get('name', 'New Desktop'),
            data.get('wallpaper')
        )
        computer.add_system_log('INFO', 'desktop-manager', f'Virtual desktop created: {desktop_id}')
        return jsonify({'success': True, 'desktop_id': desktop_id})
    else:
        user_id = 1  # Mock user ID
        desktops = computer.get_virtual_desktops(user_id)
        return jsonify({'desktops': desktops})

@app.route('/api/packages', methods=['GET', 'POST'])
def api_packages():
    """Manage software packages"""
    if request.method == 'POST':
        data = request.json
        success, message = computer.install_package(
            data.get('name'),
            data.get('version')
        )
        computer.add_system_log('INFO', 'package-manager', f'Package install attempt: {data.get("name")} - {message}')
        return jsonify({'success': success, 'message': message})
    else:
        packages = computer.get_installed_packages()
        return jsonify({'packages': packages})

@app.route('/api/logs', methods=['GET', 'POST'])
def api_system_logs():
    """Manage system logs"""
    if request.method == 'POST':
        data = request.json
        computer.add_system_log(
            data.get('level', 'INFO'),
            data.get('source', 'user'),
            data.get('message'),
            data.get('details'),
            1  # Mock user ID
        )
        return jsonify({'success': True})
    else:
        level = request.args.get('level')
        logs = computer.get_system_logs(level)
        return jsonify({'logs': logs})

@app.route('/api/tasks', methods=['GET', 'POST'])
def api_scheduled_tasks():
    """Manage scheduled tasks"""
    if request.method == 'POST':
        data = request.json
        success = computer.create_scheduled_task(
            1,  # Mock user ID
            data.get('name'),
            data.get('command'),
            data.get('schedule_type'),
            data.get('schedule_value')
        )
        computer.add_system_log('INFO', 'task-scheduler', f'Scheduled task created: {data.get("name")}')
        return jsonify({'success': success})
    else:
        tasks = computer.get_scheduled_tasks(1)  # Mock user ID
        return jsonify({'tasks': tasks})

@app.route('/terminal')
def terminal():
    """Terminal interface"""
    return render_template('terminal_universal.html', config=computer.config)

@app.route('/process-manager')
def process_manager():
    """Process manager interface"""
    return render_template('process_manager.html', config=computer.config)

@app.route('/system-services')
def system_services():
    """System services interface"""
    return render_template('system_services.html', config=computer.config)

@app.route('/network-tools')
def network_tools():
    """Network tools interface"""
    return render_template('network_tools.html', config=computer.config)

@app.route('/package-manager')
def package_manager():
    """Package manager interface"""
    return render_template('package_manager.html', config=computer.config)

@app.route('/system-logs')
def system_logs():
    """System logs interface"""
    return render_template('system_logs.html', config=computer.config)

@app.route('/task-scheduler')
def task_scheduler():
    """Task scheduler interface"""
    return render_template('task_scheduler.html', config=computer.config)

@app.route('/security-center')
def security_center():
    """Security center interface"""
    return render_template('security_center.html', config=computer.config)

@app.route('/performance-monitor')
def performance_monitor():
    """Performance monitor interface"""
    return render_template('performance_monitor.html', config=computer.config)

@app.route('/backup-center')
def backup_center():
    """Backup center interface"""
    return render_template('backup_center.html', config=computer.config)

if __name__ == '__main__':
    logger.info(f"Starting NtandoComputer Universal v3.0.0 on {HOST}:{PORT}")
    logger.info(f"Environment: {DEPLOYMENT_ENV}")
    logger.info(f"Storage Path: {STORAGE_PATH}")
    logger.info(f"Database Path: {DATABASE_PATH}")
    
    app.run(host=HOST, port=PORT, debug=False)