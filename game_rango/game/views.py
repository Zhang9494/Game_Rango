from django.shortcuts import render
from game.models import Category, Game, UserProfile
from game.forms import CategoryForm, GameForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Function for the home Page
def index(request):
    # Show the 3 games with biggest mark. In other words, most 3 favorable game.
    game_list = Game.objects.order_by('-mark')[:3]
    context_dict = {'games': game_list}

    return render(request, 'game/index.html',context=context_dict)

# Function for the about Page
def about(request):
    return render(request, 'game/about.html')

# Function for show one category
def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Get the category through slug
        category = Category.objects.get(slug=category_name_slug)
        # Get the games belong to this category
        games = Game.objects.filter(category=category)
        context_dict['games'] = games
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['games'] = None

    return render(request,'game/category.html', context_dict)

# Function for add a new category. login required.
@login_required
def add_category(request):
    # Use this form to get the input
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # success then turn to the list of category page.
            return redirect('list_category')
        else:
            print(form.errors)

    return render(request, 'game/add_category.html', {'form': form})

# Function for add a new game. login required.
@login_required
def add_game(request, category_name_slug):
    # Get the category, the add_game.html will use this to decide what to show
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # This page include input, use this form to get input
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                game = form.save(commit=False)
                game.category = category
                game.mark = 0
                game.save()
                # Success, turn to the category page(which we are add game to)
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'game/add_game.html', context_dict)

# Function for register.
def register(request):
    # use this to decide what to show in html
    registered = False
    # get the user input
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # Save data
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'game/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

# Function for login.
def user_login(request):
    # get the input
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check authentication
        user = authenticate(username=username, password=password)
        if user:
            # check if the account is active
            if user.is_active:
                login(request,user)
                # login then return to the home page
                return HttpResponseRedirect(reverse('index'))
            else:
                # use login_failed.html to show what goes wrong
                context_dict = {'message': "Your account is not active!"}
                return render(request, 'game/login_failed.html', context_dict)
        else:
            # use login_failed.html to show what goes wrong
            print("Invalid login details: {0}, {1}".format(username, password))
            context_dict = {'message': "Wrong username or password!"}
            return render(request, 'game/login_failed.html', context_dict)
    else:
        return render(request, 'game/login.html',{})

# Function for logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Function for list all the category. The category page.
def list_category(request):
    category_list = Category.objects.order_by('name')
    context_dict = {'categories': category_list}

    return render(request, 'game/list_category.html', context=context_dict)

# Function for show a game.
@login_required
def show_game(request, game_name_slug):
    context_dict = {}
    # get the game and relevant data
    try:
        game = Game.objects.get(slug=game_name_slug)
        category = game.category
        context_dict['game'] = game
        context_dict['category'] = category
    except Game.DoesNotExist:
        context_dict['game'] = None
        context_dict['category'] = None

    return render(request, 'game/game.html', context_dict)

# Function for the user profile page
@login_required
def profile(request, username):
    # get the user, if not exist(not login), redirect to the home page.
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    # create form to get the input data(The picture of avatar)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'game/profile.html',
                  {'userprofile': userprofile, 'thisuser': user, 'form': form})

# Function for jQuery(Ajax), update the mark of game and return.
@login_required
def like_game(request):
    game_id = None
    if request.method == 'GET':
        game_id = request.GET['game_id']
    likes = 0
    if game_id:
        game = Game.objects.get(id=int(game_id))
        if game:
            likes = game.mark + 1
            game.mark = likes
            game.save()
    return HttpResponse(likes)


