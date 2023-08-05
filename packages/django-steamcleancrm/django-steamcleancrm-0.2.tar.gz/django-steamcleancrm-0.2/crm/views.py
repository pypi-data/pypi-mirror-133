from .forms import AddImageToWorkOrderForm, AddTechnicianToWorkOrderForm, CreateLeadForm, UpdateLeadForm, CreateWorkOrderForm, UpdateWorkOrderForm, CloseWorkOrderForm, SubmitWorkOrderForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Lead, WorkOrder, WorkOrderImages, WorkOrderTechnicians
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime
from . import services

# Views start here.


@login_required
@permission_required(['crm.view_lead', 'crm.view_workorder'], raise_exception=True)
# The dashboard is used to display information that requires your attention
def dashboard(request):
    open_leads = Lead.objects.filter(workorder__isnull=True).filter(is_active=True)
    unassigned_work_orders = WorkOrder.objects.filter(workordertechnicians__isnull=True).filter(is_complete=False).filter(is_canceled=False)
    open_work_orders = WorkOrder.objects.filter(workordertechnicians__isnull=False).filter(is_complete=False).filter(is_canceled=False)
    context = {
        'open_leads': open_leads,
        'unassigned_work_orders': unassigned_work_orders,
        'open_work_orders': open_work_orders
    }
    return render(request, 'crm/index.html', context)


@login_required
@permission_required('crm.view_lead', raise_exception=True)
# We search by Lead only because work orders dont have specific enough fields to search by yet
def lead_search_results(request):
    query = request.GET.get('query')
    object_list = Lead.objects.filter(
        Q(fullname__icontains=query) |
        Q(phone__icontains=query) |
        Q(address_line_1__icontains=query) |
        Q(address_line_2__icontains=query) |
        Q(city__icontains=query) |
        Q(state__icontains=query) |
        Q(zipcode__icontains=query) |
        Q(email__icontains=query)
    )
    context = {'object_list': object_list, 'query': query}
    return render(request, 'crm/lead_search_results.html', context)


@login_required
@staff_member_required
# Any user can close a work order but it must be approved by a user with manager permissions or above
def closed_work_orders(request):
    closed_pending_approval = WorkOrder.objects.filter(Q(is_complete=True, reviewed=False) | Q(is_canceled=True, reviewed=False))
    completed_work_orders = WorkOrder.objects.filter(reviewed=True, is_complete=True)
    canceled_work_orders = WorkOrder.objects.filter(reviewed=True, is_canceled=True)
    context = {
        'closed_pending_approval': closed_pending_approval,
        'completed_work_orders': completed_work_orders,
        'canceled_work_orders': canceled_work_orders,
    }
    return render(request, 'crm/closed_work_orders.html', context)


# A Lead holds client contact information and can have any number of associated work orders
class LeadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lead
    fields = ('fullname', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'email')
    template_name = 'crm/lead_form.html'
    permission_required = 'crm.add_lead'

    def post(self, request, *args, **kwaargs):
        form = CreateLeadForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = True
            instance.save()
        if 'save_lead' in request.POST:   
            return redirect('lead-detail', pk=instance.id)
        elif 'save_lead_open_work_order' in request.POST:
            return redirect('create-work-order', pk=instance.id)


# Includes all information associated with a specific lead instance such as work orders
class LeadDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Lead
    permission_required = 'crm.view_lead'

    def get_context_data(self, **kwargs):
        context = super(LeadDetailView, self).get_context_data(**kwargs)
        context['work_orders'] = WorkOrder.objects.filter(lead=self.get_object())
        return context


# Leads can be marked inactive but can not be deleted
class LeadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lead
    fields = '__all__'
    template_name_suffix = '_update_form'
    permission_required = ('crm.view_lead','crm.change_lead')

    def post(self, request, pk, *args, **kwaargs):
        form = UpdateLeadForm(request.POST)
        if form.is_valid():
                lead_instance = Lead.objects.get(id=pk)
                instance = form.save(commit=False)
                lead_instance = instance
                lead_instance.id = pk
                lead_instance.date_created = datetime.now()
                lead_instance.save()
        if 'save_lead' in request.POST:
            return redirect('lead-detail', pk=lead_instance.id)
        elif 'save_lead_open_work_order' in request.POST:
            return redirect('create-work-order', pk=lead_instance.id)


# A Work Order should only be opened wirh a Lead instance passed as an argument    
class WorkOrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = WorkOrder
    fields = ('job_description', 'estimate_date', 'estimate_date', 'appointment_date', 'appointment_time')
    template_name = 'crm/add_work_order_to_lead.html'
    permission_required = ('crm.view_lead', 'crm.add_workorder')

    def get(self, request, pk, *args, **kwargs):
        context = services.lead_context_with_form(pk, CreateWorkOrderForm)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = CreateWorkOrderForm(request.POST)
        if form.is_valid():
                lead_instance = Lead.objects.get(id=pk)
                instance = form.save(commit=False)
                instance.lead = lead_instance
                instance.save()
        if 'save_work_order' in request.POST:
            return redirect('work-order-detail', lead_id=pk, pk=instance.id)
        elif 'add-technician-to-work-order' in request.POST:
            return redirect('add-technician-to-work-order', lead_id=pk, pk=instance.id)
        else:
            context = services.lead_context_with_form(pk, CreateWorkOrderForm)
        return render(request, self.template_name, context)


# Includes all information associated with a specific work order instance such as images and assigned technicians
class WorkOrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = WorkOrder
    template_name = 'crm/workorder_detail.html'
    permission_required = ('crm.view_lead', 'crm.view_workorder', 'crm.view_workordertechnicians', 'crm.view_workorderimages')

    def get(self, request, pk, *args, **kwargs):
        workorder = WorkOrder.objects.get(id=pk)
        lead = Lead.objects.get(workorder=pk)
        technicians = WorkOrderTechnicians.objects.filter(work_order=self.get_object())
        images = WorkOrderImages.objects.filter(work_order=self.get_object())
        form = CloseWorkOrderForm()
        if workorder.is_complete == True  and workorder.reviewed == True or workorder.is_canceled == True and workorder.reviewed == True:
            context = {
                'lead': lead,
                'workorder': workorder,
                'technicians': technicians,
                'images': images,
            }
        else:
            context = {
                'lead': lead,
                'workorder': workorder,
                'technicians': technicians,
                'images': images,
                'form': form
            }
        return render(request, self.template_name, context)


    def post(self, request, lead_id, pk, *args, **kwargs):
        form = CloseWorkOrderForm(request.POST)
        if form.is_valid():
            lead_instance = Lead.objects.get(id=lead_id)
            workorder_instance = WorkOrder.objects.get(id=pk)
            workorder_instance.lead = lead_instance
            if 'mark_work_order_complete' in request.POST:
                workorder_instance.is_complete = True
                if request.user.is_staff:
                    workorder_instance.reviewed = True
                workorder_instance.save()
                return redirect('work-order-detail', lead_id=lead_id, pk=pk)
            elif 'mark_work_order_canceled' in request.POST:
                workorder_instance.is_canceled = True
                if request.user.is_staff:
                    workorder_instance.reviewed = True
                workorder_instance.save()
                return redirect('work-order-detail', lead_id=lead_id, pk=pk)


# Work orders can be marked complete or canceled but can not be deleted
class WorkOrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = WorkOrder
    fields = ('job_description', 'estimate_date', 'estimate_time', 'appointment_date', 'appointment_time', 'is_complete')
    template_name = 'crm/workorder_update_form.html'
    permission_required = ('crm.view_lead', 'crm.change_workorder')

    def get(self, request, lead_id, pk, *args, **kwargs):
        workorder = WorkOrder.objects.get(id=pk)
        context = services.work_order_context_with_form(lead_id, pk, UpdateWorkOrderForm(instance=workorder))
        return render(request, self.template_name, context)

    def post(self, request, lead_id, pk, *args, **kwaargs):
        form = CreateWorkOrderForm(request.POST)
        if form.is_valid():
                workorder_instance = WorkOrder.objects.get(id=pk)
                lead_instance = Lead.objects.get(id=lead_id)
                instance = form.save(commit=False)
                workorder_instance = instance
                workorder_instance.lead = lead_instance
                workorder_instance.id = pk
                workorder_instance.date_created = datetime.now()
                workorder_instance.save()
        if 'save_work_order' in request.POST:
            return redirect('work-order-detail', lead_id=lead_id, pk=pk)
        elif 'add-technician-to-work-order' in request.POST:
            return redirect('add-technician-to-work-order', lead_id=lead_id, pk=pk)


# Associates a technician with a specific work order instance
class AddTechnicianView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = WorkOrderTechnicians
    fields = ('technician', )
    template_name = 'crm/add_technician_to_work_order.html'
    permission_required = ('crm.view_lead', 'crm.view_workorder', 'crm.add_workordertechnicians')

    def get(self, request, lead_id, pk, *args, **kwargs):
        context = services.work_order_context_with_form(lead_id, pk, AddTechnicianToWorkOrderForm)
        return render(request, self.template_name, context)
        
    def post(self, request, lead_id, pk, *args, **kwargs):
        form = AddTechnicianToWorkOrderForm(request.POST)
        if form.is_valid():
            workorder_instance = WorkOrder.objects.get(id=pk)
            instance = form.save(commit=False)
            instance.work_order = workorder_instance
            # Prevents assigning duplicate technicians to work orders
            if WorkOrderTechnicians.objects.filter(work_order=workorder_instance, technician=instance.technician).exists():
                return redirect('work-order-detail', lead_id=lead_id, pk=pk)
            else:
                instance.save()
        if 'save_technician' in request.POST:
            return redirect('work-order-detail', lead_id=lead_id, pk=pk)
        elif 'save_and_add_another_technician' in request.POST:
            return redirect('add-technician-to-work-order', lead_id=lead_id, pk=pk)


# Deletes a technicians relationship to a specific work order instance
class RemoveTechnicianView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = WorkOrderTechnicians
    success_url = reverse_lazy('index')
    permission_required = 'crm.delete_workordertechnicians'


# Any number of images can be associated with a work order instance
class AddImageView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = WorkOrderImages
    fields = ('image', )
    template_name = 'crm/add_image_to_work_order.html'
    permission_required = ('crm.view_lead', 'crm.view_workorder', 'crm.add_workorderimages')

    def get(self, request, lead_id, pk, *args, **kwargs):
        context = services.work_order_context_with_form(lead_id, pk, AddImageToWorkOrderForm)
        return render(request, self.template_name, context)

    def post(self, request, lead_id, pk, *args, **kwargs):
        form = AddImageToWorkOrderForm(request.POST, request.FILES)
        if form.is_valid():
            workorder_instance = WorkOrder.objects.get(id=pk)
            instance = form.save(commit=False)
            instance.work_order = workorder_instance
            instance.image = request.FILES['image']
            instance.save()
        return redirect('work-order-detail', lead_id=lead_id, pk=pk)


# Removed images are deleted forever
class RemoveImageView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = WorkOrderImages
    success_url = reverse_lazy('index')
    permission_required = ('crm.delete_workorderimages')

