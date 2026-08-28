from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

from tracker.models import Training_Program, Training_Session
from tracker.forms import Program_Model_Form, Exercise_Form_Set, Session_Form_Set


def home_page(request):
    return render(request, 'tracker/home.html')


@login_required
def dashboard_page(request):
    now = timezone.now()
    this_month_sessions_count = Training_Session.objects.filter(
        date_added__year=now.year,
        date_added__month=now.month
    ).count()
    training_programs = Training_Program.objects.all().filter(user=request.user)
    sessions_count = Training_Session.objects.all().count()
    last_session = Training_Session.objects.all().order_by('date_added').last()
    last_session_day = last_session.date_added if last_session else None
    

    return render(request, 'tracker/dashboard.html',{
        'training_programs': training_programs,
        'sessions_count': sessions_count,
        'this_month_session_count': this_month_sessions_count,
        'last_session_day': last_session_day
        })


@login_required
def add_program_page(request):
    if request.method == "POST":
        program_form = Program_Model_Form(request.POST)
        exercise_form_set = Exercise_Form_Set(request.POST)

        if program_form.is_valid() and exercise_form_set.is_valid():
            with transaction.atomic():
                program = program_form.save(commit=False)
                program.user = request.user
                program.save()

                exercise_form_set.instance = program
                exercise_form_set.save()

            return redirect('dashboard')
        else:
            messages.error(request, 'Training program creation failed')
    else:
        program_form = Program_Model_Form()
        exercise_form_set = Exercise_Form_Set()

    return render(request, 'tracker/add_program.html', {
        'program_form': program_form,
        'exercise_form_set': exercise_form_set,
    })


@login_required
def update_program(request, program_id):
    program = get_object_or_404(Training_Program, id=program_id, user=request.user)

    if request.method == "POST":
        program_form = Program_Model_Form(request.POST, instance=program)
        exercise_form_set = Exercise_Form_Set(request.POST, instance=program)

        if program_form.is_valid() and exercise_form_set.is_valid():
            with transaction.atomic():

                program_form.save()
                exercise_form_set.save()

            return redirect("dashboard")
        
    else:

        program_form = Program_Model_Form(
            instance=program,
        )

        exercise_form_set = Exercise_Form_Set(
            instance=program,
        )

    return render(
        request,
        "tracker/add_program.html",
        {
            "program_form": program_form,
            "exercise_form_set": exercise_form_set,
            "program": program,
            "is_update": True,
        },
    )

@login_required
def delete_program(request, program_id):
    # Only get program if it belongs to current user
    program = get_object_or_404(Training_Program, id=program_id, user=request.user)
    
    if request.method == 'POST':
        program.delete()
        messages.success(request, f'Program "{program.title}" deleted!')
        return redirect('dashboard')
    
    return redirect('dashboard')


@login_required
def start_session(request, program_id):
    program = get_object_or_404(Training_Program, id=program_id)
    queryset = program.exercise_set.all()

    # Reuse an already-started, not-yet-finished session (e.g. user refreshed the page)
    # instead of creating a new one every time they load this page.
    session, _ = Training_Session.objects.get_or_create(
        training_program=program,
        completed_at__isnull=True,
        defaults={'started_at': timezone.now()},
    )

    if request.method == 'POST':
        formset = Session_Form_Set(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            session.completed_at = timezone.now()
            session.save()
            messages.success(request, f'"{program.title}" session saved.')
            return redirect('dashboard')
    else:
        formset = Session_Form_Set(queryset=queryset)

    return render(request, 'tracker/start_session.html', {
        'program': program,
        'formset': formset,
        'session': session,
    })


@login_required
def edit_profile(request):
   pass