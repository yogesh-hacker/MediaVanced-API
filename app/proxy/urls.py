from django.urls import re_path
from revproxy.views import ProxyView

urlpatterns = [
    re_path(r'(?P<path>.*)', ProxyView.as_view(upstream='https://dave.ydc1wes.me/hls2/02/00004/revdbzh3201i_l/master.m3u8?t=uttz-ed_2vWuNinDDrE5u11X0OJJWfNU5A7PmHA2d20&s=1720273211&e=21600&f=22264&i=0.0&sp=0')),
]