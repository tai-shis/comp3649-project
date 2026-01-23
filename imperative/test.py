from input.scanner import Scanner

def test_scanner():
    with open("imperative/tests/input1.txt") as file:
        scanner = Scanner(file)

        print('-'*50)
        print(f"Test Case 1")
        print(f"a = a + 1")
        print('-'*50)
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")
        token = scanner.next_token()
        print(token, end=" ")
        print(" => destination")


if __name__ == "__main__":
    test_scanner()