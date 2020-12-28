for file in 05*; do
	sed -i "s/sugar-beet/0/g" $file;
#	sed -i "s/15 /0 /g" $file;
done
