from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

from tracker.models import Training_Program, Training_Session, Exercise, Training_Session_Exercise
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
    program = get_object_or_404(Training_Program, id=program_id, user=request.user)
    
    # 1. Get or create the current active session
    session, created = Training_Session.objects.get_or_create(
        training_program=program,
        completed_at__isnull=True,
        defaults={'started_at': timezone.now()},
    )

    # 2. Pre-create Training_Session_Exercise logs for this session if they don't exist yet
    exercises = Exercise.objects.filter(training_program=program)
    for exercise in exercises:
        # Optional: Prefill the next session by fetching the user's last completed values
        last_log = Training_Session_Exercise.objects.filter(
            exercise=exercise,
            training_session__completed_at__isnull=False
        ).order_by('-training_session__completed_at').first()

        defaults = {
            'title': exercise.title,
            'sets': last_log.sets if last_log else 3,       # Fallback to 3 sets
            'reps': last_log.reps if last_log else 10,      # Fallback to 10 reps
            'weight': last_log.weight if last_log else 0.0, # Fallback to 0.0 kg
        }

        # get_or_create ensures we don't make duplicates if they reload the page
        Training_Session_Exercise.objects.get_or_create(
            training_session=session,
            exercise=exercise,
            defaults=defaults
        )

    # 3. Use the Training_Session_Exercise queryset for the formset
    queryset = Training_Session_Exercise.objects.filter(
        training_session=session,
        exercise__in=exercises  # Keeps active exercises even if some were removed from the program
    )

    if request.method == 'POST':
        formset = Session_Form_Set(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()  # This updates the Training_Session_Exercise records in the database

            # Mark session as finished
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
def session_history(request):
    sessions = (
        Training_Session.objects
        .filter(training_program__user=request.user, completed_at__isnull=False)
        .select_related('training_program')
        .order_by('-completed_at')
    )
    return render(request, 'tracker/session_history.html', {'sessions': sessions})


def session_detail(request, session_id):
    session = get_object_or_404(
        Training_Session.objects.select_related('training_program'),
        id=session_id,
        training_program__user=request.user,   # blocks viewing another user's session by URL guessing
    )
    exercise_logs = session.exercise_logs.all()

    return render(request, 'tracker/session_detail.html', {
        'session': session,
        'exercise_logs': exercise_logs,
    })


def delete_session(request, session_id):
    session = get_object_or_404(Training_Session, id=session_id, training_program__user=request.user)
        
    if request.method == 'POST':
        session.delete()
        messages.success(request, f'session "{session}" deleted!')
        return redirect('session_history')
    return redirect('session_history')


@login_required
def edit_profile(request):
   pass