.PHONY: run

clean:
	rm ZampleOutput_6.0.txt
run:
	python3 testing_script_generator.py
	python3 parlay_testing_version.py < testing_script.txt > ZampleOutput_3.0.txt

runBF:
	python3 ts_genBF.py
	python3 parlayBFonly.py < testing_scriptBF.txt > ZampleOutput_4.0.txt

test:

	number=1 ; while [[ $$number -le 500 ]] ; do \
        python3 testing_script_generator.py ; \
	python3 parlay_testing_version.py < testing_script.txt >> ZampleOutput_3.0.txt ; \
        ((number = number + 1)) ; \
	done


testBF:
	number=1 ; while [[ $$number -le 300 ]] ; do \
        python3 ts_genBF.py ; \
	python3 parlayBFonly.py < testing_scriptBF.txt >> ZampleOutput_4.0.txt ; \
        ((number = number + 1)) ; \
	done

fetchData:
	python3 test_data_reader.py < ZampleOutput_3.0.txt

fetchDatag10+:
	python3 test_data_reader_g10+.py < ZampleOutput_3.0.txt

fetchDatag10+BF:
	python3 test_data_reader_g10+.py < ZampleOutput_4.0.txt

sim:

#num iterations for the for loops is the length of the list of bin sizes for hypoParlays which we wish to simulate
#this list can be edited in the value.py file
	

	i=1; \
	while [[ $$i -le 1 ]]; do \
		if [ $$i -eq 1 ]; then \
			python3 value.py > ZampleOutput_5.0.txt ; \
		else \
			python3 value.py >> ZampleOutput_5.0.txt ; \
		fi; \
		((i = i + 1)) ; \
	done

	j=1; \
	while [[ $$j -le 1 ]]; do \
		python3 valueSimulator.py < ZampleOutput_5.0.txt > ZampleOutput_6.0.txt ; \
		((j = j + 1)) ; \
	done


simSecondHalf:
	
		python3 valueSimulator.py < ZampleOutput_5.0.txt >> ZampleOutput_6.0.txt
	
simA:
	python3 value.py > ZampleOutput_5.0.txt