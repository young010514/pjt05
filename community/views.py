from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Post
from .utils import get_asset_by_id, load_assets


def asset_list(request):
    assets = load_assets()
    context = {"assets": assets}
    return render(request, "community/asset_list.html", context)


def board(request, asset_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    posts = Post.objects.filter(asset_id=asset_id)
    context = {"asset": asset, "posts": posts}
    return render(request, "community/board.html", context)


def post_detail(request, asset_id, post_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    context = {
        "asset": asset,
        "post": post,
        "can_manage_post": request.user.is_authenticated and post.author == request.user.username,
    }
    return render(request, "community/post_detail.html", context)


@login_required(login_url="accounts:login")
@require_http_methods(["GET", "POST"])
def post_create(request, asset_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if title and content:
            Post.objects.create(
                asset_id=asset_id,
                title=title,
                content=content,
                author=request.user.username,
            )
            messages.success(request, "게시글이 등록되었습니다.")
            return redirect("community:board", asset_id=asset_id)

        messages.error(request, "제목과 내용을 모두 입력해주세요.")

    context = {"asset": asset}
    return render(request, "community/post_form.html", context)


@login_required(login_url="accounts:login")
@require_http_methods(["GET", "POST"])
def post_update(request, asset_id, post_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    if post.author != request.user.username:
        messages.error(request, "작성자 본인만 게시글을 수정할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if title and content:
            post.title = title
            post.content = content
            post.author = request.user.username
            post.save()
            messages.success(request, "게시글이 수정되었습니다.")
            return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

        messages.error(request, "제목과 내용을 모두 입력해주세요.")

    context = {
        "asset": asset,
        "post": post,
        "title": post.title,
        "content": post.content,
        "is_edit": True,
    }
    return render(request, "community/post_form.html", context)


@login_required(login_url="accounts:login")
@require_http_methods(["POST"])
def post_delete(request, asset_id, post_id):
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    if post.author != request.user.username:
        messages.error(request, "작성자 본인만 게시글을 삭제할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    post.delete()
    messages.success(request, "게시글이 삭제되었습니다.")
    return redirect("community:board", asset_id=asset_id)
