.PHONY : %.xml clean

A-n32-k05:
	python3 main.py -t 0 -o "CVRP" "../data/Augerat-A/augerat-1995-set-a/A-n32-k05.xml"

all: clean
	find ../data -name '*.xml' -exec make "{}" + 

all-g: clean
	find ../data -name '*.xml' -exec make args=-g "{}" + 

%.xml: main.py
	python3 main.py -t 60 -o `basename $*` $(args) $@

clean :
	rm -f *.sol
	rm -f *.png

submission : clean
	tar -cvzf ../src.tgz ../src/

%.profile: main.py
	# sudo pip install cProfile
	# sudo pip install snakeviz
	python3 -m cProfile -o program.prof main.py $*.xml
	snakeviz program.prof