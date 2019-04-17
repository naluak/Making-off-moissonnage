#coding: utf-8

import json
import csv
import requests
from bs4 import BeautifulSoup 

entete = {
	"User-Agent":"Stéphanie Prévost - 438-777-4252. Je fais un moissonnage de donnée dans le cadre d'un cours universitaire en journalisme de données.",
	"From":"stephanie-prevost@hotmail.ca"
}

fichier = "UQO_PROF.csv"
f2 = open(fichier,"w")
csvOutput = csv.writer(f2)
csvOutput.writerow(["nom", "université", "ville", "pavillon", "domaine", "spécialisation", "num Téléphone","courriel", "url"])

lettre_dic = {
	"DPP" : "Département de psychoéducation et de psychologie",
	"DRI" : "Département de relations industrielles",
	"DTS" : "Département de travail social",
	"DSA" : "Département des sciences administratives",
	"DCTB" : "Département des sciences comptables",
	"DSE" : "Département des sciences de l'éducation",
	"DSI" : "Département des sciences infirmières",
	"DSN" : "Département des sciences naturelles",
	"DSSO" : "Département des sciences sociales",
	"DEL" : "Département d'études langagières",
	"DII" : "Département d'informatique et d'ingénierie",
	"EMI" : "École multidisciplinaire de l'image"
}

university = "Université du Québec en Outaouais"

def parsePage(nom, lettre, liens_fiche_prof):

	contenu2=requests.get(liens_fiche_prof, headers=entete)

	page_suite = BeautifulSoup(contenu2.text,"html.parser") 

	infos_profs = page_suite.find("div", id="divInfoProf")
	if infos_profs != None:

		#informations des profs:

		pavillonHTML = infos_profs.find("div", id="divBureau")
		pavillon = "Pavillon Inconnu"
		if pavillonHTML != None:
			pavillon = pavillonHTML.find("span", id="lblNomPavillon").text

		if pavillon == "Campus de Saint-Jérôme":
			ville = "Saint-Jérôme"
		else:
			ville = "Gatineau"

		courrielHTML = infos_profs.find("a", id="lnkCourriel")
		courriel = "Courriel Inconnu"
		if courrielHTML != None:
			courriel = courrielHTML.text

		domaineHtml = infos_profs.find("a", id="linkDepartement")
		domaine = "Domaine Inconnu"
		if domaineHtml != None:
			domaine = domaineHtml.find("span", id="lblDepartement").text

		specialisationHTML = infos_profs.find("div", id="divSpec")
		specialisation = "Spécialisation Inconnue"
		if specialisationHTML != None:
			listDeLi = specialisationHTML.find("ul", id="lstSpec").find_all("li")
			def getText(li):
				return li.text
			listDeSpecialisation = map(getText, listDeLi)
			specialisation = " % ".join(listDeSpecialisation)

		nbTelHTML = infos_profs.find("span", id="lblNoTel")
		nbTel = "Numéro de téléphone Inconnu"
		if nbTelHTML != None:
			nbTel = nbTelHTML.text

		print(nom, "/", university,"/", ville,"/", pavillon,"/", domaine,"/", specialisation,"/", nbTel,"/", courriel,  "/", url_Prof)
		csvOutput.writerow([nom, university, ville, pavillon, domaine, specialisation, nbTel, courriel, url_Prof])
	else:
		csvOutput.writerow([nom, university, "Ville Inconnue", "Pavillon Inconnu", lettre_dic.get(lettre), "Spécialisation Inconnue", "nbTel Inconnu", "courriel Inconnu", "url Inconnu"])


for lettre in lettre_dic:
	url = "http://apps.uqo.ca/DosEtuCorpsProf/AffDepartement.aspx?dep={}&onglet=p".format(lettre)

	contenu = requests.get(url,headers=entete)

	page=BeautifulSoup(contenu.text,"html.parser") 

	#prof:

	profs=page.find("table", id="lstProf").find_all("tr")

	for prof in profs:

		url_Prof = prof.find_all("a")[1]["href"]

		liens_fiche_prof = "http://apps.uqo.ca/DosEtuCorpsProf/" + url_Prof

		nom = prof.find_all("a")[1].text

		parsePage(nom, lettre, liens_fiche_prof)

	#prof asssocié:

	div_profs_asso=page.find("div", id="divProfAssoc")
	if div_profs_asso != None:
		
		profs_asso = div_profs_asso.find_all("tr")
		
		for prof_asso in profs_asso:

			span_nom = prof_asso.find("span")
			url_Prof = span_nom.find("a") 

			if url_Prof == None:
				nom = span_nom.text
				print(nom)
				csvOutput.writerow([nom, university, "Ville Inconnue", "Pavillon Inconnu", lettre_dic.get(lettre), "Spécialisation Inconnue", "nbTel Inconnu", "courriel Inconnu", "url Inconnu"])
			else:
				liens_fiche_prof = url_Prof["href"]
				bon_lien = "http://apps.uqo.ca/DosEtuCorpsProf/"
				if  bon_lien in liens_fiche_prof:
					parsePage(url_Prof.text, lettre, liens_fiche_prof)
				else:
					print(url_Prof.text)
					csvOutput.writerow([url_Prof.text, university, "Ville Inconnue", "Pavillon Inconnu", lettre_dic.get(lettre), "Spécialisation Inconnue", "nbTel Inconnu", "courriel Inconnu", "url Inconnu"])

	#prof honoraire:
	div_profs_honor=page.find("div", id="divProfHonor")
	if div_profs_honor != None:
		
		profs_honor = div_profs_honor.find_all("tr")
		
		for prof_honor in profs_honor:

			span_nom =prof_honor.find("span")
			url_Prof = span_nom.find("a")

			if url_Prof == None:
				nom = span_nom.text
				print(nom)
				csvOutput.writerow([nom, university, "Ville Inconnue", "Pavillon Inconnu", lettre_dic.get(lettre), "Spécialisation Inconnue", "nbTel Inconnu", "courriel Inconnu", "url Inconnu"])
			else:
				liens_fiche_prof = url_Prof["href"]
				bon_lien = "http://apps.uqo.ca/DosEtuCorpsProf/"
				if bon_lien in liens_fiche_prof:
					parsePage(url_Prof.text, lettre, liens_fiche_prof)
				else:
					print(url_Prof.text)
					csvOutput.writerow([url_Prof.text, university, "Ville Inconnue", "Pavillon Inconnu", lettre_dic.get(lettre), "Spécialisation Inconnue", "nbTel Inconnu", "courriel Inconnu", "url Inconnu"])

		
		
