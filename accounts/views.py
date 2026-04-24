from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from community.models import Post
from community.utils import load_assets

from .forms import CustomPasswordChangeForm, LoginForm, ProfileUpdateForm, SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("community:asset_list")

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data["password1"],
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
            return redirect("community:asset_list")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required(login_url="accounts:login")
def profile(request):
    asset_name_map = {
        asset.get("id"): asset.get("name")
        for asset in load_assets()
        if asset.get("id") and asset.get("name")
    }
    interest_stock_names = [
        asset_name_map.get(stock_id, stock_id)
        for stock_id in request.user.interest_stocks
    ]
    my_posts = Post.objects.filter(author=request.user.username)

    context = {
        "profile_user": request.user,
        "interest_stock_names": interest_stock_names,
        "my_posts": my_posts,
    }
    return render(request, "accounts/profile.html", context)


@login_required(login_url="accounts:login")
def edit_profile(request):
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect("accounts:profile")
        messages.error(request, "프로필 정보를 다시 확인해주세요.")
    else:
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"profile_form": profile_form})


@login_required(login_url="accounts:login")
@require_http_methods(["POST"])
def delete_account(request):
    confirmation = request.POST.get("confirmation_text", "").strip()
    if confirmation != "회원탈퇴":
        messages.error(request, "'회원탈퇴'를 정확히 입력해야 탈퇴할 수 있습니다.")
        return redirect("accounts:profile")

    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "회원탈퇴가 완료되었습니다.")
    return redirect("community:asset_list")


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("community:asset_list")


class CustomLogoutView(LogoutView):
    next_page = "community:asset_list"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"
