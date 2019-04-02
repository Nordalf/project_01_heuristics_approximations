.PHONY : %.xml

A-n32-k05:
	python3 main.py -t 0 -o "CVRP" "../data/Augerat-A/augerat-1995-set-a/A-n32-k05.xml"

all:
	python3 main.py -t 30 -o "CVRP" -all true

%.xml: main.py
	python3 main.py -t 30 -o `basename $*` $@


%.profile: main.py
	# sudo pip install cProfile
	# sudo pip install snakeviz
	python3 -m cProfile -o program.prof main.py $*.xml
	snakeviz program.prof
