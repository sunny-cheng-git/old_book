from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from app01.myforms import Sell_bookForm,UserForm,LoginForm
from django.contrib import auth
from django.db import transaction
import json,datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):


    return render(request,'base_foot.html')

def home(request):
    response = {'title':None,"msg":None}
    categories = models.Category.objects.all()
    book_list=models.Book.objects.all().order_by('sid')
    paginator = Paginator(book_list, 5) #每页5条
    if request.method == "POST": #动态记载返回数据
        page = request.POST.get('page')
        currentPage=int(page)
        try:
            print(page)
            books = paginator.page(page)
            books.has_next()
            data = serializers.serialize("json", books)
            response['title'] = data
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
            response['msg'] = '已经没有数据了'
        return JsonResponse(response)
    page = request.GET.get('page',1)
    books = paginator.page(page)
    return render(request,'book_list.html',locals())


def search(request):

    books = models.Book.objects.all()
    if request.method == "POST":
        print('dd')
        response = {'data':None,'msg':None}
        condition = request.POST.get('search_text')
        condition_list = books.filter(Q(title=condition) | Q(author=condition) | Q(category__title=condition)).all()
        # condition_list = book_list.filter(category__title=condition).all()
        data = serializers.serialize('json',condition_list)
        print('ds',data,type(data))
        print(condition_list)
        if condition_list:
            response['data'] = data
        else:
            response['msg'] = '暂时没有您查询的书籍'
        return JsonResponse(response)

    return render(request,'search.html')


def category(request):
    if request.method == 'POST':
        print(request.method)
        response = {'title':None,"msg":None}
        cate_id = request.POST.get('category_id')
        print(cate_id)
        cate_obj = models.Category.objects.filter(cid=cate_id).first()
        cate_list = cate_obj.book_set.all()

        response['title'] = json.loads(serializers.serialize('json', cate_list))

        return JsonResponse(response,safe=False)


    categories = models.Category.objects.all()
    return render(request,'category.html',{'category':categories})

def book_detail(request,id):
    if request.method == 'POST':
        parent_comt = request.POST.get('parent_comt')
        comt_objs = models.Comment.objects.filter(parent_comment=parent_comt,book=id).all().values_list('content','create_time','user__username')

        return JsonResponse(list(comt_objs),safe=False)
    book_obj = models.Book.objects.filter(sid=id).first()
    comment_list = models.Comment.objects.filter(book=book_obj)
    # 前端展示留言有多少条信息
        # 1.通过后端传过去
        # 2.前端如果没有留言 提示框5秒 关闭
    from django.db.models import Avg
    book_score = models.Comment.objects.filter(book=id).aggregate(Avg('score'))#评分计算规则只算有打分的
    print('book_score',book_score['score__avg'])
    score = book_score['score__avg']
    print(score)

    return  render(request,'book_detail.html',{"book":book_obj,"comment_list":comment_list,'score':score})



def shop_car(request):
    if request.method == 'POST':
        response = {'title':None,"msg":None}
        price_count = request.POST.get('price_count')
        print(price_count)
        # book_list = request.POST.get('book_list[]')
        car_list = request.POST.getlist('book_list[]')
        print(car_list,type(car_list))
        # 这里已经拿到了结算的价格了
        now = datetime.datetime.now().strftime('%Y%m%d%H%m%s')
        print(now)
        #创建订单
        with transaction.atomic():
            order_obj = models.Order.objects.create(user=request.user,order_number=now,actual_amount=price_count,status=1,date=datetime.datetime.now())
        #一个订单里面有多本书,一本书对应一个详情，并且事务回滚
            for i in car_list:
                b_obj = models.Shopping_car.objects.filter(sid=i).first()
                print(b_obj,type(b_obj),b_obj.book)
                print(b_obj.book.book_detail,type(b_obj.book.book_detail))
                models.OrderDetail.objects.create(order=order_obj,book=b_obj.book,original_price=0,price=0)
                b_obj.book.book_detail.status = 1
                b_obj.book.book_detail.save()
        #将购物车的数据清空
            for j in car_list:
                models.Shopping_car.objects.filter(sid=j).delete()

            response['title'] = "ok"
        return JsonResponse(response)

    books = models.Shopping_car.objects.filter(user=request.user).all()
    print(books)
    return  render(request,'shop_car.html',{"books":books})


def shipping_car(request,id):
    book_obj = models.Book.objects.filter(sid=id).first()
    if book_obj:
        models.Shopping_car.objects.create(user=request.user,book=book_obj)

    return redirect('/shop_car/')



def sell_book(request):
    print(request.user)
    if request.method == 'POST':
        response = {'title':None,'msg':None}
        form = Sell_bookForm(request.POST)
        if form.is_valid():
            response['title'] = form.cleaned_data.get('title')

            title = form.cleaned_data.get('title')
            price = form.cleaned_data.get('price')
            img_obj = request.FILES.get('book_img')
            if not img_obj:
                img_obj = 'book_imgs/default.jpg'
            author = form.cleaned_data.get('author')
            publish = form.cleaned_data.get('publish')
            brief = form.cleaned_data.get('brief')
            pub_time = form.cleaned_data.get('pub_time')

            #保存到数据库
            with transaction.atomic():
                book_obj = models.Book.objects.create(title=title,price=price,img=img_obj,
                                     author=author,publish=publish,brief=brief,pub_time=pub_time,
                                     user=request.user)
                models.Book_detail.objects.create(sell_book=book_obj,book_count=1)
            return redirect('/sell_in/')
        else:
            print(form.errors)
            response['msg'] = form.errors
        return JsonResponse(response)

    form = Sell_bookForm()
    return render(request,'sell_book.html',locals())





def sell_in(request):

    books = models.Book.objects.filter(user=request.user).all()
    return render(request,"sell_in.html",locals())

def sell_in_del(request,id):

    print(id)
    book_obj = models.Book.objects.filter(sid=id).first()
    if book_obj:
        models.Book.delete(book_obj)
    else:
        return HttpResponse('errror :  404 ')


    return redirect('/sell_in/')
    # return  render(request,'sell_in.html')

def sell_in_edit(request,id):
    print(id)
    print(request.user)

    if request.method == 'POST':
        response = {'title':None,'msg':None}
        form = Sell_bookForm(request.POST)
        if form.is_valid():
            response['title'] = form.cleaned_data.get('title')
            title = form.cleaned_data.get('title')
            price = form.cleaned_data.get('price')
            img_obj = request.FILES.get('book_img')
            if not img_obj:    #前端没有更改图片
                queryset_img = models.Book.objects.filter(sid=id).values('img')
                img_obj = queryset_img[0].get('img')
            else:
                img_obj = 'book_imgs/'+str(request.FILES.get('book_img'))
            author = form.cleaned_data.get('author')
            publish = form.cleaned_data.get('publish')
            brief = form.cleaned_data.get('brief')
            pub_time = form.cleaned_data.get('pub_time')
            book_obj = models.Book.objects.filter(sid=id)

            book_obj.update(title=title,price=price,img=img_obj,
                                       author=author,publish=publish,brief=brief,pub_time=pub_time,
                                       user=request.user)
            return redirect('/sell_in/')
        else:
            print(form.errors)
            response['msg'] = form.errors
        return JsonResponse(response)



    book_obj = models.Book.objects.filter(sid=id).first()
    if not book_obj:
        return HttpResponse('errror :  404 ')
    return render(request,'sell_in_edit.html',locals())


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            print("denglu",name,pwd)
            user_obj = auth.authenticate(username=name,password=pwd)
            auth.login(request,user_obj)

            return redirect('/home/')
        else:
            clean_error=form.errors.get("__all__")
            print("clean_error",clean_error)
        return render(request,'login.html',locals())
    form= LoginForm()
    return render(request,"login.html",locals())

def logout(request):
    auth.logout(request)
    return redirect('/home/')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print("cleaned_data",form.cleaned_data)
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            models.UserInfo.objects.create_user(username=name,password=pwd)
            return redirect('/login/')
        else:
            clean_error=form.errors.get("__all__")
            print("clean_error",clean_error)

        return render(request,'register.html',locals())

    form= UserForm()
    return render(request,'register.html',locals())

def my_zone(request):

    print(request.path)
    if request.path == '/my_zone/' :
        # 1.订单号
        # 2.几个商品 也就是订单详情
        # 3、图书封面  点击就是订单详情
        #根据访问的url 返回对应的数据给前端渲染
        response = {'title':None,"msg":None}
        order = models.Order.objects.filter(user=request.user).all()
        order_list = []
        for i in order:
            orderdetail_dic = {}
            detail_list = models.OrderDetail.objects.filter(order=i.pk).all()
            orderdetail_dic['order_numb']=i.order_number
            orderdetail_dic['time']=i.date
            book_list = []
            for j in detail_list:
                try:#测试的时候有删除一些数据  所以这里做了 异常捕获
                    print(j.book)
                    book_list.append(j.book)
                except :
                    continue

                # orderdetail_dic['book_id']=j.book.pk
                # orderdetail_dic['book_img'] = j.book.img
            orderdetail_dic['books']=book_list
            order_list.append(orderdetail_dic)
        return render(request,'my_zone.html',{'order_list':order_list})


    else:
        books = []
        sell_books = models.Book.objects.filter(user=request.user)
        print(sell_books)
        for book in sell_books:
            print(book)
            try :
                book.book_detail.status
                if book.book_detail.status==1:
                    print(book.book_detail.status)
                    books.append(book)
            except:
                continue




        print("books",books)




    return render(request,'my_zone.html',{'books':books})




def my_balance(request):

    return render(request,'my_balance.html')

def my_bookrack(request):
    order_list = models.OrderDetail.objects.filter(order__user=request.user).all()
    print(order_list)
    return render(request,'my_bookrack.html',{'order_list':order_list})
def info(request):
    return render(request,'my_zone_info.html')


def shopping_car_del(request,id):

    del_book = models.Shopping_car.objects.filter(sid=id).first()

    print(del_book,id)
    del_book.delete()


    return redirect('/shop_car/')


def appraise(request,book_id):
    if request.method == "POST" :
        response = {"title":None,'msg':None}
        appraise_text = request.POST.get('appraise_text')
        parent_comment = request.POST.get('parent_comment')
        print('parent_comment',parent_comment)
        comt_obj = models.Comment.objects.filter(cid=parent_comment).first()


        star_numb = request.POST.get('star_numb')
        book_obj = models.Book.objects.filter(sid=book_id).first()
        models.Comment.objects.create(parent_comment=comt_obj,content=appraise_text,book=book_obj,user=request.user,score=star_numb)
        response['title'] = True
        return JsonResponse(response)
    book = models.Book.objects.filter(sid=book_id).first()
    return render(request,'appraise.html',locals())

def diggit(request):
    if request.is_ajax():
        response = {"title":None,"msg":None}
        comment_id = request.POST.get('comment_id')
        #评论对象
        comt_obj = models.Comment.objects.filter(cid=comment_id).first()

        #根据评论对象找到点赞数量
        up_obj = models.Book_up_down.objects.filter(comment=comt_obj,user=request.user).first()
        #没有点赞对象,该用户没有对该评论点赞过
        with transaction.atomic():
            if not up_obj:
                models.Book_up_down.objects.create(comment=comt_obj,user=request.user,is_up=True)
                up_numb = comt_obj.up_count + 1
            # 有值  踩灭
            else:
                up_numb = comt_obj.up_count - 1
                up_obj.delete()


            print('up_numb',up_numb)
            comt_obj.up_count = up_numb
            comt_obj.save()
            response['title'] = str(up_numb)

        return JsonResponse(response)


def comment_reply(request,book_id,comt_id):
    book = models.Book.objects.filter(sid=book_id).first()
    comment = models.Comment.objects.filter(cid=comt_id).first()
    print('comment',comment,comment.user)
    return render(request,'comment_reply.html',locals())










