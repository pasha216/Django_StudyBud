from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Room, Topic, Message

from .forms import RoomForm

from django.http import HttpResponse


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Does Not Exist, Or Password Is Wrong.")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    context = {"page": "login"}
    return render(request, "base/login_register.html", context)


def logout_page(request):
    logout(request)
    return redirect("home")


def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "User Created Successfully!")
            return redirect("home")
        else:
            messages.error(request, "An Error Occured")
    context = {"page": "register", "form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))
    topics = Topic.objects.all()
    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))
    rooms_count = rooms.count()
    context = {
        "rooms": rooms,
        "topics": topics, 
        "room_messages":room_messages,
        "rooms_count": rooms_count,}

    return render(request, "base/pages/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        room.save()
        return redirect("room", pk=room.id)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by("-created")
    context = {"room": room, "room_messages": room_messages, 'participants':participants}

    return render(request, "base/pages/room.html", context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    # room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'user': user,
        'rooms':rooms,
        'topics':topics,
        'room_messages':room_messages
        }
    return render(request, 'base/pages/profile.html', context)


@login_required(login_url="/login/")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect("home")
    context = {"form": form, 'page':'create'}
    return render(request, "base/room_form.html", context)



class CustomUserForm(UserChangeForm):
    password = forms.CharField(
        required=True,  # now it's required
        widget=forms.PasswordInput,
        help_text="Enter a new password"
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            # Use Django's built-in password validators
            validate_password(password, self.instance)
            return password
        raise ValidationError("Password cannot be empty")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



# View
@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Optional: only allow users to edit themselves
    if request.user != user:
        messages.error(request, "You cannot edit another user.")
        return redirect("home")

    form = CustomUserForm(instance=user)

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            userdata = form.save()
            login(request, userdata)  # keep user logged in if password changed
            messages.success(request, "User Updated Successfully!")
            return redirect("home")
        else:
            messages.error(request, form.errors)

    context = {"page": "update", "form": form}
    return render(request, "base/login_register.html", context)


@login_required(login_url="/login/")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")
    context = {"form": form, 'page':'update'}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login/")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"type":"room", "obj": room})


@login_required(login_url="/login/")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        message.delete()
        return redirect(f"/room/{message.room.id}")

    return render(request, "base/delete.html", {"type":"message", "obj": message})
