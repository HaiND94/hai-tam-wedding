#!/usr/bin/env python3
"""
Web server cho thiệp cưới.
- Serve các file tĩnh (detail.html, index.html, data-images, music...)
- API lưu / đọc lời chúc trong data/wishes.csv
- API lưu / đọc danh sách xác nhận tham dự trong data/confirmations.csv

Chạy:  python3 server.py
Mở:    http://localhost:3000/detail.html
"""

import csv
import json
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'wishes.csv')
CSV_HEADER = ['time', 'name', 'wish']
CONFIRM_PATH = os.path.join(DATA_DIR, 'confirmations.csv')
CONFIRM_HEADER = ['time', 'name']


def ensure_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerow(CSV_HEADER)


def ensure_confirm_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIRM_PATH):
        with open(CONFIRM_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerow(CONFIRM_HEADER)


def read_wishes():
    ensure_csv()
    wishes = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            wishes.append({
                'time': row.get('time', ''),
                'name': row.get('name', ''),
                'wish': row.get('wish', ''),
            })
    return wishes


def append_wish(name, wish):
    ensure_csv()
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(CSV_PATH, 'a', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerow([time, name, wish])
    return {'time': time, 'name': name, 'wish': wish}


def read_confirmations():
    ensure_confirm_csv()
    rows = []
    with open(CONFIRM_PATH, 'r', newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            rows.append({
                'time': row.get('time', ''),
                'name': row.get('name', ''),
            })
    return rows


def save_confirmation(name):
    """Lưu xác nhận, dedupe theo tên (không phân biệt hoa/thường)."""
    ensure_confirm_csv()
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    rows = read_confirmations()

    key = name.strip().lower()
    found = False
    for row in rows:
        if row['name'].strip().lower() == key:
            row['time'] = time  # cập nhật thời gian xác nhận mới nhất
            found = True
            break
    if not found:
        rows.append({'time': time, 'name': name})

    with open(CONFIRM_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(CONFIRM_HEADER)
        for row in rows:
            writer.writerow([row['time'], row['name']])

    return {'time': time, 'name': name}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length) or b'{}')

    def do_GET(self):
        if self.path == '/api/wishes':
            try:
                self._send_json({'wishes': read_wishes()})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
            return
        if self.path == '/api/confirmations':
            try:
                self._send_json({'confirmations': read_confirmations()})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == '/api/wishes':
            try:
                payload = self._read_json_body()
                name = (payload.get('name') or '').strip()
                wish = (payload.get('wish') or '').strip()
                if not name or not wish:
                    self._send_json({'error': 'Thiếu tên hoặc lời chúc'}, 400)
                    return
                saved = append_wish(name, wish)
                self._send_json({'ok': True, 'wish': saved})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
            return
        if self.path == '/api/confirm':
            try:
                payload = self._read_json_body()
                name = (payload.get('name') or '').strip()
                if not name:
                    self._send_json({'error': 'Thiếu tên người xác nhận'}, 400)
                    return
                saved = save_confirmation(name)
                self._send_json({'ok': True, 'confirmation': saved})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
            return
        self.send_error(404, 'Not found')


if __name__ == '__main__':
    ensure_csv()
    ensure_confirm_csv()
    print(f'Server chạy tại http://localhost:{PORT}/detail.html')
    print(f'Lời chúc lưu vào: {CSV_PATH}')
    print(f'Xác nhận tham dự lưu vào: {CONFIRM_PATH}')
    ThreadingHTTPServer(('', PORT), Handler).serve_forever()
