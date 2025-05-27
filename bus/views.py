from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from bus.models import BusRoute


@login_required
def map_view(request):
    routes = BusRoute.objects.all()
    route_data = []

    for r in routes:
        route_data.append({
            'bus_number': r.bus.bus_number,
            'route': r.get_route(),
            'stops': r.get_stops(),
        })

    return render(request, 'bus/map.html', {
        'routes': route_data,
        'bus_numbers': [r['bus_number'] for r in route_data],
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Bus, BusEntry

def bus_entry_view(request, pk):
    bus = get_object_or_404(Bus, pk=pk)

    if request.method == "POST":
        BusEntry.objects.create(bus=bus)
        return redirect('bus_entry', pk=bus.pk)

    return render(request, 'bus/bus_entry.html', {'bus': bus})



@login_required
def driver_tracking_view(request):
    return render(request, 'bus/driver_live.html')


from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncHour
from django.utils import timezone
from datetime import timedelta
from .models import Bus, BusEntry

def analytics_view(request):
    buses = Bus.objects.all()
    selected_id = request.GET.get("bus")
    chart_data = []
    level = None
    interval = None

    if selected_id:
        bus = get_object_or_404(Bus, pk=selected_id)

        # Группировка по часу для графика
        entries = (
            BusEntry.objects
            .filter(bus=bus)
            .annotate(hour=TruncHour('timestamp'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )

        chart_data = [
            {"hour": e["hour"].strftime("%Y-%m-%d %H:%M"), "count": e["count"]}
            for e in entries
        ]

        # Анализ потока за последние 10 минут
        ten_minutes_ago = timezone.now() - timedelta(minutes=21)
        recent_count = BusEntry.objects.filter(bus=bus, timestamp__gte=ten_minutes_ago).count()

        if recent_count > 30:
            level = "Огромный поток"
        else:
            level = "Стабильный поток"

        # Расчёт рекомендованного интервала выпуска
        if recent_count <= 10:
            interval = 20
        elif 11 <= recent_count <= 30:
            interval = 10
        elif 31 <= recent_count <= 60:
            interval = 5
        else:
            interval = 3

    return render(request, 'bus/analytics.html', {
        'buses': buses,
        'chart_data': chart_data,
        'selected_id': selected_id,
        'level': level,
        'interval': interval,
    })

