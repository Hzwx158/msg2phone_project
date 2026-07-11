from msg2phone import InfoExitHandler, Messager

user_input = input("type something to test: ")

with InfoExitHandler(
    lambda : f"Title of {user_input}",
    f"Success {user_input}",
    tags=["test"],
    name="feishu",
) as eh:
    a = [10]
    b = [200]
    print(f"a+b={a+b}")
    eh.success_msg += " >_< suffix"

