# OPG Knežević
## Kristian Knežević - završni projekt

Stranica OPG Knežević napravljena je za predstavljanje pčelinjih proizvoda. 
Također omogućen je detaljniji uvid u kvalitetu svakog pojedinog prozvoda na 
način da je opisano od čega se sve sastoje naši proizvodi, kako se koriste i kako pozitivno utječu na zdravlje.
Na početnoj stranici nalaze se fotografije pčelinjaka u Bootstrap elementu "Carousel" koje se same izmjenjuju svake 3 sekunde.
Iduća stranica pod nazivom "Proizvodi" sadrži već spomenuti opis proizvoda. Stranica "Cjenik" sadrži tablicu s cjenama proizvoda za količinu u kojoj se može kupiti određeni proizvod. I ne posljednjoj stranici "Tečaj" nalazi se opis upisa u tečaj pčeranja i sve što pritom treba ispuniti. Uz to prikazana je i trenutna vremenska prognoza za mjesto Rovanjska gdje se odvija tečaj pčelarenja.
    
</br>
</br> 

## Preuzimanje materijala s gita
Da biste kod ove web stranice povukli na svoje računalu potrebno je napraviti novu mapu na svom računalu.
Zatim otvoriti jednu od konzola, npr. "Git Bash" u novoj mapi --> desni klik i odaberite "Git Bash Here"
Redoslijed narebi u konzoli za povačenje materijala s Git Hub-a: git init --> git pull <em> link repozitorija </em>

</br>
</br> 

## Instalacija i pokretanje (VS Code)
Materijal se nakon preuzimanja otvori u VS Code (proizvoljno). Zatim se otvori Terminal i slijede naredbe:
python -m venv venv --> .\venv\Scripts\Activate.ps1 --> pip install --upgrade pip --> pip install -r .\requirements.txt.
Nakon instalacije potrebno je pokrenuti aplikaciju s naredbama: $env:FLASK_DEBUG="true" --> flask run.
Ako je sve prošlo bez pogrešaka potrebno je otvoriti jedan od web preglednika, otići na http://127.0.0.1:5000/ gdje se bi se trebala
pojaviti stranica koja zahtjeva obavezan unos imena i prezimena.

</br>
</br> 

## Korišeni Bootstrap elementi
>> Navabr <https://getbootstrap.com/docs/4.1/components/navbar/>  
>> Footer <https://mdbootstrap.com/docs/jquery/navigation/footer/>  
>> Card <https://getbootstrap.com/docs/4.5/components/card/>  
>> Carousel <https://getbootstrap.com/docs/4.5/components/carousel/>  
>> Image <https://getbootstrap.com/docs/4.4/content/images/>  
>> Table <https://getbootstrap.com/docs/4.4/content/tables/>  
>> Builder <https://mdbootstrap.com/docs/jquery/forms/builder/>   


</br>
</br>

## Registracija novog korisnika
Korisnik unosi svoje podatke(ime, prezime, email i lozinka). 
Podatci se spremaju u bazu podataka po jedinstvenim ID-em.
Lozinka se ne sprema u izvornom obliku nego u hash kako nebi bila lako čitljiva, a na taj način korisnici i njihovi računi dobivaju na sigurnosti.
Svaki novi korisnik mora imati jedinstvenu e-mail adresu. Ukoliko je unesena e-mail adresa već korištena korisnik će biti obaviješten.
Ako je registracija ispravna korisnik se preusmjerava na stranicu za prijavu.

</br>
</br>

## Prijava na stranicu
Nakon registracije novog korisnika može se prjaviti na stranicu s podatcima koje je prethodno unio u bazu podataka.
Ako nešto od unesenih podataka nije ispravno korisnik će biti obaviješten.

</br>
</br>

## Migracije
Aplikacija ima ugrađene migracije koje služe za stvaranje skripti za bazu podataka.
Skripte služe kako bi netko, ako mu je potrebno, mogao dolaziti do određenih verzija baze podataka u vremenu.
Prilikom promjene baze podataka sripta se radi naredbom --> flask db migrate -m "some message".
Baza se može unaprijediti(flask db upgrade) ili vratiti na prijašnje verzije(flask db downgrade).

</br>
</br>

## Controler
App.py je python datoteka koja sadrži uvoz svih potrebnih komponenti za rad aplikacije.
Unutar ove datoteke još se nalaze klasa za stvaranje WTFormi, rute do svake pojedine stranice, filteri i error stranice.



</br>
</br>

 ## Header
Header svake stranice sadrži izbornik za prijelaz s jedne na drugu stranicu.
Header je također i responzivan što omogućuje Bootstrap, a nakon smanjenja veličine zaslona izbornik postaje padajuć.

</br>
</br>

 ## Footer
Footer sadrži podatke za kontakt.
Stvorena je mogućnost direktnog zvanja samo klikom na ikonu telefona ili slanja e-maila klikom na ikonu e-mail.
Ikone su preuzete s [Font Awesome](https://fontawesome.com/)

</br>
</br>

## Base.html
Base.html sasdrži sve zajedničke komponente svih stranica koje budu njezini "potomci".
Određena stanica naslijedi Base.html kako bi pokupila komponente.
Ovako cijelokupna aplikacija dobiva na brzini, a kod je puno pregledniji.
Sadržaj koji se odnosi na svaku pojedinu stranicu unosi se u "block" dio koji se stvori u Base.html i stranici koja ju naslijeđuje.
Ovako izgleda "block" dio:
> -  {% block content %}
> 
> -  {% endblock %}



</br>
</br>

 ## Ostali korišteni izvori
>
> - YouTube
> - W3Schools
> - sadržaj s predavanja
> - Stack Overflow
> - Flask - WTF
> - Weather API



</br>
</br>

## Slike i Logo
>
> - dio slika preuzet je s interneta, ostale su originalne
> - Logo je napravljen samostalno uz pomoć GIMP-a

</br>
</br>
