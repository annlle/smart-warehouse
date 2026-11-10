from django.shortcuts import render, redirect

items = [
    {
        'item_id': 'PALLET-001',
        'name': 'Електронні компоненти',
        'category': 'Електроніка',
        'weight_kg': 120,
        'quantity': 50,
        'zone': 'A',
        'x': 10,
        'y': 15,
        'status': 'IN_STOCK',
    },
    {
        'item_id': 'PALLET-002',
        'name': 'Літій-іонні акумулятори',
        'category': 'Електроніка',
        'weight_kg': 180,
        'quantity': 30,
        'zone': 'A',
        'x': 24,
        'y': 15,
        'status': 'RESERVED',
    },
    {
        'item_id': 'PALLET-003',
        'name': 'Кабельна продукція',
        'category': 'Електротехніка',
        'weight_kg': 90,
        'quantity': 75,
        'zone': 'B',
        'x': 8,
        'y': 20,
        'status': 'IN_STOCK',
    },
    {
        'item_id': 'PALLET-004',
        'name': 'Промислове обладнання',
        'category': 'Обладнання',
        'weight_kg': 250,
        'quantity': 10,
        'zone': 'C',
        'x': 30,
        'y': 12,
        'status': 'MOVING',
    },
]

def index(request):
    context = {
        'items': items,
        'total_items': len(items),
        'in_stock': sum(
            1 for item in items if item['status'] == 'IN_STOCK'
        ),
        'moving': sum(
            1 for item in items if item['status'] == 'MOVING'
        ),
    }

    return render(request, 'inventory/index.html', context)

def add(request):
    errors = []

    if request.method == 'POST':
        item_number = request.POST.get('item_number', '').strip()
        item_id = f'PALLET-{item_number}'
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        zone = request.POST.get('zone', '').strip().upper()

        try:
            weight_kg = float(request.POST.get('weight_kg', ''))
            quantity = int(request.POST.get('quantity', ''))
            x = int(request.POST.get('x', ''))
            y = int(request.POST.get('y', ''))

            if not item_id or not name or not category or not zone:
                errors.append('Заповніть усі текстові поля.')

            if any(item['item_id'] == item_id for item in items):
                errors.append('Палета з таким ID вже існує.')

            if weight_kg <= 0:
                errors.append('Вага повинна бути більшою за 0.')

            if quantity < 1:
                errors.append('Кількість повинна бути не меншою за 1.')

            if x < 0 or y < 0:
                errors.append('Координати не можуть бути від’ємними.')

            if not errors:
                items.append({
                    'item_id': item_id,
                    'name': name,
                    'category': category,
                    'weight_kg': weight_kg,
                    'quantity': quantity,
                    'zone': zone,
                    'x': x,
                    'y': y,
                    'status': 'IN_STOCK',
                })

                return redirect('inventory:index')

        except (ValueError, TypeError):
            errors.append('Перевірте правильність числових значень.')

    return render(request, 'inventory/add.html', {
        'errors': errors,
    })

def edit(request, item_id):
    item = next(
        (item for item in items if item['item_id'] == item_id),
        None
    )

    if item is None or item['status'] != 'IN_STOCK':
        return redirect('inventory:index')

    errors = []

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        zone = request.POST.get('zone', '').strip().upper()

        try:
            weight_kg = float(request.POST.get('weight_kg', ''))
            quantity = int(request.POST.get('quantity', ''))
            x = int(request.POST.get('x', ''))
            y = int(request.POST.get('y', ''))

            if not name or not category or not zone:
                errors.append('Заповніть усі текстові поля.')

            if weight_kg <= 0:
                errors.append('Вага повинна бути більшою за 0.')

            if quantity < 1:
                errors.append('Кількість повинна бути не меншою за 1.')

            if x < 0 or y < 0:
                errors.append('Координати не можуть бути від’ємними.')

            if not errors:
                item['name'] = name
                item['category'] = category
                item['weight_kg'] = weight_kg
                item['quantity'] = quantity
                item['zone'] = zone
                item['x'] = x
                item['y'] = y

                return redirect('inventory:index')

        except (ValueError, TypeError):
            errors.append('Перевірте правильність числових значень.')

    return render(request, 'inventory/edit.html', {
        'item': item,
        'errors': errors,
    })

def write_off(request, item_id):
    item = next(
        (item for item in items if item['item_id'] == item_id),
        None
    )

    if item is None or item['status'] != 'IN_STOCK':
        return redirect('inventory:index')

    if request.method == 'POST':
        item['status'] = 'WRITTEN_OFF'
        return redirect('inventory:index')

    return render(request, 'inventory/write_off.html', {
        'item': item,
    })

def delete(request, item_id):
    item = next(
        (item for item in items if item['item_id'] == item_id),
        None
    )

    if item is None or item['status'] not in ['IN_STOCK', 'WRITTEN_OFF']:
        return redirect('inventory:index')

    if request.method == 'POST':
        items.remove(item)
        return redirect('inventory:index')

    return render(request, 'inventory/delete.html', {
        'item': item,
    })

def change_status(request, item_id):
    if request.method != 'POST':
        return redirect('inventory:index')

    item = next(
        (item for item in items if item['item_id'] == item_id),
        None
    )

    if item is None:
        return redirect('inventory:index')

    allowed_transitions = {
        'IN_STOCK': ['RESERVED'],
        'RESERVED': ['IN_STOCK', 'MOVING'],
        'MOVING': ['IN_STOCK', 'SHIPPED'],
        'SHIPPED': [],
        'WRITTEN_OFF': [],
    }

    new_status = request.POST.get('status')

    if new_status in allowed_transitions.get(item['status'], []):
        item['status'] = new_status

    return redirect('inventory:index')