# git-lab-AAA - Quản lý sinh viên với FastAPI

Hệ thống API quản lý thông tin sinh viên xây dựng bằng framework **FastAPI**.

## Phân công nhiệm vụ (Roles)
- **Hoàng**: Hiển thị dữ liệu (`GET /students`)
- **MĐA**: Tìm kiếm dữ liệu (`GET /students/search`)
- **Trọng**: Thêm dữ liệu (`POST /students`)

---

## Hướng dẫn cài đặt và chạy chương trình

### 1. Cài đặt thư viện phụ thuộc
Khuyến nghị tạo môi trường ảo Python trước khi cài đặt:

```bash
# Tạo môi trường ảo (tùy chọn)
python -m venv venv

# Kích hoạt trên Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Cài đặt thư viện:
pip install -r requirements.txt
```

### 2. Khởi chạy server FastAPI
Chạy bằng lệnh Uvicorn:
```bash
uvicorn main:app --reload
```
Hoặc chạy trực tiếp file `main.py`:
```bash
python main.py
```

Server sẽ chạy tại địa chỉ: `http://127.0.0.1:8000`

### 3. Xem tài liệu API tự động (Interactive Swagger UI)
Truy cập trình duyệt:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
