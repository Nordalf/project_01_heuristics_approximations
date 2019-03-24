.PHONY : %.xml


%.xml: main.py
	python3 main.py -t 30 -o `basename $*` $@


%.profile: main.py
	# sudo pip install cProfile
	# sudo pip install snakeviz
	python3 -m cProfile -o program.prof main.py $*.xml
	snakeviz program.prof
