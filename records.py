"""记录校验，金额以整数分存储。"""
from datetime import date
from decimal import Decimal, InvalidOperation
import uuid
CATEGORIES = ['饮食','交通','购物','住房','娱乐','医疗','学习','工资','奖金','其他']
def validate(data):
    date.fromisoformat(data['date'])
    if data['type'] not in ['income','expense']: raise ValueError('请选择收支类型')
    if data['category'] not in CATEGORIES: raise ValueError('请选择有效类别')
    try:
        amount = Decimal(str(data['amount']))
        if not amount.is_finite() or amount <= 0 or amount > 999999999 or amount.as_tuple().exponent < -2: raise ValueError('金额须大于零，最多两位小数')
    except InvalidOperation: raise ValueError('金额格式错误')
    note = str(data.get('note','')).strip()
    if len(note) > 200: raise ValueError('备注最多200字')
    return dict(id=str(uuid.uuid4()), date=data['date'], type=data['type'], category=data['category'], cents=int(amount*100), note=note)
def select(rows, q):
    return sorted([r for r in rows if
        (not q.get('start') or r['date'] >= q['start']) and
        (not q.get('end') or r['date'] <= q['end']) and
        (not q.get('category') or r['category'] == q['category']) and
        (not q.get('type') or r['type'] == q['type']) and
        (not q.get('min') or r['cents'] >= Decimal(q['min'])*100) and
        (not q.get('max') or r['cents'] <= Decimal(q['max'])*100)], key=lambda r:r['date'], reverse=True)
