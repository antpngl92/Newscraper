from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm,  AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from account.scraper import Scraper, Source
from article.models import Article



theGuardian = Source(
    "The Guardian",
    "https://www.theguardian.com",
    ("div", "fc-item__container"),
    ("span", "js-headline-text"),
    ("div", "fc-item__standfirst"),
    ("a", "fc-item__link"),
    ("source", "srcset")
)

bbc = Source(
    "BBC",
    "https://www.bbc.co.uk/news",
    ("div", "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"),
    ("h3", "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"),
    ("p", "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"),
    ("a", "gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"),
    ("img", "src")
)

theIndependent = Source(
    "The Independent",
    "https://www.independent.co.uk",
    ("div", "article type-article media-video"),
    ("div", "headline"),
    ("", ""),
    ("a", ""),
    ("amp-img", "amp-img img-focal-center i-amphtml-layout-responsive i-amphtml-layout-size-defined i-amphtml-element i-amphtml-layout")
)

sources = []
sources.append(theGuardian)
sources.append(bbc)
sources.append(theIndependent)

categories = []
categories.append("politics")
categories.append("technology")
categories.append("sport")

def checkFavorite(request, pk=None):
    if pk:
        article = Article.objects.get(pk=pk)
        if article.favourite:
            article.favourite = False
        else:
            article.favourite = True
        article.save()

    return redirect('home')



def account_delete_done_view(request):
    return render(request, 'accounts/delete-done.html')


def account_delete_view(request):

    if request.user.is_authenticated:
        if request.method =="POST":
            user = request.user
            user.delete()
            return redirect('account-delete-done')
    else:
        return redirect('home')

    return render(request, "accounts/delete.html")

def registration(request):
    context = {}

    if request.user.is_authenticated: # If user is logged in, redirect to home screen, they cannot register again!
        return redirect('home')
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)

def favourite(request):
    context = {}
    articles_selection = []

    if request.user.is_authenticated == True:
        articles = Article.objects.filter(favourite=True)
        context['articles'] = articles

        return render(request, 'favourite.html', context)
    else:
        return redirect( '../')


### HOME VIEW ###
def home(request):
    context = {}
    source_selection = []
    categories_selection = []
    # if the user is authenticated
    if request.user.is_authenticated:
        accounts = Account.objects.filter(username=request.user).first()

        if request.user.guardianSource: source_selection.append('The Guardian')
        if request.user.bbcSource: source_selection.append("BBC")
        if request.user.independentSource: source_selection.append('The Independent')

        if request.user.categoryTech: categories_selection.append('technology')
        if request.user.categoryPolitics: categories_selection.append('politics')
        if request.user.categorySport: categories_selection.append('sport')
        context['accounts'] = accounts
    else: # if the user uses the website as a guest he will only be able to see  BBC politics category news
        source_selection.append("BBC")
        categories_selection.append("politics")

    # Extract the articles from the DB based on the filter provided
    # (user (if user - filter based on user selected sources and categories) or guess (if guess- predefined sources and categories))
    articles = Article.objects.filter(source__in=source_selection, category__in=categories_selection)

    context['articles'] = articles


    # Scrape
    scraper = Scraper(sources, categories)

    # checkRecent can take a "force-scrape" parameter to enforce the scraper to always scrape
    # if scraper.checkRecent("force-scrape"):
    if scraper.checkRecent():
        print("Scrape was recent. No scrape needed.")
    else:
        print("Scrape was not recent. Scraping...")
        scraper.search()

    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    # if user is logged in and tries to type /login it will redirect him to home
    if user.is_authenticated:
        return redirect('home')
    # else
    if request.POST:
        form = AccountAuthenticationForm(request.POST) # get the authentication form and store it in form
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'accounts/login.html', context)

def account_view(request):
    # If a guest uses the website and tryies to type /account it will redirect him to home page
    if not request.user.is_authenticated:
        return redirect('login')
    # if a register uses tries to access the /account page:
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user) # request the form of the specific instance user
        if form.is_valid(): # if the form is valid (all values are entered correctly) save the form
            form.save()
            context['success_message'] = "Updated" # This is the message to print on success
    else: # Display the saved user details from database
        form = AccountUpdateForm(
                                initial = {
                                'username':request.user.username,
                                "guardianSource": request.user.guardianSource,
                                "bbcSource": request.user.bbcSource,
                                "independentSource": request.user.independentSource,

                                "categoryTech": request.user.categoryTech,
                                "categoryPolitics": request.user.categoryPolitics,
                                "categorySport": request.user.categorySport,
                                            })
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)

# Create your views here.
