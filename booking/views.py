from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect


from django.http import HttpResponse
from .models import Booking, Department, Day

import datetime


def calculate_overbooking(date):
    # check overbooking
    max_people = Day.objects.filter(day__lt=date).order_by("-day")
    if max_people.count() > 0:
        maxp = max_people.first()
    else:
        maxp = settings.MAX_CAPACITY


def make_capacity(day, max_capacity):
    if max_capacity == -1:
        dday = Day.objects.create(day=day)
    else:
        dday = Day.objects.create(day=day, max_capacity=max_capacity)
    dday.save()


def create_day_structure(calendar, day, username, append=True):
    if not Day.objects.filter(day=day.strftime("%Y%m%d")):
        make_capacity(day.strftime("%Y%m%d"), -1)
    capacity = Day.objects.filter(day=day.strftime("%Y%m%d")).first()
    booked = Booking.objects.filter(day=day.strftime(("%Y%m%d")))
    if booked.filter(user=username.username).count() != 0:
        present = "booked"
    else:
        present = ""
    count = booked.count()
    details = capacity.max_capacity - count
    count = count * 100 / capacity.max_capacity
    if count >= 50:
        color = "yellow"
        if color == 100:
            color = "red"
    else:
        color = "green"
    info = {
        "id": day.strftime("%Y%m%d"),
        "date": day.strftime("%d-%m-%Y"),
        "name": day.day,
        "status": color,
        "details": details,
        "present": present,
        "wd": day.weekday(),
    }
    if append == True:
        calendar.append(info)
    else:
        calendar.insert(0, info)


def create_calendar(cal, day, username):
    nextm = (day + datetime.timedelta(days=32)).replace(day=1)
    if day.weekday() != 0:
        prevday = day - datetime.timedelta(days=1)
        create_day_structure(cal, prevday, username)
        while prevday.weekday() != 0:
            prevday = prevday - datetime.timedelta(days=1)
            create_day_structure(cal, prevday, username, False)
    while day.month != nextm.month:
        create_day_structure(cal, day, username)
        day = day + datetime.timedelta(days=1)
    while day.weekday() != 6:
        create_day_structure(cal, day, username)
        day = day + datetime.timedelta(days=1)
    create_day_structure(cal, day, username)


@login_required
def book(request):
    months = []
    bookings = []
    nextbookings = []
    today = datetime.datetime.now()
    if "id" in request.GET:
        try:
            today = datetime.datetime.strptime(request.GET["id"], "%Y%m%d")
        except Exception as e:
            print(e)
    firstdom = today.replace(day=1)
    create_calendar(bookings, firstdom, request.user)
    months.append([today.strftime("%B"), today.year, bookings])
    nextm = (firstdom + datetime.timedelta(days=32)).replace(day=1)
    prevm = (firstdom - datetime.timedelta(days=15)).replace(day=1)
    context = {
        "months": months,
        "prev": prevm.strftime("%Y%m%d"),
        "next": nextm.strftime("%Y%m%d"),
    }
    return render(request, "booking.html", context)


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y%m%d")
        return date_text
    except ValueError:
        print("Incorrect data format, should be YYYYMMDD")
        return datetime.datetime(1970, 1, 1)


@login_required
def pubsub(request):
    if request.method == "POST":
        if "day" in request.POST:
            booked = validate(request.POST["day"])
            username = request.user
            booking = Booking.objects.filter(day=booked, user=username.username)
            if booking.count() > 0:
                booking.delete()
            else:
                overbooking = calculate_overbooking(booked)
                if not overbooking:
                    booking = Booking.objects.create(day=booked, user=username.username)
                    booking.save()
    #return redirect("book")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

