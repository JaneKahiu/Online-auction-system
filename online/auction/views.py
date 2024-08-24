
from typing import Required
from django.shortcuts import render,redirect, get_object_or_404
from .models import AuctioningListing, Category
from django.utils import timezone
from .forms import AuctioningListingForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Bid

# Create your views here.
def homepage(request):
    active_auctions = AuctioningListing.objects.filter(end_date__gt=timezone.now())
    return render(request, 'homepage.html' , {'active_auctions': active_auctions})



@login_required
def create_auction_view(request):
    if request.method == 'POST':
        form = AuctioningListingForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user  # Assign the logged-in user as the owner
            auction.save()
            return redirect('homepage')  # Redirect to homepage after saving
    else:
        form = AuctioningListingForm()  # Instantiate an empty form

    return render(request, 'create-auction.html', {'form': form})
    
def auction_detail_view(request, auction_id):
    auction = get_object_or_404(AuctioningListing, id=auction_id)
    if request.method == 'POST':
        form =AuctioningListingForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user
            if bid.bid_amount > auction.current_bid:
                bid.save()
                auction.current_bid = bid.bid_amount
                auction.save()
                return HttpResponseRedirect(reverse('auction_detail', args=[auction.id]))
    else:
        form = AuctioningListingForm()
    return render(request, 'auction_detail.html', {'auction': auction, 'form': form})

#my auction views
@login_required
def my_auctions_views(request):
    my_auctions = AuctioningListing.objects.filter(owner=request.user)
    return render(request, 'myauctions.html' ,{'auctions':my_auctions})


            
#login page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to the homepage after successful login
        else:
            messages.error(request, 'Invalid credentials')  # Display error message for invalid credentials
        
    return render(request, 'login.html')
#register page


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'message': 'Username already exists'})

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'message': 'Email already exists'})

        # Check if the passwords match
        if password == confirm_password:
            try:
                # Create the new user
                user = User.objects.create_user(username=username, email=email, password=password)
                # Log the user in
                login(request, user)
                return redirect('homepage')
            except Exception as e:
                # Handle unexpected errors (e.g., database issues)
                return render(request, 'register.html', {'message': f'Error creating account: {str(e)}'})
        else:
            return render(request, 'register.html', {'message': 'Passwords do not match'})

    return render(request, 'register.html')

#logout page
def logout_view(request):
    logout(request)
    return redirect('homepage')

#edit auction view
def edit_auction_view(request, auction_id):
    auction = get_object_or_404(AuctioningListing, id=auction_id)
    if request.method == 'POST':
        form = AuctioningListingForm(request.POST, request.FILES, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('auction_detail', auction_id=auction.id) 
    else:
        form = AuctioningListingForm(instance=auction)
    return render(request, 'edit_auction.html', {'form': form, 'auction': auction})
#delete auction view

def delete_auction_view(request, auction_id):
    auction = get_object_or_404(AuctioningListing, id=auction_id)
    if request.method == 'POST':
        auction.delete()
        return redirect('my_auctions')

#bid history view
def bid_history_view(request, auction_id):
    auction = get_object_or_404(AuctioningListing, id=auction_id)
    bids = Bid.objects.filter(auction=auction).order_by('-bid_time')
    return render(request, 'bid_history.html', {'auction': auction, 'bids': bids})
     