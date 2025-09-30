# Projet Portfolio Finance : Analyse des Actifs avec Yahoo Finance et Power BI

## Introduction

Ce projet a pour objectif d'analyser et de visualiser la performance d'un portefeuille financier sur les cinq dernières années. Pour ce faire, nous nous posons plusieurs questions clés :  

- Comment les différents actifs du portefeuille (actions, cryptomonnaies, indices) ont-ils évolué sur la période ?  
- Quels actifs ont contribué le plus à la performance globale ?  
- Comment visualiser la répartition et la dynamique du portefeuille pour en tirer des insights pertinents ?  

Le projet est structuré sur deux pages principales dans Power BI :  
1. **Analyse par actif** : permet d’explorer individuellement chaque actif et ses indicateurs clés (valeur, performance, volatilité, Sharpe, drawdown, etc.).  
2. **Performance globale et benchmarking** : compare les classes d’actifs (stocks, cryptos, indices) et observe l’évolution globale du portefeuille, son alpha et sa composition au fil du temps.  


## Organisation du projet

Le projet est organisé de la manière suivante :

<img width="867" height="417" alt="image" src="https://github.com/user-attachments/assets/d71efece-4d32-4384-92c2-db38a13c2ef6" />



<img width="898" height="377" alt="image" src="https://github.com/user-attachments/assets/0d84b68c-e88d-44c0-a20e-add6b6e74581" />

---

## Pipeline du projet

1. **Extraction des données** : récupération des historiques d'actifs via l’API Yahoo Finance.  
2. **Transformation et enrichissement** : calcul des indicateurs financiers essentiels :
   - `daily_return`, `cumulative_return`
   - `volatility_20d`
   - `rolling_mean_50` et `rolling_mean_200`
   - `drawdown` et `max_drawdown`
   - `Sharpe ratio sur 20 jours`
3. **Stockage** : sauvegarde des données au format Parquet pour une ingestion facile dans Power BI.  
4. **Visualisation** : création de dashboards interactifs sur Power BI pour suivre la performance individuelle des actifs et celle du portefeuille global.


## Page 1 - Analyse par actif

Cette première page permet de filtrer les actifs du portefeuille pour analyser leurs performances individuelles :  

- Carte individuelle de chaque actif (ex. Amazon, Apple, Bitcoin) avec sa **valeur actuelle** et son **retour journalier moyen**.  
- Graphiques : évolution du **daily return**, **volatilité**, **Sharpe**, **drawdown**.  
- TriMap des **parts relatives des actions** dans le portefeuille.  
- Graphiques d’évolution de l’**alpha sur 60 jours** et du **portefeuille global**.  

**Capture d’écran de la page 1 :**  
<img width="1097" height="611" alt="image" src="https://github.com/user-attachments/assets/8c1c3511-1ba0-4843-9814-13c9a098bdc9" />


**Exemples d’indicateurs globaux du portefeuille sur 5 ans :**  
- Croissance du portefeuille : 1,48 
- Daily return moyen : 17  
- Volatilité 20 jours : 0,03  
- Sharpe 20 jours : -0,22  
- Drawdown moyen : -0,25  

---

## Page 2 - Performance globale et benchmarking

La deuxième page permet de comparer les classes d’actifs et d’analyser la performance globale :  

- Répartition du portefeuille :  
  - Actions : 50%  
  - Cryptomonnaies : 29,29%  
  - Indices : 20,16%  
- Graphiques d’évolution globale : valeur du portefeuille, alpha sur 60 jours, tendance des stocks, cryptos et indices.  
- Analyse des performances relatives : observation que cryptos et indices sont très volatiles, alors que les indices restent plus stables.  

**Capture d’écran de la page 2 :**  

<img width="1090" height="613" alt="image" src="https://github.com/user-attachments/assets/7d220e4e-5838-436a-af8f-e2de0f341f94" /> 

**Indicateurs globaux :**  
- Valeur actuelle du portefeuille : 15 366 $  
- Croissance globale : 2,97%  
- Daily return moyen : 17 $  
- Volatilité 20 jours : 0,03  
- Sharpe 20 jours : -0,22  
- Drawdown moyen : -0,25  

---

## Résultats et insights

Grâce à ce projet, il est possible de :  
- Identifier les actifs qui contribuent le plus à la performance.  
- Visualiser la dynamique globale du portefeuille et son risque.  
- Comparer les différentes classes d’actifs sur plusieurs années.  
- Fournir un outil exploitable par un investisseur pour suivre l’évolution de son portefeuille.  

---

## Auteur

**Aimé ADJEGUEDE** – passionné de data et de finance, spécialisé dans l’analyse de portefeuilles et la visualisation des données financières.  

**Prochaines étapes potentielles :**  
- Intégration d’un **entrepôt SQL Server** pour centraliser les données.  
- Mise en place d’une **pipeline CI/CD** pour automatiser la récupération et le traitement des données.  
- Développement d’une **application web (Django)** pour permettre une consultation dynamique et interactive des analyses, destinée aux investisseurs ou aux journalistes financiers.

---


