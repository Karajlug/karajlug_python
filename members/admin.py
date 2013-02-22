# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010  Karajlug community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.forms.formsets import all_valid
from django.forms.util import ErrorList

from .models import Member, MemberDetail


def email(obj):
    return obj.user.email
email.short_description = "Email"


class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface class for member model
    """
    list_display = ("__unicode__", "link", email, "user")
    list_editable = ("link", )
    search_fields = ("user", )
    list_filter = ("user", )

    def save_form(self, request, form, change):
        if request.user == form.cleaned_data["user"] or request.user.is_superuser or \
               request.user.has_perm("members.member_admin"):
            return form.save(commit=False)
        else:
            raise PermissionDenied(_("You can only add yourself as a member"))

    def save_model(self, request, obj, form, change):
        if request.user == obj.user or request.user.is_superuser or \
               request.user.has_perm("members.member_admin"):
            obj.creator = request.user
            if not request.user.is_superuser or \
               not request.user.has_perm("members.member_admin"):
                if change:
                    obj.weight = Member.objects.filter(id=obj.id)[0].weight
                else:
                    obj.weight = 40
            obj.save()
        else:
            raise PermissionDenied(_("You can only add yourself as a member"))


    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta
        error_msg = None

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    new_object = self.save_form(request, form, change=False)
                    form_validated = True
                except PermissionDenied as e:
                    form_validated = False
                    error_msg = str(e)
                    new_object = self.model()
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request),
                                       self.get_inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=inline.queryset(request))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=False)

                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request),
                                       self.get_inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        if error_msg:
            form.errors["user"] = ErrorList([error_msg])

        context = {
            'title': _('Add %s') % unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

    def queryset(self, request):
        """
        Return the records that user allowed to see.
        """
        items = None
        if request.user.is_superuser or request.user.has_perm("members.member_admin"):
            items = self.model.objects.all()
        else:
            items = self.model.objects.filter(user=request.user.id)
        return items


class DetailAdmin(admin.ModelAdmin):
    """
    Admin interface class for member detail model
    """
    list_display = ("member", "field_name", "field_value", "user", "weight", "language")
    list_editable = ("field_name", "field_value", "weight", "language")
    ordering = ("weight", "id")
    search_fields = ("member", "filed_name")
    list_filter = ("user", "member")


    def save_model(self, request, obj, form, change):
        if request.user == obj.member.user or request.user.is_superuser or \
               request.user.has_perm("members.member_admin"):
            obj.user = request.user
            obj.save()
        else:
            raise PermissionDenied(_("You can add only yourself as a member."))

    def save_form(self, request, form, change):
        if "member" in form.cleaned_data:
            if request.user == form.cleaned_data["member"].user or \
                   request.user.is_superuser or \
                   request.user.has_perm("members.member_admin"):

                return form.save(commit=False)
            else:
                raise PermissionDenied(_("You can add only details about yourself."))
        else:
            if request.user == form.cleaned_data["id"].member or \
                   request.user.is_superuser or \
                   request.user.has_perm("members.member_admin"):

                return form.save(commit=False)
            else:
                raise PermissionDenied(_("You can add only details about yourself."))

    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta
        error_msg = None

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    new_object = self.save_form(request, form, change=False)
                    form_validated = True
                except PermissionDenied as e:
                    form_validated = False
                    error_msg = str(e)
                    new_object = self.model()
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=inline.queryset(request))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=False)

                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        if error_msg:
            form.errors["member"] = ErrorList([error_msg])

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

    def queryset(self, request):
        """
        Return the records that user allowed to see.
        """
        items = None
        if request.user.is_superuser or request.user.has_perm("members.member_admin"):
            items = self.model.objects.all()
        else:
            items = self.model.objects.filter(member__user=request.user.id)
        return items


admin.site.register(Member, MemberAdmin)
admin.site.register(MemberDetail, DetailAdmin)
