# Thiệp Cưới Điện Tử - Hoàng Nam & Thanh Tú

Một trang web thiệp cưới interactive với tính năng lưu lời chúc khách mời vào file CSV.

## 📋 Tính Năng

- ✨ Thiệp cưới 3D với hiệu ứng tim rơi
- 📖 Trang chi tiết sự kiện đầy đủ
- 📝 Sổ lưu bút - khách có thể để lại lời chúc
- 💾 Lưu lời chúc vào file CSV
- 📱 Responsive - hoạt động tốt trên mobile
- 🎨 Thiết kế đẹp với phong cách truyền thống

## 🚀 Cách Cài Đặt & Chạy

### Yêu Cầu
- Node.js v14 trở lên
- npm hoặc yarn

### Bước 1: Cài Đặt Dependencies

```bash
cd hai-tam-wedding
npm install
```

Hoặc nếu dùng yarn:
```bash
yarn install
```

### Bước 2: Chạy Server

```bash
npm start
```

Server sẽ chạy tại: **http://localhost:3000**

### Bước 3: Mở Thiệp

- **Trang chính (Envelope)**: http://localhost:3000/
- **Trang chi tiết**: http://localhost:3000/chi-tiet.html

## 📁 Cấu Trúc File

```
hai-tam-wedding/
├── index.html              # Thiệp chính
├── chi-tiet.html          # Trang chi tiết với sổ lưu bút
├── server.js              # Node.js backend server
├── package.json           # Dependencies
├── wishes.csv             # File lưu lời chúc (tự động tạo)
└── README.md              # File này
```

## 📊 File CSV (wishes.csv)

Lời chúc được lưu tự động vào file `wishes.csv` với định dạng:

```
Tên,Lời chúc,Ngày giờ
"Anh Tuấn","Chúc hai bạn hạnh phúc","07/07/2026 14:30:45"
"Chị Mai","Yêu nhau lâu dài","07/07/2026 15:45:20"
```

Mỗi khi khách gửi lời chúc:
1. Dữ liệu được gửi đến server via API
2. Server tự động ghi vào file CSV
3. Trang web tự động reload để hiển thị lời chúc mới

## 🔗 API Endpoints

### GET /api/wishes
- Lấy danh sách tất cả lời chúc
- Response: JSON array

```javascript
[
  {
    "name": "Tên khách",
    "wish": "Lời chúc",
    "time": "07/07/2026 14:30:45"
  }
]
```

### POST /api/wishes
- Thêm lời chúc mới
- Body: JSON

```javascript
{
  "name": "Tên khách",
  "wish": "Lời chúc"
}
```

## 🔧 Tùy Chỉnh

### Thay Đổi Tên Cô Dâu/Chú Rể

Trong `chi-tiet.html`, tìm và sửa:

```html
<h2>Hoàng Nam</h2>  <!-- Chú rể -->
<h2>Thanh Tú</h2>   <!-- Cô dâu -->
```

### Thay Đổi Ngày Giờ Sự Kiện

Trong `chi-tiet.html`, script section:

```javascript
function setEventDate() {
    const eventDate = new Date(2026, 1, 1); // Tháng 2, ngày 1, năm 2026
    // ...
}
```

### Thay Đổi Port Server

Trong `server.js`:

```javascript
const PORT = 3000; // Thay 3000 thành port khác
```

## 📝 Sử Dụng

1. Khách truy cập trang chi tiết (`chi-tiet.html`)
2. Cuộn xuống phần "Sổ Lưu Bút"
3. Nhập tên và lời chúc
4. Click nút "Gửi Lời Chúc"
5. Lời chúc được lưu vào `wishes.csv` và hiển thị ngay trên trang

## 🛑 Dừng Server

Nhấn `Ctrl + C` trong terminal

## 📦 Development Mode (Optional)

Để tự động reload server khi có thay đổi, cài nodemon:

```bash
npm install -D nodemon
npm run dev
```

## 🐛 Troubleshooting

### Lỗi "Cannot find module 'express'"
```bash
npm install
```

### Lỗi "Port 3000 already in use"
Thay đổi port trong `server.js` hoặc dừng ứng dụng khác đang dùng port 3000

### CSV file không được tạo
Server sẽ tự động tạo file `wishes.csv` khi khách gửi lời chúc đầu tiên

## 📄 License

MIT

---

**Chúc mừng Hoàng Nam & Thanh Tú! 💕**
