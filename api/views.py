import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from api import movie_api
from api.response import JsonResponse, JsonError

data = dict()
data["movie_tag"] = movie_api.Movie().get_movie_tag()


def page_not_found(request, exception):
    return render(request, 'tempate.html', {"tip": "404错误，网页地址信息错误，请检确认无误后访问！", "url": "/", "time": 3,
                                            "title": "404错误页面", "data": data}, status=404)
    # return render(request, 'page/404.html', {"status": 404}, status=404)


def page_error(request):
    return render(request, 'tempate.html', {"tip": "500错误，服务端出错，请联系系统管理员！", "url": "/", "time": 3,
                                            "title": "500错误页面", "data": data}, status=500)
    # return render(request, 'page/500.html', {"status": 500}, status=500)
@require_GET
def img_proxy(request):
    """
    /api/img_proxy?url=<douban_image_url>
    代理豆瓣图片，解决防盗链问题
    """
    url = request.GET.get("url", "")
    if not url:
        return HttpResponse(status=400)

    # 放宽域名限制：同时支持 doubanio.com 和 douban.com
    allowed_domains = ["doubanio.com", "douban.com", "img1.doubanio.com", "img2.doubanio.com",
                       "img3.doubanio.com", "img9.doubanio.com", "movie.douban.com"]
    if not any(domain in url for domain in allowed_domains):
        return HttpResponse(status=403)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://movie.douban.com/",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException:
        return HttpResponse(status=502)

    if r.status_code != 200:
        return HttpResponse(status=r.status_code)

    content_type = r.headers.get("Content-Type", "image/jpeg")
    resp = HttpResponse(r.content, content_type=content_type)
    resp["Cache-Control"] = "public, max-age=86400"  # 缓存 1 天，减少重复请求
    resp["Access-Control-Allow-Origin"] = "*"
    return resp


@require_GET
def realtime_recommend(request):
    """
    /api/realtime_recommend?top_n=20
    实时推荐API - 返回混合推荐列表
    """
    user_id = request.session.get("user_id", 2)
    top_n = int(request.GET.get("top_n", 20))
    movie = movie_api.Movie()
    data = movie.get_realtime_recommend(user_id, top_n)
    return JsonResponse(data)


@require_GET
def realtime_recommend_grouped(request):
    """
    /api/realtime_recommend_grouped?per_type=5
    按类型分组的实时推荐API - 返回按类型分组的推荐列表
    """
    user_id = request.session.get("user_id", 2)
    per_type = int(request.GET.get("per_type", 5))
    movie = movie_api.Movie()
    data = movie.get_realtime_recommend_grouped(user_id, per_type)
    return JsonResponse(data)
