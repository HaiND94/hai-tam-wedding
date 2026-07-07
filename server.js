const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

const CSV_FILE = path.join(__dirname, 'wishes.csv');

// Initialize CSV file with headers if it doesn't exist
function initializeCSV() {
    if (!fs.existsSync(CSV_FILE)) {
        const headers = 'Tên,Lời chúc,Ngày giờ\n';
        fs.writeFileSync(CSV_FILE, headers, 'utf8');
    }
}

// Get all wishes
app.get('/api/wishes', (req, res) => {
    initializeCSV();
    try {
        const data = fs.readFileSync(CSV_FILE, 'utf8');
        const lines = data.trim().split('\n');

        if (lines.length <= 1) {
            return res.json([]);
        }

        const wishes = lines.slice(1).map(line => {
            // Parse CSV - handle commas in content
            const parts = [];
            let current = '';
            let inQuotes = false;

            for (let i = 0; i < line.length; i++) {
                const char = line[i];
                if (char === '"') {
                    inQuotes = !inQuotes;
                } else if (char === ',' && !inQuotes) {
                    parts.push(current.replace(/^"|"$/g, ''));
                    current = '';
                } else {
                    current += char;
                }
            }
            parts.push(current.replace(/^"|"$/g, ''));

            return {
                name: parts[0] || '',
                wish: parts[1] || '',
                time: parts[2] || ''
            };
        }).filter(w => w.name && w.wish);

        res.json(wishes);
    } catch (error) {
        console.error('Error reading wishes:', error);
        res.status(500).json({ error: 'Failed to read wishes' });
    }
});

// Add a new wish
app.post('/api/wishes', (req, res) => {
    initializeCSV();
    try {
        const { name, wish } = req.body;

        if (!name || !wish) {
            return res.status(400).json({ error: 'Name and wish are required' });
        }

        // Escape quotes and create CSV line
        const escapedName = `"${name.replace(/"/g, '""')}"`;
        const escapedWish = `"${wish.replace(/"/g, '""')}"`;
        const now = new Date();
        const time = now.toLocaleString('vi-VN');

        const line = `${escapedName},${escapedWish},"${time}"\n`;

        fs.appendFileSync(CSV_FILE, line, 'utf8');

        res.json({
            success: true,
            wish: {
                name,
                wish,
                time
            }
        });
    } catch (error) {
        console.error('Error saving wish:', error);
        res.status(500).json({ error: 'Failed to save wish' });
    }
});

// Serve index.html at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

initializeCSV();
app.listen(PORT, () => {
    console.log(`🎉 Thiệp cưới server đang chạy tại http://localhost:${PORT}`);
    console.log(`📝 Lời chúc được lưu tại: ${CSV_FILE}`);
});