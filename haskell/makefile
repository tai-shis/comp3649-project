GHCI = ghci
FLAGS = -i./Input -i./Tests
GHC = ghc
OUT = ./bin

all: build test-all

build:
	mkdir -p $(OUT)
	$(GHC) $(FLAGS) Input/Token.hs Input/Instruction.hs Tests/TokenTest.hs Tests/InstructionTest.hs -outputdir $(OUT)

test-token:
	$(GHCI) $(FLAGS) Tests/TokenTest.hs

test-instruction:
	$(GHCI) $(FLAGS) Tests/InstructionTest.hs

test-liveness:
	$(GHCI) $(FLAGS) Tests/LivenessTest.hs

test-assembly:
	$(GHCI) $(FLAGS) Tests/AssemblyTest.hs

test-all:
	runghc Tests/TokenTest.hs
	runghc Tests/InstructionTest.hs

clean:
	rm -rf $(OUT)