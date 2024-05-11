from django.shortcuts import render, get_object_or_404,HttpResponseRedirect

from book.models import BookCategory,BookCode,BookData,BookLendRecord
from account.models import Student

from book.forms import BookDataForm

# Create your views here.
def search(request):
    try:
        books = BookData.objects.all().order_by("id")
        for book in books:
            category = BookCategory.objects.get(category_id=book.category_id)
            book.category_name = category.category_name
            status = BookCode.objects.get(code_id=book.status_id)
            book.status_name = status.code_name
            if book.keeper_id:
                keeper_name = Student.objects.get(id=book.keeper_id).username
                book.keeper_name = keeper_name
            else:
                book.keeper_name = "-"
    except:
        errormessage = "讀取錯誤"
        
    return render(request,"book/search.html",locals())

def detail(request, pk=None):
    book = get_object_or_404(BookData, pk=pk)
    return render(request, 'book/bookdata.html', locals())

def create(request):
    if request.method == "POST":
        form = (request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = BookDataForm()
    return render(request, "book/bookdata.html", locals())

def edit(request, pk=None):
    book = get_object_or_404(BookData, pk=pk)
    if request.method == "POST":
        form = BookDataForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = BookDataForm(instance=book)
    return render(request, "book/bookdata.html", locals())
    
def delete(request, pk=None):
    book = get_object_or_404(BookData, pk=pk)
    book.delete()
    return render(request, "", locals())

def lend_record(request, pk=None):
    book = get_object_or_404(BookData, pk=pk)
    records = BookLendRecord.objects.filter(book_id=pk).order_by("-id")
    for record in records:
        record.borrower_name = Student.objects.get(id=record.borrower_id).username
    return render(request, "book/lend_record.html", locals())

