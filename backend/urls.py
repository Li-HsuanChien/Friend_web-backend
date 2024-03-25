from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static, serve
from django.urls import re_path, include
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from friend_web import views
import friend_web.views
from django.conf import settings


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'data', views.UserdataViewSet)
# router.register(r'connection', views.ConnectionViewSet)

urlpatterns = [
    #re_path(r'^(?P<path>.*)$', serve, { 'document_root': settings.FRONTEND_ROOT}),
    # path('', include(router.urls)),
    #path('api/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
    #returns all userdatas(admin restricted)
    path('api/adminonly/userdatas', friend_web.views.UserDataList.as_view()),

    #returns current logined user name and id {"username": {}, "id": {}}
    path('api/currentuser', friend_web.views.CurrentUser.as_view()),
	#returns targeted user username and id using username
    path('api/targetuser', friend_web.views.TargetUser.as_view()),
    #returns all userdata that contains search substring
    path('api/search', friend_web.views.SearchUserName.as_view()),

    #returns user data by inputing user_id
    path('api/userdata', friend_web.views.TargetUserData.as_view()),
    #add current user userdata
    path('api/userdatas/add', friend_web.views.UserCreate.as_view()),
    #update current user userdata
    path('api/userdatas/update', friend_web.views.CurrentUserRetrieveUpdateDestroy.as_view()),

    #takes 'user_id' and get user's activated connections
    path('api/connections/activated', friend_web.views.ConnectionListActivated.as_view()),
	#takes 'user_id' and get user's pending(activated False) connections
    path('api/connections/pending', friend_web.views.ConnectionListPending.as_view()),
    #adds connection by getting "closeness, "inviter(id)", inviter is the current user
    path('api/connections/add', friend_web.views.ConnectionCreate.as_view()),
    #edits(takes nickname and closeness) single self connection or destroy
    path('api/connections/self', friend_web.views.ConnectionRetrieveUpdateDestroy.as_view()),

    #login url takes username and pass returns jwt bearer token
    path('api/login', friend_web.views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    #returns Token refreshview
    path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    #register takes username pass pass2
    path('api/register', friend_web.views.RegisterView.as_view(), name='auth_register'),
    #send user password reset link takes data email
    path('api/forgotpassword', friend_web.views.SendPasswordResetEmail.as_view(), name='send_reset_link'),
	#takes password, password1, passwordresettoken
    path('api/resetpassword', friend_web.views.ResetPassword.as_view(), name='auth_change_password'),
    #change password consider email or two-auth
    path('api/change_password/<int:pk>/', friend_web.views.ChangePasswordView.as_view(), name='auth_change_password'),
    #black list jwt token
    path('api/logout', friend_web.views.LogoutView.as_view(), name='auth_logout'),
    #get user's email confirmation status takes request.user
    path('api/verifystatus', friend_web.views.GetEmailConfirmationStatus.as_view(), name='get_email_confirmation_status'),
    #send user confirmation email takes request.user
    path('api/sendverifyemail', friend_web.views.SendEmailConfirmationToken.as_view(), name='send_email_confirmation_token'),
	#verify account email takes token from body
    path('api/confirm', friend_web.views.ConfirmEmailView.as_view(), name='confirm_email_confirmation_token'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

