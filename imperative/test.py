from input.scanner import Scanner

def test_scanner():
    with open("imperative/tests/input1.txt") as file:
        scanner = Scanner(file)

        # Test Case 1
        print('-'*50)
        print(f"Test Case 1")
        print(f"a = a + 1")
        print('-'*50)

        expected = [ "destination", "equals", "variable", "operator", "literal", "newline"]
        print(scanner)
        for e in expected:
            token = scanner.next_token()
            print(token, end=" ")
            print(f"=> {e}")
        print(scanner)
        scanner.reset()
        print(scanner)
        print('-'*50)

        # Test Case 2
        print('-'*50)
        print(f"Test Case 2")
        print(f"t1 = a * 4")
        print('-'*50)

        expected = [ "destination", "equals", "variable", "operator", "literal", "newline"]
        print(scanner)
        for e in expected:
            token = scanner.next_token()
            print(token, end=" ")
            print(f"=> {e}")
        print(scanner)
        scanner.reset()
        print(scanner)
        print('-'*50)



if __name__ == "__main__":
    test_scanner()