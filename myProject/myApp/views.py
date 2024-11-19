from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from datetime import date
import requests
import json
#import requests

# decorator: kiểm tra xem user có phải là admin
# view_func đại diện cho view sẽ được áp dùng
def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            # Thêm Điều hướng đến trang thông báo lỗi!
            return HttpResponse('Bạn không phải là admin')
        return view_func(request, *args, **kwargs)
    return wrapped_view

#----------------------------------------------------------------------
# View login

#----------------------------------------------------------------------Admin


def cv_view_pro(request):
    # id người dùng
    id = 15
    base_url = "http://192.178.205.140:8000/Thisinh/"
    # đường url chính xác
    url = f"{base_url}{id}"
    # Gửi yêu cầu GET đến url và lấy dữ liệu trả về
    response = requests.get(url)
    data = response.json()
    
    user_info = {
        "id": data.get("id"),
        "bidanh": data.get("bidanh"),
        "chucdanh": data.get("chucdanh"),
        "lienhe": data.get("lienhe"),
        "hocvan": data.get("hocvan"),
        "diemmanh": data.get("diemmanh"),
        "thongtincanhan": data.get("thongtincanhan"),
        "kinhnghiemlamviec": data.get("kinhnghiemlamviec"),
        "muctieucongviec": data.get("muctieucongviec"),
    }
    Nganhan = user_info["muctieucongviec"]['Ngắn hạn']
    Daihan = user_info["muctieucongviec"]['Dài hạn']
    
    # Truyền dữ liệu tới template
    return render(request, "cv_final.html", {"user_info": user_info,'Nganhan':Nganhan,'Daihan':Daihan,})

def cv_view2(request):
    api_url = "https://jsonplaceholder.typicode.com/users"
    
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(api_url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        # Lấy dữ liệu JSON từ API
        data = json.loads(response.text)
        users = data
    except requests.exceptions.RequestException as e:
        # Nếu lỗi, trả về danh sách rỗng và thông báo
        users = []
        print(f"Lỗi khi gọi API: {e}")
    print(users)
    # Render dữ liệu lên template
    return render(request, "cv.html", {"users": users})