// Cấu hình pm2 để chạy Python web server cho thiệp cưới.
// Khởi động:  pm2 start ecosystem.config.js
// cwd = __dirname => chạy đúng dù đặt ở bất kỳ đường dẫn nào trên VPS.
module.exports = {
  apps: [
    {
      name: 'wedding',
      script: 'server.py',
      interpreter: 'python3',
      cwd: __dirname,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      env: {
        PYTHONUNBUFFERED: '1', // để log hiện ngay, không bị buffer
      },
    },
  ],
};
