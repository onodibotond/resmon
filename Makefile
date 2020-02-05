build:
	cd ../; tar -zcvf resmon.tar.gz --exclude Makefile --exclude .git resmon

clean:
	cd ../; rm resmon.tar.gz
