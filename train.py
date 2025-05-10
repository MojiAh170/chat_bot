try:
    a = int(input("عدد اول: "))
    b = int(input("عدد دوم: "))
    print("حاصل:", a / b)
except ZeroDivisionError:
    print("تقسیم بر صفر مجاز نیست.")
except ValueError:
    print("فقط عدد وارد کن لطفاً.")
