from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home_view(request):
    """Home page"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    """Dashboard - Hiển thị danh sách file"""
    from apps.documents.models import Document
    
    # Lấy tất cả documents của user
    documents = Document.objects.filter(user=request.user)
    
    # Tìm kiếm
    search_query = request.GET.get('search', '')
    if search_query:
        documents = documents.filter(
            Q(filename__icontains=search_query) |
            Q(extracted_text__icontains=search_query)
        )
    
    documents = documents.order_by('-created_at')
    
    context = {
        'documents': documents,
        'total_documents': documents.count(),
        'search_query': search_query,
    }
    return render(request, 'core/dashboard.html', context)