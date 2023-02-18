from pyqiwip2p import AioQiwiP2P

# QIWI_PRIV_KEY = "f1bf351a79eea75eb4f34ba031778816"

# p2p = AioQiwiP2P(auth_key=QIWI_PRIV_KEY)

async def create_invoice(amount: int, comment: str=None):
    # Выставим счет на сумму 228 рублей который будет работать 15 минут
    new_bill = await p2p.bill(amount=amount, lifetime=15)

    print(new_bill.bill_id, new_bill.pay_url)
    return new_bill.pay_url, new_bill.bill_id
    # Потеряли ссылку на оплату счета? Не проблема!
    # print(await p2p.check(bill_id=245532).pay_url)

    # Клиент отменил заказ? Тогда и счет надо закрыть
    # await p2p.reject(bill_id=new_bill.bill_id)

async def check_payment(bill_id: int) -> bool:
    # Проверим статус выставленного счета через его bill_id
    return await p2p.check(bill_id=bill_id).status
