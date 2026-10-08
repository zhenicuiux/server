module.exports = {
  apps: [
    {
      name: "web-dashboard",
      script: "server_dashboard_starter.py",
      interpreter: "python3",
      args: "--port 8000",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      env: {
        NODE_ENV: "production",
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
};
