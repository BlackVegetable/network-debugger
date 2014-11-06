all: paper_summary.pdf discussion_summary.pdf

paper_summary.pdf: biblio.bib paper_summary.tex
	pdflatex paper_summary
	bibtex paper_summary
	pdflatex paper_summary
	pdflatex paper_summary

discussion_summary.pdf: biblio.bib discussion_summary.tex
	pdflatex discussion_summary
	pdflatex discussion_summary

clean: 
	\rm -f *.dvi *.aux *.ps *~ *.log *.blg *.bbl *.pdf
