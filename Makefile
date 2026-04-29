all:report.pdf
report.pdf:report.tex ref.bib
	pdflatex report.tex
	bibtex report
	pdflatex report.tex
	pdflatex report.tex
.PHONY:clean
clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out
