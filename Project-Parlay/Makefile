.PHONY: run

clean:
	rm testing_script.txt
	rm SampleOutput_1.0.txt
run:
	python3 testing_script_generator.py
	python3 parlay.py < testing_script.txt > results/output.txt

demo:
	python3 testing_script_generator.py
	python3 parlay.py < testing_script.txt > ZampleOutput_2.0.txt
