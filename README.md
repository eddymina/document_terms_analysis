# Document Terms Analysis

How to use this simple tool: 

1. Let your data, either a folder or single document, be the same directory (sample_folder has some sample shakespeare text)


`python text_analyzer -h`: display analyzer options <br /><br />

`python text_analyzer.py -i sample_folder`: analyze all elements in corpus sample folder <br />
`python text_analyzer.py -i sample_folder/sample_1.txt`: analyze all elements in sample_1.txt
<br /><br />
`python text_analyzer.py -i sample_folder/sample_1.txt -top_k 10`: analyze and display top 10 frequencies 
<br /><br />
`python text_analyzer.py -i sample_folder/sample_1.txt -top_k 10 --tfidf sample_1.txt`: analyze compared tfidf for sample_1 with respect to the entire corpus 

---

More info on TFIDF here: http://www.tfidf.com/

Stayed tuned for future work with stop words and document similarity 





