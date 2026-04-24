from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeDoneView,
    CustomPasswordChangeView,
    delete_account,
    edit_profile,
    profile,
    signup,
)

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="profile_edit"),
    path("delete/", delete_account, name="delete"),
    path("password/change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path(
        "password/change/done/",
        CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
