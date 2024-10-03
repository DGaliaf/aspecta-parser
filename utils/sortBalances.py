def sort_balance():
    with open("../balances/balances.txt", "r") as balances:
        lines = balances.readlines()

        for line in lines:
            addr, balance = line.split(":")
            print(addr, balance)

            if 0 <= float(balance.strip()) <= 500:
                file_path = "../balances/0_400.txt"
            elif 501 <= float(balance.strip()) <= 1000:
                file_path = "../balances/401_1000.txt"
            else:
                file_path = "../balances/1000_plus.txt"

            with open(file_path, "a") as b_output:
                b_output.write(f"{addr}\n")


if __name__ == "__main__":
    sort_balance()
