from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Favorite, Inquiry, Property

from .forms import ProfileForm, RegisterForm

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Ayoya Realestate. Your account is ready.")
            return redirect("dashboard:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "title": "Create account"})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username, is_active=True)
    properties = Property.objects.filter(owner=profile_user, status=Property.Status.PUBLISHED)[:12]
    return render(request, "accounts/profile.html", {"profile_user": profile_user, "properties": properties})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("dashboard:home")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form, "title": "Edit profile"})


@login_required
def dashboard(request):
    if request.user.user_type == User.USER_TYPE_AGENT:
        return redirect("dashboard:agent")
    if request.user.user_type == User.USER_TYPE_SELLER:
        return redirect("dashboard:seller")
    return redirect("dashboard:buyer")


@login_required
def agent_dashboard(request):
    properties = Property.objects.filter(owner=request.user).order_by("-created_at")
    inquiries = Inquiry.objects.filter(property__owner=request.user).select_related("property", "user")[:20]
    return render(request, "dashboard/agent.html", {"properties": properties, "inquiries": inquiries})


@login_required
def seller_dashboard(request):
    properties = Property.objects.filter(owner=request.user).order_by("-created_at")
    inquiries = Inquiry.objects.filter(property__owner=request.user).select_related("property", "user")[:20]
    return render(request, "dashboard/seller.html", {"properties": properties, "inquiries": inquiries})


@login_required
def buyer_dashboard(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("property")[:20]
    inquiries = Inquiry.objects.filter(user=request.user).select_related("property")[:20]
    return render(request, "dashboard/buyer.html", {"favorites": favorites, "inquiries": inquiries})
