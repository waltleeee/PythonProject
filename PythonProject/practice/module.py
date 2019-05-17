import plugin.function
import plugin.function as aaa
import plugin.accountclass as accountclass

print(max(5,6))
print(aaa.max(10,12))

acct=accountclass.Account("walt","777",1000)
acct.deposit(500)
acct.withdraw(200)
print(acct)