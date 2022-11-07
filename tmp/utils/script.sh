#!/bin/bash
echo "START"
echo "1.log"
python3.7 retrive-tweet-from-ID.py full_NAACL_SRW_2016.csv >> fulltext_NAACL_SRW_2016.log
echo "2.log"
python3.7 retrive-tweet-from-ID.py full_NLP+CSS_2016.csv >> fulltext_NLP+CSS_2016.log
echo "3.log"
python3.7 retrive-tweet-from-ID.py full_IHSC_ids-total.csv >> fulltext_IHSC_ids-total.log
echo "END"