from django.shortcuts import render, redirect

from app01.models import Department, UserInfo, PhoneNumbers
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import NumModelForm, NumModelFormEdit, UserModelForm
from django.db import connection

def batchdata_list(req):
    search_data_dict = {}
    search_data = req.GET.get("q", "")

    if search_data:
        search_data_dict["name__contains"] = search_data
        # mobile__contains==xx 作为filter参数表示字符串包含xx 类似的 还有 __gt __lte __startwith
    queryset = UserInfo.objects.filter(**search_data_dict)
    # 相当于 order by level desc ,   queryset切片可以越界但要为正数

    # queryset = UserInfo.objects.all()
    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    content = {
        "queryset": page_queryset,
        "page_nav_string": page_nav_string,
    }
    return render(req, "batch/batchdata_list.html", content)



def query_article_number(req):
    query = req.GET.get('q', '')
    results = []
    if query:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM articles WHERE article_number LIKE %s", ['%' + query + '%'])
            print('ddddddddddddddd')
            results = cursor.fetchall()
    return render(req, 'batch/query_article_number.html', {'results': results})



def user_delete(req):
    nid = req.GET.get("nid")
    UserInfo.objects.filter(user_id=nid).delete()
    return redirect("/user/list")


def user_edit(req, nid):
    row_obj = UserInfo.objects.filter(user_id=nid).first()  # 查找出这一行
    ct = row_obj.creat_time
    if req.method == "GET":
        form = UserModelForm(instance=row_obj)  # 显示时显示默认值
        return render(req, "users/user_edit.html", {"form": form})

    form = UserModelForm(data=req.POST, instance=row_obj)  # 用post的消息更新表单，instance表示修改而不是新增
    if form.is_valid():
        # form.instance.字段名 = 手动赋值
        if form.instance.creat_time is None:
            form.instance.creat_time = ct
        form.save()
        return redirect("/user/list")
    return render(req, "users/user_edit.html", {"form": form})