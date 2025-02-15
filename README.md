# 🌍 Rețele de Calculatoare - CoAP

![CoAP Logo](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-25/blob/main/.assets/logo2.png)

<h2 align="center">🌐 Client Interface CoAP implementation! 🌐</h2>
</p>
<br>
<p align="center">
<a href="https://discord.gg/BQb4rT3d"><img src="https://img.shields.io/badge/Join%20Our%20Discord-7289DA?logo=discord&logoColor=white&style=flat-square"></a>
<a href=""><img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square"></a>
<a href=""><img src="https://img.shields.io/badge/Code%20Quality-A-blue?style=flat-square"></a>
</p>

---
### 📄 Documentație
Autorii:  
- Arama Luigi-Emanuel  
- Lupu Gheorghe

## Cuprins
- [📝 Descriere](#-descriere)
- [🚀 Caracteristici principale](#-caracteristici-principale)
- [🔗 Modelul Cerere/Răspuns](#-modelul-cererăspuns)
- [🧩 Formatul Mesajelor](#-formatul-mesajelor)
- [🔢 Formatul Opțiunilor](#-formatul-opțiunilor)
- [🖥️ Componentele Sistemului](#️-componentele-sistemului)
- [📂 Funcționalități ale Clientului](#-funcționalități-ale-clientului)
- [🪽 Server CoAP Application Diagram](#-server-coap-application-diagram)
- [Legendă - Structura Aplicației Server CoAP](#legendă---structura-aplicației-server-coap)
- [🔥 Concluzii](#-concluzii)
- [💻 Bibliografie](#-bibliografie)

---

## 📝 Descriere

**The Constrained Application Protocol (CoAP)** este un protocol de internet special conceput pentru rețele și noduri constrânse. Este utilizat în aplicațiile **M2M** (*Machine-to-Machine*), cum ar fi automatizarea clădirilor și managementul energiei inteligente. Protocolul CoAP permite schimbul eficient de date între dispozitive cu resurse limitate, precum microcontrolere de 8 biți, și este compatibil cu **HTTP**, facilitând integrarea cu Web-ul.

---



   Acest internet protocol de tip CoAP este în mod special utilizat în realizarea retelelor constranse si transferarea protocoalelor cu noduri constranse. 
Nodurile de obicei se afla pe microcontrolere de 8 biti, pe un spatiu mic de ROM si RAM, in timp ce retelele constranse cum ar fi IPv6 
“Low-Power Wireless Personal Area Networks” au de obicei rate mari de eroare la transmiterea pachetelor si o viteza tipica de 10 kbit/s. 
Protocolul este conceput pentru aplicatii de tip machine-to-machine (M2M) cum ar fi energia inteligenta si automatizarea cladirilor.

   CoAP ofera un model de interactiune cerere/raspuns intre punctele finale ale aplicatiei, 
suporta descoperirea incorporata a serviciilor si resurselor si include concepte-cheie ale Web-ului, 
cum ar fi URI-urile si tipurile de media pe Internet. CoAP este conceput pentru a se intregra usor cu HTTP, 
permitand interconectarea cu Web-ul respectand in acelasi timp cerintele speciale, cum ar fi suportul pentru multicast, 
o incarcare redusa si simplitate pentru medii constranse.


                        +----------------------+
                        |      Application     |
                        +----------------------+
                        +----------------------+  \
                        |  Requests/Responses  |  |
                        |----------------------|  | CoAP
                        |       Messages       |  |
                        +----------------------+  /
                        +----------------------+
                        |          UDP         |
                        +----------------------+

                    Figure 1: Abstract Layering of CoAP

Aplicatia demonstrativa in cauza va urmari realizarea conexiunii intre Client-Server, codificarea metodelor implementate si transmiterea informatiilor/pachetelor catre server din intermediul aplicatiei de interfata. 

Componentele Clientului
  sistemul va include două componente principale:

Serverul: stocheaza fisierele trimise de client și gestionează structura de directoare. Acesta răspunde solicitarilor clientului prin protocoale de tip CoAP (Constrained Application Protocol).

Clientul: utilizeaza protocoale CoAP pentru a trimite si a recepționa date de la server, având o interfață grafică pentru navigarea și manipularea fișierelor.

## 🚀 Caracteristici principale

1. Protocol web conceput pentru aplicațiile M2M (Machine-to-Machine)
2. Se bazează pe UDP pentru comunicare rapidă
3. Suportă schimburi asincrone de mesaje
4. Overhead redus pentru antete, ideal pentru medii constrânse
5. Gestionarea deduplicării și gruparea pachetelor



### 🔗 Modelul Cerere/Răspuns
   In CoAP, fiecare mesaj include un cod de raspuns care indica starea solicitarii. Optiunile CoAP si, uneori, datele suplimentare din payload sunt folosite pentru a transmite informatii optionale. Raspunsurile la cereri pot fi trimise in acelasi mesaj cu cererea sau intr-un mesaj separat, în funcție de tipul mesajului..

- ✅ Mesaj Confirmabil (CON): Asigurǎ o transmitere sigurǎ, garantând livrarea cererii.
- ❌ Mesaj Non-confirmabil (NON): permite transmisii rapide, nesigure, potrivite pentru date ce nu necesită confirmare.

Metodele precum `GET`, `PUT`, `POST`, `DELETE`, și o metodă specifică, `RENAME` sunt implementate de CoAP.

## 🧩 Formatul Mesajelor
Mesajele CoAP sunt codificate într-un format binar compact, cu un antet de 4 biți urmat de un token cu dimensiune variabilǎ. Urmează opțiunile CoAP și, opțional, un marcaj de payload (0xFF) care indicǎ prezența datelor suplimentare.


                   0                   1                   2                   3
                   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                  |Ver| T |  TKL  |      Code     |          Message ID           |
                  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                  |                    Token (dacă există, TKL bytes)             |
                  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                  |                      Opțiuni (dacă există)                    |
                  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                  |1 1 1 1 1 1 1 1|      Payload (dacă există)                    |
                  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                 Figura 2: Formatul unui mesaj CoAP




1. **Versiune (Ver)**: 2 biți. Reprezintă versiunea CoAP (01 binar).
2. **Tip (T)**: 2 biți. Indicativul mesajului: CON (0), NON (1), ACK (2), RST (3).
3. **Lungimea Token-ului (TKL)**: 4 biți. Lungimea câmpului Token (0-8 biți).
4. **Cod**: 8 biți, cuprinzând clasa (3 biți) și detaliul (5 biți) formatat ca "c.dd".
5. **ID Mesaj**: 16 biți în ordinea rețelei. Identificator unic pentru fiecare mesaj.

### 🔢 Formatul Opțiunilor
Opțiunile sunt ordonate după număr și utilizează o codificare delta pentru a optimiza transmisia.

                 0   1   2   3   4   5   6   7
               +---------------+---------------+
               |  Option Delta | Option Length |   1 byte
               +---------------+---------------+
               |         Option Delta          |   0-2 bytes
               |          (extins)             |
               +-------------------------------+
               |         Option Length         |   0-2 bytes
               |          (extins)             |
               +-------------------------------+
               |         Option Value          |   0 sau mai mulți byți
               +-------------------------------+
                  Figura 2: Formatul Opțiunii  




## 🖥️ Componentele Sistemului
Sistemul include două părți:

- **Server**: Stochează fișierele trimise și răspunde solicitărilor CoAP.
- **Client**: Interfață grafică care trimite/primește date prin protocoale CoAP.

### 📂 Funcționalități ale Clientului
- **Navigare**: Cereri GET pentru a naviga structura de directoare.
- **Descărcare**: Descărcare fișiere cu cereri CoAP de tip GET.
- **Încărcare/Creare**: Transfer de fișiere cu cereri POST/PUT.
- **Ștergere**: Eliminare fișiere prin comenzi DELETE.
- **Redenumire**: Funcționalitate RENAME pentru fișiere și directoare.





## 🪽 Clien CoAP Application Diagram


      ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
      │                                       Session Creation                                           │
      └──────────────────────────────────────────────────────────────────────────────────────────────────┘
      
         ┌──────────────┐                       ┌─────────────┐                       ┌──────────────┐
         │ CoAP Client  │                       │   Gateway   │                       │ Mesh CoAP    │
         └──────────────┘                       └─────────────┘                       │ Server       │
                                                                                      └──────────────┘
      
         │                                   ┌───────────────────────┐                                   │
         │  POST                             │                       │                                   │
         │ coap://gateway/sessions           │                       │                                   │
         └──────────────────────────────────>│ Validate credentials  │                                   │
                                             │  and trust sender     │
                                             │         port          │
                                             │ <──────────────────────┘
                                             │      CREATED_201      │
                                             └────────────────────────┘
      
      
      ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
      │                                       Session Usage                                              │
      │                               (typically more than one request)                                  │
      └──────────────────────────────────────────────────────────────────────────────────────────────────┘
      
         ┌──────────────┐                       ┌─────────────┐                       ┌──────────────┐
         │ CoAP Client  │                       │   Gateway   │                       │ Mesh CoAP    │
         └──────────────┘                       └─────────────┘                       │ Server       │
                                                                                      └──────────────┘
      
         │                                   ┌───────────────────────┐                                   │
         │  GET Proxy-Uri:gateway            │                       │                                   │
         │ coap://device123/temp             │                       │                                   │
         └──────────────────────────────────>│ Sender port has       │                                   │
                                             │  session              │
                                             │  Queue message        │
                                             │  for send             │
                                             │                       │
                                             │         GET coap://device123/temp                         │
                                             └──────────────────────────────────────────────────────────>│
         │                                   │                       │                                   │
         │                                   │                       │       CONTENT_205                 │
         │<──────────────────────────────────────────────────────────────────────────────────────────────│
         │                       CONTENT_205                                                             │
         └──────────────────────────────────────────────────────────────────────────────────────────────<│
                                             
      
      ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
      │                                       Session Closure                                            │
      │                                          (when done)                                             │
      └──────────────────────────────────────────────────────────────────────────────────────────────────┘
      
         ┌──────────────┐                       ┌─────────────┐                       ┌──────────────┐
         │ CoAP Client  │                       │   Gateway   │                       │ Mesh CoAP    │
         └──────────────┘                       └─────────────┘                       │ Server       │
                                                                                      └──────────────┘
      
         │                                   ┌────────────────────────┐                                   │
         │  DELETE                           │                        │                                   │
         │ coap://gateway/sessions           │                        │                                   │
         └──────────────────────────────────>│ Stop trusting          │                                   │
                                             │ sender port            │
                                             │ <──────────────────────┘
                                             │      DELETED_202       │
                                             └────────────────────────┘


### Legendă - CoAP interfață

1. **CoAP Client** 🖥️: Aplicația care inițiază cereri către gateway pentru a obține date de la serverul Mesh CoAP.

2. **Session Creation** 🔐: Procesul de inițiere a unei sesiuni între client și gateway prin trimiterea unei cereri POST, urmată de verificarea și acceptarea conexiunii.

3. **Gateway** 🌉: Punctul de intermediere între client și server, responsabil de validarea sesiunilor și transmiterea cererilor către Mesh CoAP Server.

4. **Mesh CoAP Server** 🖧: Serverul care procesează cererile de la gateway și trimite răspunsuri cu datele solicitate (de exemplu, date de temperatură).

5. **Session Usage** 🔄: Etapa în care clientul face cereri GET către gateway pentru a accesa resurse pe serverul Mesh CoAP, iar gateway-ul transmite cererea mai departe.

6. **Proxy-Uri** 🔗: URI utilizat de client pentru a specifica resursa dorită prin gateway, facilitând comunicarea indirectă cu serverul Mesh CoAP.

7. **ACK** ✅: Mesaj de confirmare trimis de gateway pentru a confirma primirea unei cereri GET de la client.

8. **CONTENT_205** 📥: Răspunsul serverului cu conținutul solicitat (de exemplu, temperatura), trimis prin gateway către client.

9. **Session Closure** 🗑️: Procesul de închidere a sesiunii prin trimiterea unei cereri DELETE de la client către gateway, pentru a opri conexiunea și încrederea în portul clientului.

10. **DELETED_202** 🗑️: Mesaj de confirmare trimis de gateway pentru a indica închiderea cu succes a sesiunii.

---



## 🔥 Concluzii
Implementarea protocolului CoAP pentru client-server asigură o conexiune eficientă și adaptată pentru rețelele constrânse, cu o interfață prietenoasă pentru utilizatori. Compatibilitatea cu HTTP oferă flexibilitate, iar designul său ușor permite aplicarea într-o varietate de scenarii M2M. 🎉



## 💻 Bibliografie

- **RFC 7252**: [The Constrained Application Protocol (CoAP)](https://datatracker.ietf.org/doc/html/rfc7252#section-5.9.2) - Specificațiile oficiale ale protocolului CoAP.
- **ResearchGate**: [The constrained application protocol (CoAP) architecture](https://www.researchgate.net/figure/The-constrained-application-protocol-CoAP-EAP-architecture_fig3_298341986) - Un articol cu detalii despre arhitectura CoAP.

