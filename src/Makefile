PY=python3

.PHONY : %.xml clean

A-n32-k05:
	$(PY) main.py -t 20 -o "CVRP" "../data/Augerat-A/augerat-1995-set-a/A-n32-k05.xml"

all: clean
	find ../data -name '*.xml' -exec make "{}" + 

all-g: clean
	find ../data -name '*.xml' -exec make args=-g "{}" + 

%.xml: main.py
	$(PY) main.py -t 1 -o `basename $*` $(args) $@

clean :
	rm -f *.sol
	rm -f *.png

submission : clean
	tar -cvzf ../src.tgz ../src/

performancetest: 
	$(PY) main.py -t 60 -performancetest true

%.profile: main.py
	# sudo pip install cProfile
	# sudo pip install snakeviz
	$(PY) -m cProfile -o program.prof main.py $*.xml
	snakeviz program.prof