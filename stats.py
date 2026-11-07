def summarize(rows):
    income = sum(r['cents'] for r in rows if r['type']=='income')
    expense = sum(r['cents'] for r in rows if r['type']=='expense')
    categories = {}
    for r in rows:
        if r['type']=='expense': categories[r['category']] = categories.get(r['category'],0)+r['cents']
    return dict(income=income, expense=expense, balance=income-expense, count=len(rows), categories=categories)
