from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Hệ thống Quản lý Sinh viên",
    description="API quản lý thông tin sinh viên xây dựng bằng FastAPI - Git Lab",
    version="1.0.0",
)


# ==========================================
# Data Models (Pydantic)
# ==========================================
class StudentBase(BaseModel):
    student_code: str = Field(..., example="SV001", description="Mã số sinh viên")
    full_name: str = Field(..., example="Nguyễn Văn A", description="Họ và tên")
    email: EmailStr = Field(..., example="vana@example.com", description="Email sinh viên")
    major: str = Field(..., example="Công nghệ thông tin", description="Chuyên ngành")
    gpa: float = Field(..., ge=0.0, le=4.0, example=3.5, description="Điểm trung bình tích lũy (hệ 4)")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="Nguyễn Văn B")
    email: Optional[EmailStr] = Field(None, example="vanb@example.com")
    major: Optional[str] = Field(None, example="Khoa học máy tính")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, example=3.8)


class Student(StudentBase):
    id: int = Field(..., description="ID định danh hệ thống")


# ==========================================
# In-Memory Database (Dữ liệu mẫu)
# ==========================================
students_db: List[Student] = [
    Student(
        id=1,
        student_code="SV001",
        full_name="Nguyễn Văn An",
        email="an.nv@example.com",
        major="Công nghệ thông tin",
        gpa=3.6,
    ),
    Student(
        id=2,
        student_code="SV002",
        full_name="Trần Thị Bình",
        email="binh.tt@example.com",
        major="Hệ thống thông tin",
        gpa=3.2,
    ),
    Student(
        id=3,
        student_code="SV003",
        full_name="Lê Hoàng Cường",
        email="cuong.lh@example.com",
        major="Kỹ thuật phần mềm",
        gpa=3.8,
    ),
]


# ==========================================
# API Endpoints
# ==========================================
@app.get("/", tags=["Root"])
def read_root():
    """Trang chủ chào mừng và chuyển hướng tài liệu."""
    return {
        "message": "Chào mừng đến với API Quản lý Sinh viên",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


# 1. Hiển thị danh sách sinh viên (Role: Hoàng)
@app.get("/students", response_model=List[Student], tags=["Sinh viên"])
def get_all_students():
    """Lấy toàn bộ danh sách sinh viên."""
    return students_db


# 2. Tìm kiếm sinh viên (Role: MĐA)
@app.get("/students/search", response_model=List[Student], tags=["Sinh viên"])
def search_students(
    query: Optional[str] = Query(None, description="Tìm theo tên hoặc mã sinh viên"),
    major: Optional[str] = Query(None, description="Lọc theo chuyên ngành"),
):
    """Tìm kiếm sinh viên theo từ khóa (họ tên, mã SV) hoặc theo chuyên ngành."""
    results = students_db

    if query:
        q = query.lower()
        results = [
            s for s in results
            if q in s.full_name.lower() or q in s.student_code.lower()
        ]

    if major:
        results = [s for s in results if major.lower() in s.major.lower()]

    return results


# 3. Lấy thông tin chi tiết một sinh viên theo ID
@app.get("/students/{student_id}", response_model=Student, tags=["Sinh viên"])
def get_student_by_id(student_id: int):
    """Lấy thông tin chi tiết của một sinh viên theo ID."""
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sinh viên có ID {student_id}",
    )


# 4. Thêm mới sinh viên (Role: Trọng)
@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    tags=["Sinh viên"],
)
def create_student(student_in: StudentCreate):
    """Thêm mới một sinh viên vào hệ thống."""
    # Kiểm tra mã sinh viên đã tồn tại chưa
    if any(s.student_code.lower() == student_in.student_code.lower() for s in students_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã sinh viên '{student_in.student_code}' đã tồn tại!",
        )

    # Tự động tăng ID
    new_id = max([s.id for s in students_db], default=0) + 1
    new_student = Student(id=new_id, **student_in.model_dump())
    students_db.append(new_student)
    return new_student


# 5. Cập nhật thông tin sinh viên
@app.put("/students/{student_id}", response_model=Student, tags=["Sinh viên"])
def update_student(student_id: int, student_update: StudentUpdate):
    """Cập nhật thông tin của sinh viên theo ID."""
    for idx, student in enumerate(students_db):
        if student.id == student_id:
            update_data = student_update.model_dump(exclude_unset=True)
            updated_student = student.model_copy(update=update_data)
            students_db[idx] = updated_student
            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sinh viên có ID {student_id}",
    )


# 6. Xóa sinh viên
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Sinh viên"])
def delete_student(student_id: int):
    """Xóa sinh viên khỏi hệ thống theo ID."""
    for idx, student in enumerate(students_db):
        if student.id == student_id:
            deleted = students_db.pop(idx)
            return {"message": f"Đã xóa sinh viên {deleted.full_name} ({deleted.student_code}) thành công"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sinh viên có ID {student_id}",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
