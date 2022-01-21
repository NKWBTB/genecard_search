from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv

if __name__ == "__main__":
    lines = []
    browser = webdriver.Firefox()
    
    with open("genelist.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open("genesearch.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["gene", "gene_type", "RNA_type", "summary", "Aliases"])
        for i in range(1, len(lines)):
            gene = lines[i][:-1]
            print(i, gene)
            browser.get("https://www.genecards.org/cgi-bin/carddisp.pl?gene="+gene)
            html = browser.page_source

            soup = BeautifulSoup(html, 'html.parser')

            first = soup.find(id="geneSymbol")
            if first is None:
                writer.writerow([gene, "Not found"])
                continue
            gene_type = first.parent.find(class_="gc-category")
            gene_type = gene_type.get_text().strip()

            first = soup.find(id="aliases_descriptions")
            second = first.find_all(class_="gc-subsection")
            RNA_type = ""
            Aliases = []
            for header in second:
                desc_text = header.find("h3")
                # print("!!!", desc_text.string)
                if desc_text.get_text().strip().startswith("RNA"):
                    RNA_type = desc_text.parent.find("div").get_text().strip()
                    # print(RNA_type)
                elif desc_text.get_text().strip().startswith("Aliases"):
                    for span in header.find_all(class_="aliasMainName"):
                        alias = span.get_text().strip()
                        fspace = alias.find('\n')
                        alias = alias[:fspace].strip()
                        # print(alias)
                        Aliases.append(alias)
                
            first = soup.find(id="summaries")
            second = first.find_all(class_="gc-subsection")
            summary = ""
            for header in second:
                desc_text = header.find("h3")
                # print(desc_text.get_text().strip())
                if desc_text.get_text().strip().startswith("GeneCards Summary"):
                    summary = header.find("p").get_text().replace('\n', '').strip()
                    summary = re.sub(' +', ' ', summary)
                    # print(summary)
            writer.writerow([gene, gene_type, RNA_type, summary] + Aliases)