from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Post


# Create your views here.
def index(request):
    # saving newly created post
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        category_id = request.POST["category_id"]
        image = request.FILES.get("image")

        post = Post(
            title=title,
            content=content,
            author=request.user,
            category=Category.objects.get(id=category_id),
        )
        # Only set the image if it is provided
        if image:
            post.image = image
        # Save the post object
        post.save()
        return redirect("index")

    # searching
    q = request.GET.get("q")
    if q is not None:
        posts = Post.objects.filter(title__icontains=q)
        categories = (
            Category.objects.all()
        )  # for displaying categories in 'add new post' form
        context = {"posts": posts, "categories": categories}
        return render(request, "blog/index.html", context)

    # displaying existing posts/blog
    posts = Post.objects.all()
    categories = (
        Category.objects.all()
    )  # for displaying categories in 'add new post' form
    context = {"posts": posts, "categories": categories}
    return render(request, "blog/index.html", context)


def register(request):
    # registering/creating a new user
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        if password == cpassword:
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already exists")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=email,
                    password=password,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                )
                user.save()
                return redirect("login")
        else:
            messages.error(request, "Passwords doesn't match")
            return redirect("register")
    return render(request, "blog/register.html")


def login_page(request):
    # loging in a user
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect("login")
    return render(request, "blog/login.html")


def logout_user(request):
    # loging out a user
    logout(request)
    return redirect("index")


@login_required(login_url="/login")
def profile(request):
    my_posts = Post.objects.filter(author=request.user)
    context = {"posts": my_posts}
    return render(request, "blog/profile.html", context)


@login_required(login_url="/login")
# vieng single blog page
def blog_single(request, pk):
    try:
        post = Post.objects.get(id=pk)
        context = {"post": post}
        return render(request, "blog/blog-single.html", context)
    except Post.DoesNotExist:
        return redirect("error")


@login_required(login_url="/login")
# editing a blog
def edit_blog(request, pk):
    try:
        # fetching existing values
        post = Post.objects.get(id=pk)
        categories = Category.objects.all()
        context = {"post": post, "categories": categories}

        # inserting updated content
        if request.method == "POST":
            post.title = request.POST["title"]
            post.content = request.POST["content"]
            post.category = Category.objects.get(id=request.POST["category_id"])
            image = request.FILES.get("image")

            # Only set the image if it is provided
            if image:
                post.image = image
            # Save the post object
            post.save()
            return redirect("index")
        return render(request, "blog/edit-blog.html", context)

    except Post.DoesNotExist:
        return redirect("error")


@login_required(login_url="/login")
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        # Update first name if provided
        if fname:
            user.first_name = fname

        # Update last name if provided
        if lname:
            user.last_name = lname

        # Update email if provided and different from the current one
        if email and email != user.username:
            if User.objects.filter(usernmae=email).exists():
                messages.error(request, "Email already exists")
                return redirect("profile")
            else:
                user.email = email
                user.username = email

        # Update password if provided and matches the confirmation
        if password:
            if password == cpassword:
                user.set_password(password)
            else:
                messages.error(request, "Passwords don't match")
                return redirect("profile")

        # Save the updated user details
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")


def error_page(request):
    return render(request, "blog/error.html")


def delete(request, pk):
    # deleting a post
    try:
        post = Post.objects.get(id=pk)
        if post.author != request.user:
            return redirect("error")
        post.delete()
        return redirect("index")
    except Post.DoesNotExist:
        return redirect("error")
