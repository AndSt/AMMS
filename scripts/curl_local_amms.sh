
for i in $(seq 1 $1); do
	if [ $(($i % 100)) -eq 0 ];
		then echo $i
	fi

	curl -s -X POST "localhost:5000" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"text\":\"Monatlich bezahlen, gruzefix\"}" > /dev/null;
done
