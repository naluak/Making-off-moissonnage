#coding: utf-8

import json
import csv
import requests
from bs4 import BeautifulSoup 

entete = {
	"User-Agent":"Stéphanie Prévost - 438-777-4252. Je fais un moissonnage de donnée dans le cadre d'un cours universitaire en journalisme de données.",
	"From":"stephanie-prevost@hotmail.ca"
}

fichier = "Bishop_PROF.csv"
f2 = open(fichier,"w")
csvOutput = csv.writer(f2)
csvOutput.writerow(["université", "titre", "prénom", "nom", "domaine", "courriel", "num Téléphone", "url"])

for lettreOrd in range(ord("A"), ord("Z")+1):
	lettre = chr(lettreOrd)
	url = "https://www.ubishops.ca/bu-directory/char/{}".format(lettre)

	contenu = requests.get(url,headers=entete)

	page=BeautifulSoup(contenu.text,"html.parser") 

	profs=page.find_all("div", attrs={"data-entry-type":"individual"})

	for prof in profs:
		university = "Bishop university"

		titleHtml = prof.find("span", class_="title")
		title = "Titre Inconnu"
		if titleHtml != None:
			title = titleHtml.text

		prenom = prof.find("span", class_="given-name").text
		nom = prof.find("span", class_="family-name").text
		
		domaineHtml = prof.find("span", class_="organization-unit")
		domaine = "Domaine Inconnu"
		if domaineHtml != None:
			domaine = domaineHtml.text

		courrielHTML = prof.find("span", class_="email-address")
		courriel = "Courriel Inconnu"
		if courrielHTML != None:
			courriel = courrielHTML.find("a").text

		nbTelHTML = prof.find("span", class_="tel")
		nbTel = "Numéro de téléphone Inconnu"
		if nbTelHTML != None:
			nbTel = nbTelHTML.find("span", class_ = "value").text
		
		# print([university, title, prenom, nom, domaine, courriel, nbTel, url])
		csvOutput.writerow([university, title, prenom, nom, domaine, courriel, nbTel, url])

# Le document contient tous le personnel de l'école et possiblement plus. Il faudra nettoyer le dossier avant de l'utiliser.
