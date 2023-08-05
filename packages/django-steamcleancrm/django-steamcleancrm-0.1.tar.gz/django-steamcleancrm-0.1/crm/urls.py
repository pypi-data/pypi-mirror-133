from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('lead/search/', views.lead_search_results, name='lead-search-results'),
    path('closed-work-orders/', views.closed_work_orders, name='closed-work-orders'),
    path('lead/new/', views.LeadCreateView.as_view(), name='create-lead'),
    path('lead/<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('lead/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('lead/<int:pk>/work-order/new/', views.WorkOrderCreateView.as_view(), name='create-work-order'),
    path('lead/<int:lead_id>/work-order/<int:pk>/', views.WorkOrderDetailView.as_view(), name='work-order-detail'),
    path('lead/<int:lead_id>/work-order/<int:pk>/update/', views.WorkOrderUpdateView.as_view(), name='work-order-update'),
    path('lead/<int:lead_id>/work-order/<int:pk>/technician/new/', views.AddTechnicianView.as_view(), name='add-technician-to-work-order'),
    path('lead/<int:lead_id>/work-order/<int:workorder_id>/technician/<int:pk>/delete', views.RemoveTechnicianView.as_view(), name='remove-technician-from-work-order'),
    path('lead/<int:lead_id>/work-order/<int:pk>/image/new/', views.AddImageView.as_view(), name='add-image-to-work-order'),
    path('lead/<int:lead_id>/work-order/<int:workorder_id>/image/<int:pk>/delete', views.RemoveImageView.as_view(), name='remove-image-from-work-order'),
    
]
