from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import DS_DangKy,DS_NhatKy,DS_Lop
from .form import Dangki,Nhatki
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
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác")
    return render(request, 'login.html')
# View cho logout
def logout_view(request):
    logout(request)
    return redirect('login')
#----------------------------------------------------------------------Admin
# View cho manager
@login_required(login_url='login')
@admin_required
def diary_list(request):
      context ={
          'diary_list':None
      }
      diary_list = DS_NhatKy.objects.all()
      context['diary_list'] = diary_list
      html_template = loader.get_template('diary_list.html')
      return HttpResponse(html_template.render(context, request))
# View cho form nhật ký
@login_required(login_url='login')
@admin_required
def diary_form(request):
    if request.method == 'POST':
        form = Nhatki(request.POST)
        if form.is_valid():
            ma_hv = form.cleaned_data['Ma_hv']
            ten = form.cleaned_data['Ten']
               # Kiểm tra xem ma_hv có tồn tại trong bảng DS_LOP
            if DS_Lop.objects.filter(pk=ma_hv).filter(Ten = ten).exists():
                pass
            else:
                messages.error(request, "Mã học viên hoặc Tên không tồn tại")
                return render(request, 'diary_form.html',{'form':Nhatki()})
            noi_dung = form.cleaned_data['Noi_dung']
            diem = form.cleaned_data['Diem']
            if form.cleaned_data['selection'] == 'is_vipham':
                vipham = True
                thanhtich = False
            else:
                thanhtich = True
                vipham= False
            DS_NhatKy.objects.create(
                Ma_hv_id = ma_hv,
                Ten = ten,
                Noi_dung = noi_dung ,
                is_vipham = vipham,
                is_thanhtich = thanhtich,
                Diem = diem,
                Ngay_dang_ky = date.today()
            )
            messages.success(request, "Nhật ký đã được thêm thành công")
            return render(request, 'diary_form.html',{'form':Nhatki()})
    else:  
        form = Nhatki()
    return render(request, 'diary_form.html',{'form':form})
#----------------------------------------------------------------------User
# View cho danh sách đăng kí 
@login_required(login_url='login')
def waiting_list(request):
    context = {
        'Waiting_list':None
    }
    Waiting_list = DS_DangKy.objects.all()
    context['Waiting_list'] = Waiting_list
    for item in context['Waiting_list']:
        Pre = DS_NhatKy.objects.filter(Ten = item.Ten).aggregate(total_sum = Sum('Diem'))
        total_sum = Pre['total_sum'] 
        if total_sum is None:
            item.Phe_duyet = True
        elif total_sum >= 0:
            item.Phe_duyet = True
        else:
            item.Phe_duyet = False
    
    html_template = loader.get_template('waiting_list.html')
    return HttpResponse(html_template.render(context, request))
# View cho trang home
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')
# View cho thông báo kết quả!
@login_required(login_url='login')
def Notification(request):
    return render(request,'thongbao.html')
# View cho form đăng ký ra vào doanh trại
@login_required(login_url='login')
def register_view(request):
    context = ''
    if request.method == 'POST':
        form = Dangki(request.POST)
        if form.is_valid():
            ma_hv = form.cleaned_data['Ma_hv']
            ten = form.cleaned_data['Ten']
            if DS_Lop.objects.filter(pk=ma_hv).filter(Ten= ten).exists():
                pass
            else:
                form = Dangki()
                messages.error(request, "Mã học viên hoặc Tên Sai")
                return render(request, 'diary_form.html',{'form':form})
            don_vi = form.cleaned_data['Don_vi']
            sdt_nguoi_than = form.cleaned_data['Sdt_nguoi_than']
            ly_do = form.cleaned_data['Ly_do']
            dia_diem = form.cleaned_data['Dia_diem']
            thoigian_ra = form.cleaned_data['Thoigian_ra']
            thoigian_vao = form.cleaned_data['Thoigian_vao']
            DS_DangKy.objects.create(
                Ma_hv_id=ma_hv,
                Ten=ten,
                Don_vi=don_vi,
                Sdt_nguoi_than=sdt_nguoi_than,
                Ly_do=ly_do,
                Dia_diem=dia_diem,
                Ngay_dang_ky = date.today(), 
                Thoigian_ra=thoigian_ra,
                Thoigian_vao=thoigian_vao,
            )
            messages.success(request, "Thành công")
            return render(request, 'diary_form.html',{'form':form,'context':context})
    else:
        form = Dangki()    
    return render(request, 'register.html',{'form':form})


def cv_view(request):
    url = "https://randomuser.me/api/?results=1"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse JSON từ API
        data = response.json()
        users = data.get("results",[])
    else:
        users = []
    # Truyền dữ liệu tới template
    return render(request, "cv.html", {"users": users})

def cv_view2(request):
    data_json = {
    "id": "17",
    "ho_ten": "Tô Trung Nghĩa",
    "ngay_sinh": "22/04/1991",
    "gioi_tinh": "Nam",
    "que_quan": "Hồ Chí Minh",
    "dia_chi": "56 Đường Lê Văn Sỹ, Hồ Chí Minh",
    "dien_thoai": "0902345679",
    "email": "totrungnghia@email.com",
    "hoc_van": {
        "truong": "Đại học QRS",
        "chuyen_nganh": "Quản trị Kinh doanh",
        "khoa": "2010-2014",
        "xep_loai": "Khá"
    },
    "kinh_nghiem": [
        {
            "cong_ty": "Công ty DEF",
            "thoi_gian": "2021",
            "vi_tri": "Chuyên viên marketing",
            "cong_viec": "Lập kế hoạch chiến lược marketing và quảng bá sản phẩm"
        },
        {
            "cong_ty": "Công ty GHI",
            "thoi_gian": "2019",
            "vi_tri": "Nhân viên marketing",
            "cong_viec": "Quản lý các chiến dịch truyền thông và quảng cáo"
        }
    ],
    "diem_manh": [
        "Kỹ năng giao tiếp tốt",
        "Khả năng lên kế hoạch chiến lược"
    ],
    "muc_tieu": [
        "Phát triển sự nghiệp trong lĩnh vực marketing và quản lý thương hiệu"
    ]
    }
    return render(request, "cv2.html", {"data": data_json})