from django.contrib import admin
from .models import DS_DangKy,DS_Lop,DS_NhatKy

class DS_Dangky_admin(admin.ModelAdmin):
    list_display=['Ten','Don_vi','Sdt_nguoi_than','Ly_do','Dia_diem',
                  'Ngay_dang_ky','Thoigian_ra','Thoigian_vao','Phe_duyet']
class Ds_Lop_admin(admin.ModelAdmin):
   list_display=['Ma_hv','Ten','Don_vi','Ngay_sinh','Que_quan']
class Ds_NhatKy_admin(admin.ModelAdmin):
   list_display=['Ngay_dang_ky','Ma_hv_id','Ten','Noi_dung','is_vipham','is_thanhtich','Diem']

admin.site.register(DS_NhatKy,Ds_NhatKy_admin)
admin.site.register(DS_Lop, Ds_Lop_admin)
admin.site.register(DS_DangKy,DS_Dangky_admin)

   
