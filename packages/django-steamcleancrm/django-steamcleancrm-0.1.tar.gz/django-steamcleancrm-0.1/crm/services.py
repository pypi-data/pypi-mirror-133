from crm.models import Lead, WorkOrder

# Services start here


def lead_context_with_form(pk, form):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead,
        'form': form
    }
    return context

def work_order_context_with_form(lead_id, pk, form):
    lead = Lead.objects.get(id=lead_id)
    workorder = WorkOrder.objects.get(id=pk)
    context = {
        'lead': lead,
        'workorder': workorder,
        'form': form
    }
    return context