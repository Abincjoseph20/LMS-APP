from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import  Teacher,Teacher_ProfilePermission,Categories,Instructor,Levels,Language,Course,VideoModel,UserCourses
from adminapp.models import Account
from .forms import Teacher_ProfilePermissionForm,CategoryForm,InstructorForm,LevelForm,LanguageForm,CourseForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_roles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models.expressions import Case, Func, Star, Value, When
from django.core.exceptions import FieldError, FullResultSet
from django.db.models.functions.mixins import (
    FixDurationInputMixin,
    NumericOutputFieldMixin,
)



def assign_teacher_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  
    teacher = get_object_or_404(Teacher, user=account)

    if request.method == "POST":
        form = Teacher_ProfilePermissionForm (request.POST)
        if form.is_valid():
            permissions, created = Teacher_ProfilePermission.objects.get_or_create(teacher=teacher)
            
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('teacher_success_page', user_id=user_id)  # Redirect to teacher success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
        form = Teacher_ProfilePermissionForm (instance=existing_permissions)

    return render(request, 'teacher/teacher_roles_form.html', {'form': form, 'user': teacher})

def teacher_success(request, user_id=None):
    teacher = None
    permissions = None

    if user_id:
        account = get_object_or_404(Account, id=user_id)
        teacher = get_object_or_404(Teacher, user=account)
        permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    return render(request, 'teacher/assign_permisssion.html', {
        'user': teacher,
        'permissions': permissions
    })





@login_required
def profile_edit(request):
    user = request.user

    # Get the teacher object for the logged-in user
    teacher = get_object_or_404(Teacher, user=user)
    # Get the teacher's permissions
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    # Check edit permission
    if not permissions or not permissions.can_edit:
        messages.error(request, "You do not have permission to edit this profile.")
        return redirect('profile_view')

    if request.method == 'POST':
        # Update fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('teacher_profile_edit')

    return render(request, 'teacher/teacher_profile.html', {'user': user})


@login_required
def profile_delete(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.can_delete:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')

    if request.method == "POST":
        # Check if the confirmation checkbox is checked
        if 'confirm_delete' in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('register')  # Redirect to home or login page
        else:
            messages.error(request, "Please confirm the deletion before proceeding.")
            return redirect('profile_view')

    return render(request, 'confirm_delete.html', {'user': user})


#category

@login_required
@allowed_roles(['admin_and_instructor'])
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            category, created = Categories.objects.get_or_create(
                name=form.cleaned_data['name'],
                defaults={'icon': form.cleaned_data['icon']}
            )
            if created:
                messages.success(request, "Category added successfully!")
            else:
                messages.info(request, "Category already exists.")
            return redirect('category_list')
    else:
        form = CategoryForm()
        if request.user.roles == 'Teacher':
            template_name = 'teacher/add_category.html'
        else:
            template_name = 'admin/add_category.html'
            
    return render(request, template_name, {'form': form})



@login_required
@allowed_roles(['admin_and_instructor'])   #for restricting student
def category_list(request):
    categories = Categories.objects.all()
    if request.user.roles == 'Teacher':
        template_name = 'teacher/category_list.html'
    else:
        template_name = 'admin/category_list.html'
    
    return render(request, template_name, {'categories': categories})


@login_required
@allowed_roles(['admin_and_instructor'])
def update_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)  # Fetch the category object
    if request.method == 'POST':
        # Initialize the form with POST data, FILES, and bind it to the category instance
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()  # Save the updated data to the database
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        # Pre-fill the form with the current category instance
        form = CategoryForm(instance=category)
        if request.user.roles == 'Teacher':
            template_name = 'teacher/update_category.html'
        else:
            template_name = 'admin/update_category.html'
    return render(request, template_name, {'form': form, 'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('category_list')




@login_required
def create_instructor(request):
    if request.method == 'POST':
        # Check if the logged-in user already has an Instructor profile
        if Instructor.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an instructor profile.")
            return redirect('create_instructor')  # Replace with your desired page

        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.user = request.user 
            instructor.save()
            messages.success(request, "Instructor profile created successfully!")
            return redirect('InstructorListView') 
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('create_instructor')
    else:
        form = InstructorForm()

    return render(request, 'teacher/teacher_form.html', {'form': form})

class InstructorListView(LoginRequiredMixin, ListView):
    model = Instructor
    template_name = 'teacher/teacher_details.html'
    context_object_name = 'instructor'
    paginate_by = 10

    def get_queryset(self):
        # Filter instructors based on the logged-in user
        return Instructor.objects.filter(user=self.request.user)
    
    
@login_required
def update_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)

    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor profile updated successfully!")
            return redirect('InstructorListView')  # Replace with your desired page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InstructorForm(instance=instructor)

    return render(request, 'teacher/update_teacher.html', {'form': form})


@login_required
def delete_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)
    
    instructor.delete()
    messages.success(request, "Instructor profile deleted successfully!")
    return redirect('InstructorListView')  # Replace with your desired page



#level


def level_list(request):
    levels = Levels.objects.all()
    return render(request, 'teacher/level_list.html', {'levels': levels})

# Add new Level
def add_level(request):
    if request.method == "POST":
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm()
    return render(request, 'teacher/add_level.html', {'form': form})


# Update Level
def update_level(request, pk):
    level = get_object_or_404(Levels, pk=pk)
    if request.method == "POST":
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm(instance=level)
    return render(request, 'teacher/update_level.html', {'form': form})


def delete_level(request, pk):
    level = get_object_or_404(Levels, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('level_list')





# Add new Level
def add_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm()
    return render(request, 'teacher/add_language.html', {'form': form})

def language_list(request):
    language = Language.objects.all()
    return render(request, 'teacher/language_list.html', {'language': language})


def update_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm(instance=language)
    return render(request, 'teacher/update_language.html', {'form': form})


def delete_language(request, pk):
    level = get_object_or_404(Language, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('language_list')
# END LANGUAGE 






# START COURSE

class Coalesce(Func):
    """Return, from left to right, the first non-null expression."""

    function = "COALESCE"

    def __init__(self, *expressions, **extra):
        if len(expressions) < 2:
            raise ValueError("Coalesce must take at least two expressions")
        super().__init__(*expressions, **extra)

    @property
    def empty_result_set_value(self):
        for expression in self.get_source_expressions():
            result = expression.empty_result_set_value
            if result is NotImplemented or result is not None:
                return result
        return None

    def as_oracle(self, compiler, connection, **extra_context):
        # Oracle prohibits mixing TextField (NCLOB) and CharField (NVARCHAR2),
        # so convert all fields to NCLOB when that type is expected.
        if self.output_field.get_internal_type() == "TextField":
            clone = self.copy()
            clone.set_source_expressions(
                [
                    Func(expression, function="TO_NCLOB")
                    for expression in self.get_source_expressions()
                ]
            )
            return super(Coalesce, clone).as_sql(compiler, connection, **extra_context)
        return self.as_sql(compiler, connection, **extra_context)


class Aggregate(Func):
    template = "%(function)s(%(distinct)s%(expressions)s)"
    contains_aggregate = True
    name = None
    filter_template = "%s FILTER (WHERE %%(filter)s)"
    window_compatible = True
    allow_distinct = False
    empty_result_set_value = None

    def __init__(
        self, *expressions, distinct=False, filter=None, default=None, **extra
    ):
        if distinct and not self.allow_distinct:
            raise TypeError("%s does not allow distinct." % self.__class__.__name__)
        if default is not None and self.empty_result_set_value is not None:
            raise TypeError(f"{self.__class__.__name__} does not allow default.")
        self.distinct = distinct
        self.filter = filter
        self.default = default
        super().__init__(*expressions, **extra)

    def get_source_fields(self):
        # Don't return the filter expression since it's not a source field.
        return [e._output_field_or_none for e in super().get_source_expressions()]

    def get_source_expressions(self):
        source_expressions = super().get_source_expressions()
        if self.filter:
            return source_expressions + [self.filter]
        return source_expressions

    def set_source_expressions(self, exprs):
        self.filter = self.filter and exprs.pop()
        return super().set_source_expressions(exprs)

    def resolve_expression(
        self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    ):
        # Aggregates are not allowed in UPDATE queries, so ignore for_save
        c = super().resolve_expression(query, allow_joins, reuse, summarize)
        c.filter = c.filter and c.filter.resolve_expression(
            query, allow_joins, reuse, summarize
        )
        if summarize:
            # Summarized aggregates cannot refer to summarized aggregates.
            for ref in c.get_refs():
                if query.annotations[ref].is_summary:
                    raise FieldError(
                        f"Cannot compute {c.name}('{ref}'): '{ref}' is an aggregate"
                    )
        elif not self.is_summary:
            # Call Aggregate.get_source_expressions() to avoid
            # returning self.filter and including that in this loop.
            expressions = super(Aggregate, c).get_source_expressions()
            for index, expr in enumerate(expressions):
                if expr.contains_aggregate:
                    before_resolved = self.get_source_expressions()[index]
                    name = (
                        before_resolved.name
                        if hasattr(before_resolved, "name")
                        else repr(before_resolved)
                    )
                    raise FieldError(
                        "Cannot compute %s('%s'): '%s' is an aggregate"
                        % (c.name, name, name)
                    )
        if (default := c.default) is None:
            return c
        if hasattr(default, "resolve_expression"):
            default = default.resolve_expression(query, allow_joins, reuse, summarize)
            if default._output_field_or_none is None:
                default.output_field = c._output_field_or_none
        else:
            default = Value(default, c._output_field_or_none)
        c.default = None  # Reset the default argument before wrapping.
        coalesce = Coalesce(c, default, output_field=c._output_field_or_none)
        coalesce.is_summary = c.is_summary
        return coalesce

    @property
    def default_alias(self):
        expressions = self.get_source_expressions()
        if len(expressions) == 1 and hasattr(expressions[0], "name"):
            return "%s__%s" % (expressions[0].name, self.name.lower())
        raise TypeError("Complex expressions require an alias")

    def get_group_by_cols(self):
        return []

    def as_sql(self, compiler, connection, **extra_context):
        extra_context["distinct"] = "DISTINCT " if self.distinct else ""
        if self.filter:
            if connection.features.supports_aggregate_filter_clause:
                try:
                    filter_sql, filter_params = self.filter.as_sql(compiler, connection)
                except FullResultSet:
                    pass
                else:
                    template = self.filter_template % extra_context.get(
                        "template", self.template
                    )
                    sql, params = super().as_sql(
                        compiler,
                        connection,
                        template=template,
                        filter=filter_sql,
                        **extra_context,
                    )
                    return sql, (*params, *filter_params)
            else:
                copy = self.copy()
                copy.filter = None
                source_expressions = copy.get_source_expressions()
                condition = When(self.filter, then=source_expressions[0])
                copy.set_source_expressions([Case(condition)] + source_expressions[1:])
                return super(Aggregate, copy).as_sql(
                    compiler, connection, **extra_context
                )
        return super().as_sql(compiler, connection, **extra_context)

    def _get_repr_options(self):
        options = super()._get_repr_options()
        if self.distinct:
            options["distinct"] = self.distinct
        if self.filter:
            options["filter"] = self.filter
        return options

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, user=request.user)  # Pass user to the form
        if form.is_valid():
            course = form.save(commit=False)
            instructor = Instructor.objects.filter(user=request.user).first()  # Fetch the current instructor
            if instructor:
                course.author = instructor
                course.save()
                messages.success(request, "Course added successfully!")
                return redirect('course_list')
            else:
                messages.error(request, "You are not an instructor. Please contact the admin.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm(user=request.user)  # Pass user to the form
    
    instructor = Instructor.objects.filter(user=request.user).first()
    return render(request, 'teacher/add_course.html', {'form': form, 'instructor': instructor})

@login_required
def course_list(request):
    # Filter courses where the author is the currently logged-in user
    courses = Course.objects.filter(author__user=request.user)
    return render(request, 'teacher/course_list.html', {'courses': courses})

class Sum(FixDurationInputMixin, Aggregate):
    function = "SUM"
    name = "Sum"
    allow_distinct = True


def get_course_data(course_id, user=None):
    """
    
    Retrieves course details, lessons, and video progress. used in course_detail and WATCH_COURSE
    
    """
    course = get_object_or_404(Course, pk=course_id)
    course_time_duration = VideoModel.objects.filter(course=course).aggregate(sum=Sum('time_duration'))
    lessons = course.lesson_set.annotate(total_duration=Sum('videomodel__time_duration'))

    category = Categories.objects.all().order_by('id')[0:6] #category on nav bar 

    check_enroll = None
    

    if user and user.is_authenticated:
        check_enroll = UserCourses.objects.filter(user=user, course=course).first()
        
    return {
        'course': course,
        'course_time_duration': course_time_duration,
        'lessons': lessons,
        'check_enroll': check_enroll,
        'category':category
    }


def course_detail(request, course_id):
    course_data = get_course_data(course_id, request.user)   # another function, place just above
    return render(request, 'teacher/course-details.html', course_data)

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
        # print(course.author)
        # print(form)
    return render(request, 'lecture/update_course.html', {'form': form,'course':course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})
