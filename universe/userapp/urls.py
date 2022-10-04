from django.urls import re_path
from django.views.generic import TemplateView
from universe.userapp import views as user_view

urlpatterns = [
    re_path('edit_otheruser_profile/(?P<user_id>\d+)/', user_view.editUserProfile , name='edit_otheruser_profile'),
    re_path('user_profile/(?P<user_id>\d+)/', user_view.updateUserProfile , name='user_profile'),
    re_path('edit_profile', user_view.editMyProfile , name='edit_profile'),
    re_path('my_profile', user_view.myProfile , name='my_profile'),
    re_path('deactivate/(?P<user_id>\d+)/', user_view.deactivateUser , name='deactivate'),
    re_path('manage_staff', user_view.manageStaff , name='manage_staff'),
    re_path('manage_customer', user_view.manageCustomer , name='manage_customer'),

]
