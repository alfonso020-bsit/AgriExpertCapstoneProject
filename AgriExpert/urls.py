from django.urls import path
from .views import signup
from . import views
from django.contrib.auth.decorators import login_required
from AgriExpert.views import landing, user_login, farmer_home,farmer_farmers, expert_home, admin_dashboard, user_logout, admin_reports, admin_library, admin_farmers, admin_experts, admin_profile, farmer_scan, farmer_library,farmer_experts, farmer_collab, farmer_profile,  update_expert_status, generate_expert_pdf, generate_farmer_pdf, view_expertfromfarmer, message_expert,send_message, chat_detail, edit_message, delete_message, expert_scan, expert_library, expert_experts, expert_collab, expert_profile, user_logout , view_expertfromexpert, view_farmerfromexpert , message_farmer, chat_detailexpert,edit_message_expert, delete_message_expert, expert_farmers, expert_collaboration, expert_report, mark_solved, create_expert_post, edit_expert_post, delete_expert_post_image, view_post,upvote_post, comment_post, mark_comment_as_solution, get_library_details, get_prediction_history,view_farmer_post,toggle_farmer_post_upvote,add_farmer_post_comment, expert_view_farmer_posts, expert_toggle_farmer_post_upvote, expert_add_farmer_post_comment, expert_view_farmer_post
from .views import PasswordResetRequestView, PasswordResetConfirmView
from django.shortcuts import render
from .views import convert_docx_to_pdf
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", landing, name="landing"),
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    # path("farmer/home/", farmer_home, name="farmer_home"),
    # path("expert/home/", expert_home, name="expert_home"),
    # path("adminako/dashboard/", views.adminako_dashboard, name="adminako_dashboard"),
    path("farmer/home/", farmer_home, name="farmer_home"),
    path("expert/home/", expert_home, name="expert_home"),
    path("adminako/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("logout/", user_logout, name="logout"),
    
    # admin
    path("adminako/reports/", admin_reports, name="admin_reports"),     path('adminako/libary/',views.admin_library, name='admin_library'),
    path('adminako/farmers/', admin_farmers, name='admin_farmers'),
    path('adminako/experts/', admin_experts, name='admin_experts'),
    path('adminako/profile/', admin_profile, name= 'admin_profile'),
    path("adminako/expert/<int:expert_id>/", views.view_expert, name="view_expert"),
    path('adminako/view_post_asadmin/<int:post_id>/', views.view_post_asadmin, name='view_post_asadmin'),
    path("update_expert_status/", update_expert_status, name="update_expert_status"),
    # path("adminako/expert/<int:expert_id>/edit/", views.edit_expert, name="edit_expert"),
    path("adminako/farmer/<int:farmer_id>/edit/", views.view_farmer, name="view_farmer"),
    path('convert_docx_to_pdf/', convert_docx_to_pdf, name='convert_docx_to_pdf'),
    
    
    
     # Admin Farmers URLs
    path('farmers/', views.admin_farmers, name='admin_farmers'),
    path('farmer/<int:farmer_id>/', views.admin_view_farmer, name='admin_view_farmer'),
    path('farmer-post/<int:post_id>/', views.admin_view_farmer_post, name='admin_view_farmer_post'),
    path('farmer-post/<int:post_id>/remove/', views.admin_remove_farmer_post, name='admin_remove_farmer_post'),
    
    
    
    # expert
    path("expert/scan/", expert_scan, name="expert_scan"),
    path("expert/library/", expert_library, name="expert_library"),
    path("expert/experts/", expert_experts, name="expert_experts"),
    path('view_post/<int:post_id>/', view_post, name='view_post'),
    path('upvote_post/<int:post_id>/', upvote_post, name='upvote_post'),
    path('comment_post/<int:post_id>/', comment_post, name='comment_post'),
    path('mark_solution/<int:comment_id>/', mark_comment_as_solution, name='mark_comment_as_solution'),
    path("expert/collab/", expert_collab, name="expert_collab"),
    path("expert/farmers/", expert_farmers, name="expert_farmers"),
    path("expert/collaboration/", expert_collaboration, name="expert_collaboration"),
    path("expert/collaboration/create/", create_expert_post, name="create_expert_post"),
    path('expert/collaboration/edit/<int:post_id>/', edit_expert_post, name='edit_expert_post'),
    path('delete-image/<int:image_id>/', delete_expert_post_image, name='delete_expert_post_image'),
    path('expert/report/', expert_report, name='expert_report'),
    path("expert/profile/", expert_profile, name="expert_profile"),
    path('expert/viewedit/<int:expert_id>/', view_expertfromexpert, name='view_expertfromexpert'),
    path('farmer/viewedit/<int:farmer_id>/', view_farmerfromexpert, name='view_farmerfromexpert'),
    path('chat/expert/send/<int:farmer_id>/', views.send_message_expert, name='send_message_expert'),
    path('message/farmer/<int:farmer_id>/', message_farmer, name='message_farmer'),
    path('chat/expert/<int:farmer_id>/', chat_detailexpert, name='chat_detailexpert'),
    # views.
    path("edit_message_expert/<int:message_id>/", edit_message_expert, name="edit_message_expert"),
    # views.
    path("delete_message_expert/<int:message_id>/", delete_message_expert, name="delete_message_expert"),
    path("chat/mark-solved/<int:message_id>/", mark_solved, name="mark_solved"),
    # path("chat/mark-solved/<int:farmer_id>/", mark_solved, name="mark_solved"),
    
    
    
    # farmer
    path('farmer/scan/', farmer_scan, name='farmer_scan'),
    path('farmer/library/', farmer_library, name='farmer_library'),
      path('get-library/<str:paksa>/', get_library_details, name='get_library'),
    path('farmer/experts/', farmer_experts, name='farmer_experts'),
    path('farmer/farmers/', farmer_farmers, name='farmer_farmers'),
    
    path('farmer/post/<int:post_id>/', view_farmer_post, name='view_farmer_post'),
    path('farmer/post/<int:post_id>/upvote/', toggle_farmer_post_upvote, name='toggle_farmer_post_upvote'),
    path('farmer/post/<int:post_id>/comment/', add_farmer_post_comment, name='add_farmer_post_comment'),
    
    path('expert/farmer-posts/', expert_view_farmer_posts, name='expert_view_farmer_posts'),
    path('expert/farmer-post/<int:post_id>/upvote/', expert_toggle_farmer_post_upvote, name='expert_toggle_farmer_post_upvote'),
    path('expert/farmer-post/<int:post_id>/comment/', expert_add_farmer_post_comment, name='expert_add_farmer_post_comment'),
    path('expert/farmer-post/<int:post_id>/',expert_view_farmer_post, name='expert_view_farmer_post'),

    path('farmer/collab/', farmer_collab, name='farmer_collab'),
    path('farmer/collab/chat/<int:expert_id>/', chat_detail, name='chat_detail'),
    path('farmer/profile/', farmer_profile, name='farmer_profile'),
    path("farmer/collaboration/", views.farmer_collaboration, name="farmer_collaboration"),
    path('farmer/create-post/', views.create_farmer_post, name='create_farmer_post'),
    path('farmer/collaboration/edit/<int:post_id>/', views.edit_farmer_post, name='edit_farmer_post'),
    path('experts/<int:expert_id>/', view_expertfromfarmer, name='view_expertfromfarmer'),
    path('farmer/view_post/<int:post_id>/', view_post, name='farmer_view_post'),
    # path('message/<int:expert_id>/', message_expert, name='message_expert'),
    path("message/expert/<int:expert_id>/", send_message, name="send_message"),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('predict_disease/', views.predict_disease, name='predict_disease'),
    path("upload_to_supabase_and_save/", views.upload_to_supabase_and_save, name="upload_to_supabase_and_save"),
    path('predict_pest/', views.predict_pest_image, name='predict_pest'),
    path('save_pest_prediction/', views.save_pest_prediction, name='save_pest_prediction'),
    path('get_prediction_history/', views.get_prediction_history, name='get_prediction_history'),

    #  reset
    path('reset_password/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset_password/confirm/<str:role>/<str:email>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/done/', lambda request: render(request, 'email/password_reset_done.html'), name='password_reset_done'),
    path('reset_password/complete/', lambda request: render(request, 'email/password_reset_complete.html'), name='password_reset_complete'),
    
    
    # print
    path('generate_expert_pdf/', generate_expert_pdf, name='generate_expert_pdf'),
    path('generate_farmer_pdf/', generate_farmer_pdf, name='generate_farmer_pdf'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
