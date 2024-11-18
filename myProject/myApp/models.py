from django.db import models
from django.utils import timezone


class DS_Lop(models.Model):
    Ma_hv = models.IntegerField(primary_key=True, default=000) 
    Ten = models.CharField(max_length=100)
    Don_vi = models.CharField(max_length=100)
    Ngay_sinh = models.DateField()
    Que_quan = models.CharField(max_length=100)

class DS_DangKy(models.Model):
    # on _delete xóa đi dòng khi nào Ma_hv không tồn tại trong bảng gốc!
    Ma_hv = models.ForeignKey(DS_Lop, on_delete=models.CASCADE, to_field='Ma_hv')
    Ten = models.CharField(max_length=100)
    Don_vi = models.CharField(max_length=100)
    Sdt_nguoi_than = models.CharField(max_length=15)
    Ly_do = models.TextField()
    Dia_diem = models.CharField(max_length=100)
    Ngay_dang_ky = models.DateField()
    Thoigian_ra = models.TimeField()
    Thoigian_vao = models.TimeField()
    Phe_duyet = models.BooleanField(default=False)

class DS_NhatKy(models.Model):
    Ma_hv = models.ForeignKey(DS_Lop, on_delete=models.CASCADE, to_field='Ma_hv') 
    Ten = models.CharField(max_length=100)
    Noi_dung = models.CharField(max_length=256)
    Ngay_dang_ky = models.DateField()
    is_vipham = models.BooleanField(default=False)
    is_thanhtich = models.BooleanField(default=False)
    Diem = models.IntegerField()

     


