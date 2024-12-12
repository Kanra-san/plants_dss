import os
import sqlite3
import json

def delete_database(db_path="plant_diseases.db"):  # Set up fresh database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database file '{db_path}' deleted successfully.")
    else:
        print(f"Database file '{db_path}' does not exist.")


delete_database()


# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect("plant_diseases.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS flowers (
    FlowerID INTEGER PRIMARY KEY,
    FlowerName TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS diseases (
    DiseaseID INTEGER PRIMARY KEY,
    DiseaseName TEXT,
    FlowerID INTEGER,
    Description TEXT,
    FOREIGN KEY (FlowerID) REFERENCES flowers(FlowerID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS symptoms (
    SymptomID INTEGER PRIMARY KEY,
    SymptomName TEXT,
    MinValue FLOAT,             
    MaxValue FLOAT,             
    MembershipParameters TEXT   
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS rules (
    RuleID INTEGER PRIMARY KEY,    
    DiseaseID INTEGER NOT NULL,    
    FOREIGN KEY (DiseaseID) REFERENCES diseases(DiseaseID)   
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS rule_conditions (
    RuleConditionID INTEGER PRIMARY KEY,
    RuleID INTEGER NOT NULL,
    SymptomID INTEGER NOT NULL,
    Condition TEXT NOT NULL,
    FOREIGN KEY (RuleID) REFERENCES rules(RuleID),
    FOREIGN KEY (SymptomID) REFERENCES symptoms(SymptomID)
)""")

# Commit and close connection
conn.commit()
conn.close()

def populate_database(db_path="plant_diseases.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def print_table(table):
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # Flowers
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Mieczyk')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Róża')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Goździk')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Aksamitka')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Gwiazdosz')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Chryzantema')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Jaśmin')")
    cursor.execute("INSERT INTO flowers (FlowerName) VALUES ('Storczyk')")

    # Diseases - mieczyk
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fuzarioza mieczyka (Fusarium oxysporum f. sp. Gladioli)', 1, ?)
    """, (json.dumps({
        "description": "Choroba powoduje skręcanie, zginanie, łukowatość, zahamowanie wzrostu, żółknięcie lub wysychanie liści, związane z gniciem korzeni i bulw w polu, jak i w przechowywaniu. W przechowywaniu choroba charakteryzuje się suchym gniciem, które często ogranicza się do podstawy bulwy. Po przekrojeniu bulw na pół, widać ciemne pasma promieniujące od podstawy bulwy przez miąższ, a w ciężkich przypadkach cała środek bulwy jest czarny i zgniły. Początkowa infekcja bulw może pochodzić z gleby lub z utajonej infekcji bulw z poprzedniego roku, szczególnie w niesprzyjających warunkach pogodowych. To prowadzi do powstawania jaskrawo żółtych pasów między żyłkami na liściach. Charakterystycznym objawem jest zginanie rośliny w kierunku geotropowym z oparzeniem końcówek liści, które zawsze zaczyna się w miejscu, gdzie bulwy wykazują objawy gnicia. Patogen może być przenoszony w zapasowych bulwach i cebulkach jako utajona infekcja. Rozprzestrzenia się również przez glebę, skażoną wodę oraz mszyce.",
        "recommendation": "Moczenie cebulek w wodzie o temperaturze 57,2°C przez maksymalnie 30 minut zmniejsza wystąpienie choroby, jeśli cebulki zostały wykopane w połowie kwietnia lub na początku lata i traktowane 6-10 tygodni po zbiorach. Opryskiwanie bulw przed sadzeniem lub po zbiorach 10-20% Benomylem lub 10-20% Tiabendazolem (TBZ) jest skuteczne. Zanurzenie bulw w 0,1% Carbendazimie przed sadzeniem również kontroluje chorobę. Ekstrakty roślinne z Allium sativum i Ocimum sanctum wykazały skuteczność w kontrolowaniu choroby w 61-67% (Tomar i Chandel, 2006)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna rdzenia lub gąbczasta (Botrytis gladiolorum)', 1, ?)
    """, (json.dumps({
        "description": "Choroba zaczyna się jako małe plamy, które rozwijają się w większe plamy pokryte pleśnią, ostatecznie zabijając liście. Objawy charakterystyczne to małe plamy z czerwonawymi brzegami i rdzawe przebarwienia na liściach i łodygach, a także jasnobrązowe do ciemnobrązowych plamy na kwiatach. Grzyb rozprzestrzenia się przez pędy naczyniowe łodyg i liści, w końcu powodując gnicie rdzenia bulw. Jest to grzyb glebowy, wysoce destrukcyjny, który atakuje rośliny podczas chłodnej i wilgotnej pogody, w temperaturze optymalnej od 13 do 15°C.",
        "recommendation": "Chorobę można skutecznie kontrolować stosując fungicydy takie jak Winclozolin i Benlate. Opryski Mancozebem (0,2%) również skutecznie kontrolują infekcję. Leczenie bulw gorącą wodą (52°C) jest skuteczne w eliminowaniu patogenu. Bulwy powinny być dokładnie wysuszone przed przechowywaniem."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Sucha zgnilizna lub zgnilizna szyjki (Stormatinia gladioli)', 1, ?)
    """, (json.dumps({
        "description": "Grzyb często wytwarza sklerocja, ale w naturze rzadko tworzy apotecja. Infekcja pochodzi z zakażonych bulw i sklerocjów. Wysoka proporcja zakopanych sklerocjów w glebie zwiększa rozprzestrzenianie choroby przez bliskie sadzenie. Zgnilizna sucha jest szeroko rozpowszechniona, atakuje rośliny gladioli w polu oraz bulwy w przechowywaniu, szczególnie w wilgotnych warunkach polowych, gdzie wcześniejsze żółknięcie prowadzi do śmierci roślin. Liście brązowieją od końców w dół, a przy podstawach gniją, prowadząc do zgnilizny szyjki, podczas gdy bulwy pozostają mocno przytwierdzone do łodygi. Zainfekowane bulwy mają liczne okrągłe, czarne plamy, z lekko uniesionymi brzegami, które mogą zlewać się, tworząc nieregularne obszary.",
        "recommendation": "Konieczne jest stosowanie rotacji upraw przez cztery do sześciu lat w celu usunięcia patogenów glebowych. Leczenie gorącą wodą jest skuteczne w eliminowaniu patogenu. Cebulki należy najpierw moczyć w zimnej wodzie przez 24 godziny, a następnie traktować gorącą wodą o temperaturze 54,5°C przez 30 minut. Bulwy należy traktować Tihramem lub Diklorem (0,3%)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna przechowalnicza (Penicillium gladioli)', 1, ?)
    """, (json.dumps({
        "description": "Choroba zwykle objawia się czarnym, brązowym, zielonkawym lub żółtawym wzrostem pleśni na bulwach w czasie przechowywania. W złych warunkach wentylacyjnych bulwy mogą gnić i wydzielać nieprzyjemny zapach. Infekcja występuje przez uszkodzenia, dlatego należy unikać ranienia bulw podczas kopania lub przenoszenia. ",
        "recommendation": "Po wykopaniu bulwy należy je traktować Tihramem 75 DS (0,3%) i odpowiednio leczyć w temperaturze 30-35°C przez 7-10 dni przed przechowywaniem w chłodni. Należy unikać wilgotnych warunków przechowywania, a także temperatur powyżej 50°C w chłodniach, ponieważ mogą one prowadzić do szybkiego gnicia bulw w wilgotnych warunkach."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Parch (Burkholderia gladioli pv. Gladioli)', 1, ?)
    """, (json.dumps({
        "description": "Na liściach objawy pojawiają się jako brązowo-żółte plamki. Na bulwach objawy występują zazwyczaj w postaci okrągłych, brązowych, wklęsłych zmian z uniesionymi brzegami. Plamy te rozwijają się bardziej obficie w dolnej części bulwy. Objawy zgnilizny szyjki pojawiają się jako liczne, brązowe do czarnych małe plamy w pobliżu podstawy roślin. Zmiany te często wydzielają gumowate wycieki. Patogen szybko się rozmnaża i rozprzestrzenia przez glebę lub może być przenoszony przez bulwy, roztocza i nicienie korzonkowe.",
        "recommendation": "Ponieważ choroba może być przenoszona przez roztocza, nicienie i inne owady glebowe, należy stosować insektycydy, takie jak Thimet, Furadan lub Temik, które należy aplikować w otwarte rowki przy sadzeniu przed przykryciem bulw glebą. Bulwy i cebulki należy moczyć w formaldehydzie (0,5%) przez 2 godziny, a następnie w 200 ppm Streptomycynie przez 2 godziny tuż przed sadzeniem. Zanurzenie bulw w zawiesinie Tihramu (0,2%) przez 15 minut również zapobiega infekcji."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści Curvularia (Curvularia trifolii f. sp. gladioli)', 1, ?)
    """, (json.dumps({
        "description": "Patogen występuje w glebie. Choroba szybko się rozprzestrzenia w wilgotnych warunkach. Choroba ta głównie atakuje liście, ale inne części rośliny również mogą zostać zaatakowane. Na liściach plamy początkowo są małe i okrągłe, ale później rozszerzają się głównie w kierunku żyłek. Są jasnobrązowe, otoczone ciemniejszymi, czerwono-brązowymi pierścieniami i żółtą halo. W centrum tych plam formują się czarne masy zarodników grzyba. Na łodydze plamy są brązowe, wydłużone i wklęsłe, mogą obejmować całą łodygę, co skutkuje złamaniem rośliny powyżej miejsca infekcji. Na bulwach również pojawiają się brązowe do czarnych plamy.",
        "recommendation": "Należy stosować zdrowe, wolne od chorób bulwy do sadzenia. Chorobę można kontrolować przez opryskiwanie Dithane M-45 w stężeniu 0,2%."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Guzowatość korzeni (Meloidogyne incognita i M. hapla)', 1, ?)
    """, (json.dumps({
        "description": "Rośliny wykazują opóźniony wzrost i stają się blade. Charakterystycznym objawem jest tworzenie się guzów na korzeniach roślin.",
        "recommendation": "Należy przeprowadzać głęboką orkę latem i stosować rotację upraw co najmniej przez 3 lata. Należy wprowadzić Thimet 10 G lub Temik 10 w ilości 12 kg granulek na akr do gleby."
    }),))

    # Diseases - róża
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mączniak prawdziwy (Sphaerotheca pannosa var. rosae)', 2, ?)
    """, (json.dumps({
        "description": "Choroba pojawia się, gdy dni są ciepłe, a noce chłodne. Pierwsze objawy występują na młodych liściach jako podniesione, pęcherzykowate obszary, które wkrótce pokrywają się szarym, białym, proszkowym wzrostem grzyba. Zainfekowane liście zwykle mają bardziej purpurowy odcień niż zdrowe. Nowe pędy ulegają zniekształceniu. W przypadku silnej infekcji końcówki pędów mogą wyschnąć. Często nieotwarte pąki stają się białe z powodu ataku mączniaka. Zainfekowane pąki nie otwierają się, a w otwartych kwiatach infekcja prowadzi do przebarwień i zniekształceń płatków. Ogólna witalność rośliny jest osłabiona. Głównym sposobem przezimowania grzyba jest infekcja uśpionych pąków (Price, 1970). Patogen wytwarza konidia w łańcuchach, które są łatwo rozprzestrzeniane przez powietrze, co powoduje rozprzestrzenianie się choroby.",
        "recommendation": "Chorobę można kontrolować poprzez opryskiwanie Bavistinem lub Benlate (0,1%) co 30 dni. Siarka koloidalna (0,2%), propikonazol (0,1%) i Karathane (0,05%) mogą być stosowane co 7-10 dni w celu zwalczania choroby. Siarki koloidalnej nie należy stosować, gdy temperatura dzienna przekracza 30°C. Grzyb antagonistyczny Sporothrix flocculosa okazał się wysoce skuteczny w kontrolowaniu choroby (Belanger et al., 1994). Tilletiopsis pallescens, drożdżak wytwarzający balistospory, wyizolowany z liści zainfekowanych mączniakiem, udowodnił swoją skuteczność przeciwko grzybowi. Biologiczny środek redukuje występowanie choroby o 97-98% (Na et al., 1997)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Obumieranie, (Diplodia rosarum)', 2, ?)
    """, (json.dumps({
        "description": "Usychanie pędów to jedna z głównych chorób róż. Choroba występuje w maksymalnej sile po przycinaniu pędów po monsunie. Powoduje obumieranie rośliny od końców pędów w dół. Starsze rośliny są bardziej narażone na atak w porównaniu z młodszymi. Charakterystyczne objawy choroby to brązowe zabarwienie, które jest widoczne po rozcięciu zainfekowanych pędów. Patogen dostaje się do tkanek rośliny przez drobne uszkodzenia spowodowane przez osy kopacze.",
        "recommendation": "Zainfekowane rośliny należy usunąć i spalić. Sekatory należy zdezynfekować alkoholem, a przycięte końce natychmiast pokryć pastą chaubatia, zawierającą 4 części węglanu miedzi, 4 części czerwonego ołowiu i 5 części oleju lnianego."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Czarna plamistość róży (Diplocarpon rosae (Ana: Marssonina rosae))', 2, ?)
    """, (json.dumps({
        "description": "Grzyb przezimowuje na opadłych liściach róż i zainfekowanych tkankach łodyg. Rola etapu doskonałego w cyklu życia patogenu nie jest dobrze zrozumiana. Optymalna temperatura i wilgotność względna dla kiełkowania konidiów i infekcji wynoszą odpowiednio 24°C i >85%. Główne objawy to plamki na liściach oraz ich żółknięcie, a następnie opadanie liści i drastyczne zmniejszenie liczby i rozmiaru kwiatów. Ciemnobrązowe do czarnych plamy występują głównie na górnej powierzchni liści i rzadko na dolnej powierzchni. W pełni rozwinięte plamy mają średnicę 7-12 mm, są okrągłe lub podokrągłe i zwykle wyraźnie oddzielone.",
        "recommendation": "Opryskiwanie Bavistinem (0,1%), a następnie Benlate (0,1%) co 15 dni okazało się bardzo skuteczne w kontrolowaniu choroby. Opryski Dithane M-45 i Dithane Z-78 (0,2%) również są pomocne."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Alternaria alternate)', 2, ?)
    """, (json.dumps({
        "description": "Choroba powoduje duże straty w sezonie deszczowym. Młodsze liście są bardziej podatne na infekcję. Małe, owalne do nieregularnych, matowe brązowe do czarnych plamki pojawiają się najpierw na brzegach liści, które później powiększają się, zlewają i pokrywają całą powierzchnię liścia. Patogen przezimowuje na zainfekowanych liściach i innych częściach rośliny. Temperatura 28-30°C i wysoka wilgotność sprzyjają rozwojowi choroby.",
        "recommendation": "Zainfekowane liście należy zbierać i spalić. Cztery opryski Benlate (0,06%), Captan (0,25%) lub Mancozeb (0,25%) co 10 dni w okresie grudzień-styczeń skutecznie kontrolują chorobę."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza róży (Phragmidium spp.)', 2, ?)
    """, (json.dumps({
        "description": "Choroba charakteryzuje się obecnością czerwonawo-pomarańczowych puchów na listkach i czasami na ogonkach liściowych. Kolor tych puchów zmienia się na czarny, gdy formują się teleutospory. W przypadkach ciężkiej infekcji dochodzi do opadania liści. Produkcja kwiatów przez zainfekowane rośliny jest znacznie zmniejszona. Patogen przezimowuje w formie teliosporów lub mycelium w zainfekowanej łodydze. Łagodne zimowe temperatury i opady deszczu sprzyjają wybuchom epidemii rdzy.",
        "recommendation": "Opadłe, zainfekowane liście należy zbierać i zniszczyć. Wiosenne przycinanie oraz oprysk roślin w stanie uśpienia miedzią oksychlorkiem (0,3%) są skuteczne w kontrolowaniu choroby. Chorobę można skutecznie kontrolować opryskiwaniem Dithane M-45 (0,2%), Vita vax (0,1%) lub Benodonilem (0,1%) trzy razy co 15 dni w okresie marzec-kwiecień. Dithiokarbamiany, oksykarboksyny i fungicydy hamujące biosyntezę ergosterolu zapewniają dobrą kontrolę nad rdzawymi chorobami róż (Shattock i Bhatti, 1983)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Szara pleśń (Botrytis cinerea)', 2, ?)
    """, (json.dumps({
        "description": "Grzyb głównie atakuje kwiaty i kwitnące pędy. Objawy są widoczne jako brązowe plamy na płatkach pąków kwiatowych, które powiększają się i pokrywają całą powierzchnię. Zainfekowane pąki opadają w dół. Wklęsłe, szaro-czarne zmiany rozprzestrzeniają się na łodygę od podstawy pąka. Czasami widoczne są objawy przypominające usychanie. Grzyb przezimowuje w formie mycelium lub sklerocjów w zainfekowanych resztkach roślin. Konidia są przenoszone przez powietrze i powodują rozprzestrzenianie się choroby. Przedłużone okresy wilgotności sprzyjają infekcji.",
        "recommendation": "Opryskiwanie Bavistinem (0,1%) lub Mancozebem (0,25%) okazało się skuteczne w kontrolowaniu choroby. Praktyki sanitarno-higieniczne mogą zmniejszyć występowanie choroby. Wszystkie opadłe liście, kwiaty i resztki roślin należy usunąć i zniszczyć. Trichoderma viride (PDBCTV 4) jest skuteczne w kontrolowaniu choroby. Sok czosnkowy w stężeniu 0,5-5% zmniejsza rozwój zgnilizny botrytis."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Antraknoza róży (Sphaceloma rosarum)', 2, ?)
    """, (json.dumps({
        "description": "Małe, okrągłe, brązowe plamki z purpurowym obrzeżem pojawiają się na liściach, które powiększają się i pokrywają całą blaszki liściowej, a silna infekcja prowadzi do całkowitego opadania liści. W niektórych przypadkach zainfekowana tkanka odpada, co daje liściom wygląd 'dziurawych liści'.",
        "recommendation": "Zbierać wszystkie zainfekowane liście i spalić. Chorobę można skutecznie kontrolować opryskiwaniem Benlate (0,1%)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mozaika róży (Wirus RMV)', 2, ?)
    """, (json.dumps({
        "description": "Mozaika róż występuje głównie na różach uprawianych w szklarniach. Choroba charakteryzuje się żółtymi lub białawymi chlorotycznymi liniami, pierścieniami, plamkami lub wzorcami mozaikowymi na liściach. Zainfekowane rośliny wykazują ogólny spadek kondycji, usychanie i przedwczesne opadanie liści.",
        "recommendation": "Zainfekowane rośliny należy zniszczyć i nigdy nie używać ich do rozmnażania. Należy używać materiału do szczepienia i szczepienia wolnego od wirusów."
    }),))

    # Diseases - goździk
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fuzarioza (Fusarium oxysporum f. sp. dianthi)', 3, ?)
    """, (json.dumps({
        "description": "Początkowe objawy choroby to żółknięcie liści oraz pojawienie się zniekształconych, wygiętych pędów. Łodygi stają się miękkie, łatwe do zgniecenia. Po przecięciu łodygi widać brązowe pasy lub strefy w rejonie naczyń. Cała roślina więdnie i opada w bardzo krótkim czasie.",
        "recommendation": "Ponieważ grzyb powodujący tę chorobę jest przenoszony przez glebę, pierwszym krokiem w kontroli jest unikanie skażonej gleby. Zastosowanie oprysku gleby oxychloridem miedzi (0,4%) i oprysk Bavistinem (0,1%) zmniejsza nasilenie choroby. Solarizacja gleby okazała się bardzo skuteczna w minimalizowaniu choroby. Środki biologiczne, takie jak Trichoderma harzianum, Pseudomonas fluorescens, Bacillus subtilis, Streptomyces sp. i izolat niepatogenny Fusarium zostały uznane za skuteczne przeciwko chorobie. Formulacje na bazie neem również wykazały skuteczność w walce z chorobą (Chandel i Tomar, 2008)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna podstawy rośliny (Phytophthora nicotianae var. parasitica, Pythium sp., Rhizoctonia solani, Sclerotinia sclerotiorum)', 3, ?)
    """, (json.dumps({
        "description": "Pod wysoką wilgotnością grzyby atakują korzenie i część szyjki łodygi w rejonie poziomu gleby, co później prowadzi do więdnięcia. Liście zmieniają kolor i zaczynają wysychać od dołu ku górze.",
        "recommendation": "Unikanie nadmiernej wilgotności gleby jest ważnym krokiem w strategii zarządzania chorobą. Leczenie gleby Benlate lub Iprodionem przeciwko Rhizoctonia solani oraz Fosetyl-Al i Metalaksylem przeciwko Pythium i Phytophthora jest skuteczne. Kontrola biologiczna za pomocą Trichoderma harzianum zmniejsza występowanie choroby o 70%."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Alternaria dianthi)', 3, ?)
    """, (json.dumps({
        "description": "Choroba powoduje jasnobrązowe plamy z purpurowymi brązowymi obrzeżami na liściach i łodygach. Pierwsze atakowane są dolne liście, a choroba postępuje ku górze. Po powiększeniu się plam, łączą się one, powodując zamieranie liści i ich przedwczesne obumieranie.",
        "recommendation": "Usuwać zainfekowane liście. Aplikacja foliarna Dithane M-45 (0,2%) lub Bavistin (0,1%) jest skuteczna w minimalizowaniu strat związanych z chorobą."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mycosphaerella dianthi', 3, ?)
    """, (json.dumps({
        "description": "Grzyb powoduje pojawianie się plam w kształcie pierścieni, które łączą się, rozszerzają i w końcu niszczą liście.",
        "recommendation": "Dithane M-45 (0,2%) lub Bavistin (0,1%) co 10 dni kontroluje chorobę."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna podstawy (Sclerotium rolfsii)', 3, ?)
    """, (json.dumps({
        "description": "Patogen infekuje łodygę na poziomie gleby, a później rozprzestrzenia się na liście, powodując zgniliznę łodygi. Na zainfekowanej części widać kłaczkowaty wzrost mycelium grzyba.",
        "recommendation": "Usuwać stare i zwiędłe liście dotykające gleby. Regulacja wilgotności gleby oraz unikanie nadmiernego nawożenia azotem pomaga w kontrolowaniu choroby. Należy podlać glebę w pobliżu podstawy łodygi Thiramem (0,25%) lub Carbendazimem (0,1%)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza (Uromyces dianthi)', 3, ?)
    """, (json.dumps({
        "description": "Na liściach, łodygach i pąkach kwiatowych widać wąskie, czekoladowo-brązowe puchy. Zainfekowane rośliny stają się karłowate, a ich liście zaczynają się zwijać.",
        "recommendation": "Należy utrzymywać suche liście. Opryskiwanie Dithane M-45 (0,2%) lub Bavistin (0,1%) oraz stosowanie Verticillium lecanii znacznie zmniejsza występowanie choroby."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Więdnięcie Phialophora (Phialophora cinerescens)', 3, ?)
    """, (json.dumps({
        "description": "Patogen powoduje stopniowe więdnięcie rośliny. Liście zainfekowanych roślin blakną i przybierają kolor słomy. Łodygi, po przecięciu, pokazują czekoladowe brązowe przebarwienia w rejonie naczyń. W zaawansowanej fazie infekcji można zauważyć więdnięcie całej rośliny.",
        "recommendation": "Zastosowanie oprysku gleby oxychloridem miedzi (0,4%) i oprysk Bavistinem (0,1%) zmniejsza nasilenie choroby. Solarizacja gleby okazała się bardzo skuteczna w minimalizowaniu choroby. Środki biologiczne, takie jak Trichoderma harzianum, Pseudomonas fluorescens, Bacillus subtilis, Streptomyces sp. i izolat niepatogenny Fusarium zostały uznane za skuteczne przeciwko chorobie. Formulacje na bazie neem również wykazały skuteczność w walce z chorobą (Chandel i Tomar, 2008)."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Szara pleśń (Botrytis cinerea)', 3, ?)
    """, (json.dumps({
        "description": "Choroba jest bardzo powszechna w czasie cięcia goździków. Pod wysoką wilgotnością grzyb powoduje wodniste plamy na zewnętrznych płatkach kwiatów, które stopniowo obejmują cały kwiat.",
        "recommendation": "Opryskiwanie gleby i roślin Bavistinem (0,1%) zmniejsza intensywność choroby. Biofungicyd Mycostop (Streptomyces griseoviridis) okazał się skuteczny w minimalizowaniu choroby."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna łodygi (Fusarium roseum f.sp. cerealis)', 3, ?)
    """, (json.dumps({
        "description": "Choroba występuje w wyniku uszkodzeń spowodowanych ciągłym zbiorem. Często obserwuje się gnicie łodygi na poziomie gleby lub wyżej na roślinie. Zgnilizna na podstawie łodygi powoduje więdnięcie rośliny.",
        "recommendation": "Ponieważ choroba jest przenoszona przez glebę, fumigacja gleby i solarizacja gleby okazały się skuteczne w kontrolowaniu choroby. Opryskiwanie Benomylem lub Bavistinem (0,1%) również kontroluje chorobę."
    }),))

    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Więdnięcie bakteryjne (Burkholderia caryophylli)', 3, ?)
    """, (json.dumps({
        "description": "Liście stają się szarozielone, następnie żółkną, a na końcu dochodzi do więdnięcia rośliny. Inne objawy to przebarwienie naczyń, wypływ bakteryjny i gnicie korzeni. Rośliny można łatwo wyjąć z gleby.",
        "recommendation": "Należy stosować materiał roślinny wolny od chorób. Gleba powinna być sterylizowana. Usuwanie zainfekowanych roślin. Unikać nawadniania nadziemnego."
    }),))

    # Diseases - aksamitka
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgorzel siewek (Rhizoctonia solani)', 4,  ?)
    """, (json.dumps({
        "description": "Objawy pojawiają się jako brązowe, martwicze plamy, otaczające korzeń, które później rozprzestrzeniają się na pęd główny (plumule) i powodują zamieranie przedwschodowe. Objawy po wschodach pojawiają się na dolnej części hipokotylu w postaci wodnistych, brązowych, martwiczych pierścieni, prowadzących do zapadania się siewek. Po wyciągnięciu zainfekowanych siewek system korzeniowy wydaje się częściowo lub całkowicie zgnity.",
        "recommendation": "W celu zarządzania problemem należy zapewnić odpowiedni drenaż na zagonie siewnym. Zaleca się podlanie gleby roztworem Karbendazymu (0,1%). Należy również stosować rotację upraw w cyklu trzy-czteroletnim."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści, zaraza (Alternaria spp. – A. tagetica, A. alternata; Cercospora spp.; Septoria spp.)', 4,  ?)
    """, (json.dumps({
        "description": "Na dolnych liściach pojawiają się drobne, brązowe, okrągłe plamki, które w późniejszym stadium infekcji powiększają się, prowadząc do przedwczesnego opadania liści, zmniejszenia wielkości kwiatów, a ostatecznie do zamierania roślin.",
        "recommendation": "Aby kontrolować chorobę, należy opryskiwać uprawy aksamitki preparatem Dithane M-45 w stężeniu 0,2% lub Karbendazymem (0,05%) co dwa tygodnie, rozpoczynając od momentu pojawienia się pierwszych objawów choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mączniak prawdziwy (Oidium sp., Leveillula taurica)', 4,  ?)
    """, (json.dumps({
        "description": "Na liściach pojawiają się białe, drobne, powierzchowne plamki, które z czasem pokrywają całe nadziemne części rośliny białym nalotem.",
        "recommendation": "Chorobę można zwalczać, opryskując rośliny preparatem Karathane w stężeniu 0,05% lub Sulfexem (3 g/l wody) co dwa tygodnie."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna pąków kwiatowych (Alternaria dianthi)', 4,  ?)
    """, (json.dumps({
        "description": "Choroba występuje głównie na młodych pąkach kwiatowych, powodując ich suche gnicie z brązowymi, przypalonymi, martwiczymi przebarwieniami działek kielicha i łodygi. Kwiaty języczkowe i rurkowate również brązowieją. W późniejszych stadiach pąki marszczą się, ciemnieją i wysychają. Objawy są mniej widoczne na dojrzałych pąkach, ale takie pąki nie otwierają się. Na brzegach i końcówkach starszych liści widoczne są brązowe, martwicze plamy.",
        "recommendation": "Aby zwalczyć tę chorobę, należy regularnie opryskiwać rośliny preparatem Dithane M-45 w stężeniu 0,2%."
    }),))

    # Diseases - gwiazdosz
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fuzarioza (Fusarium oxysporum f. sp. callistephi, Verticillium albo-atrum)', 5,  ?)
    """, (json.dumps({
        "description": "Choroba charakteryzuje się zahamowaniem wzrostu, żółknięciem liści, a następnie więdnięciem rośliny i gniciem okolicy szyjki korzeniowej. Po przecięciu łodygi zainfekowanej rośliny widoczny jest brązowy pierścień naczyniowy, szczególnie po stronie najbardziej dotkniętej chorobą. Takie rośliny ostatecznie więdną.",
        "recommendation": "Ponieważ grzyb zimuje w glebie i może być przenoszony na wszystkich częściach zainfekowanych roślin, nasiona zebrane z chorych roślin muszą zostać odkażone, podobnie jak gleba, w której będą sadzone. Bardzo skuteczne w zapobieganiu chorobie okazało się moczenie nasion przez 30 minut w 0,1% roztworze chlorku rtęci oraz parowa sterylizacja gleby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna szyjki korzeniowej (Phytophthora cryptogea)', 5,  ?)
    """, (json.dumps({
        "description": "Łodygi i korzenie zainfekowanej rośliny wydają się nasiąknięte wodą i czarne. Zgnilizna spowodowana przez grzyb jest bardziej wyraźna i nie ma różowego nalotu zarodników charakterystycznego dla roślin zainfekowanych przez więdnięcie.",
        "recommendation": "Środki zapobiegawcze obejmują ścisłe ograniczenie nawadniania oraz unikanie sadzenia w pobliżu roślin żywicielskich alternatywnych. Jeśli to możliwe, nie należy sadzić roślin na polu, na którym wystąpiła choroba w poprzednich latach. Jeśli konieczne jest wykorzystanie tych samych zagonów, gleba powinna zostać wysterylizowana."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Szara pleśń (Botrytis cinerea)', 5,  ?)
    """, (json.dumps({
        "description": "Objawy choroby obejmują zarazę kwiatów, gnicie pąków, raka łodygi, zgniliznę łodyg i korony, zarazę liści oraz zgorzel siewek. W wilgotnych warunkach porażona tkanka zaczyna gnić. Na tych tkankach można zaobserwować szarą lub brązową grzybnię. Choroba rozprzestrzenia się szybko w chłodnej i wilgotnej pogodzie.",
        "recommendation": "Chorobę można ograniczyć poprzez stosowanie lekkiej, dobrze zdrenowanej gleby. Zainfekowane rośliny, ich części oraz chwasty powinny być usunięte i zniszczone. Należy unikać nadmiernego zagęszczenia roślin i podlewania z góry. Nasiona powinny być suszone w temperaturze 18–20°C. W celu zwalczania choroby należy wykonać 3–4 opryski preparatami Mancozeb (0,25%) lub Chlorothalonil (0,2%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza (Coleosporium asterum)', 5,  ?)
    """, (json.dumps({
        "description": "Na dolnej powierzchni liści, szczególnie u młodych roślin, pojawiają się jaskrawe, żółtopomarańczowe plamy. Początkowo plamy te są pokryte cienką warstwą tkanki roślinnej, ale w miarę dojrzewania stają się pękające, odsłaniając pomarańczowoczerwone, pylące masy zarodników. Wzrost zainfekowanych roślin zostaje zahamowany, a jakość kwiatów ulega pogorszeniu.",
        "recommendation": "Zainfekowane części roślin powinny zostać zebrane i zniszczone. Należy unikać nawadniania roślin za pomocą zraszaczy. Opryskiwanie siarką zwilżalną w okresie wegetacji jest skuteczne w zwalczaniu choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Ascochyta asteris, Septoria callistephi, Stemphylium callistephi)', 5, ?)
    """, (json.dumps({
        "description": "Plamy początkowo są żółtawe, a następnie ciemnobrązowe i czarne, stopniowo powiększając się. Najpierw zakażeniu ulegają dolne liście. W przypadku silnej infekcji zainfekowane liście zamierają i opadają na ziemię. Jakość kwiatów ulega pogorszeniu.",
        "recommendation": "Zainfekowane części roślin powinny zostać zebrane i spalone. Nasiona przed siewem należy zaprawić preparatem Thiram (0,2%) lub Karbendazym (0,1%). Chorobę można skutecznie zwalczać, stosując opryski Dithane M-45 (0,2%) w odstępach tygodniowych."
    }),))

    # Diseases - chryzantema
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zaraza bakteryjna (Erwinia chrysanthemi)', 6, ?)
    """, (json.dumps({
        "description": "Patogen powoduje więdnięcie roślin w słoneczne dni. W miarę rozprzestrzeniania się choroby wierzchołki łodyg brunatnieją, stają się kruche i załamują się. Łodyga staje się pusta w środku z brunatnymi smugami rozciągającymi się aż do podstawy.",
        "recommendation": "Metody minimalizacji choroby obejmują niszczenie zainfekowanych roślin, sterylizację gleby, stosowanie zdrowych sadzonek oraz unikanie zanieczyszczeń podczas uszczykiwania. Skuteczne jest opryskiwanie preparatem Streptocycline (0,01%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Bakteryjna plamistość liści (Pseudomonas cichorii)', 6, ?)
    """, (json.dumps({
        "description": "Liście zainfekowanej rośliny wykazują ciemnobrązowe do czarnych, lekko zapadnięte plamy z koncentrycznymi strefami. W miarę rozwoju plamy łączą się, tworząc duże martwicze obszary. W zaawansowanym stadium bakteria atakuje pąki kwiatowe, które ciemnieją i zamierają przedwcześnie.",
        "recommendation": "Skuteczne jest stosowanie zdrowych sadzonek oraz opryskiwanie preparatem Streptocycline (0,01%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna korzeni (Pythium spp. i Phytophthora spp.)', 6, ?)
    """, (json.dumps({
        "description": "Korzenie ulegają zniszczeniu. Zainfekowane rośliny są zahamowane w wzroście i przybierają bladożółty kolor. Zainfekowane rośliny można łatwo wyciągnąć z gleby.",
        "recommendation": "Wśród praktyk agrotechnicznych ważne są solarizacja gleby, usuwanie zainfekowanych roślin oraz zapewnienie dobrego drenażu. Zalecane fungicydy do zwalczania choroby to: Metalaksyl, Mancozeb, Captan i Fosetyl-Al."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna korzeni Phoma (Phoma chrysanthemi)',6, ?)
    """, (json.dumps({
        "description": "Zainfekowane rośliny wykazują zahamowanie wzrostu, żółknięcie dolnych liści oraz pękanie głównej łodygi.",
        "recommendation": "Podlewanie gleby tlenochlorkiem miedzi (0,3%) na dwa tygodnie przed sadzeniem zapewnia dobrą kontrolę choroby. Skuteczne w zwalczaniu choroby okazało się również traktowanie gleby izolatami Trichoderma (T 8 B, T5B, T73B, T P5, T 40 i T 20B)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna podstawy rośliny (Rhizoctonia solani)', 6, ?)
    """, (json.dumps({
        "description": "Choroba jest bardzo powszechna w ciepłych i wilgotnych warunkach. Atak grzyba powoduje miękką, brązową zgniliznę łodyg i liści.",
        "recommendation": "Sterylizacja gleby oraz podlewanie fungicydami miedziowymi zapewniają skuteczną kontrolę choroby. Biofungicyd wytworzony z połączenia Bacillus subtilis i Kaslin został zgłoszony jako skuteczny w ochronie przed zgorzelą podstawy łodyg. Ponadto, opryskiwanie młodych roślin lub ich zanurzanie w Benomylu (0,2%) zapewnia ochronę."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna łodygi (Fusarium solani)', 6, ?)
    """, (json.dumps({
        "description": "Zainfekowane rośliny wykazują martwicę liści oraz rozkład i przebarwienia rdzenia oraz przyległych naczyń w korze. Grzyb powoduje powstawanie małych, ciemnych zmian u podstawy łodygi. W zaawansowanych stadiach infekcji obserwuje się rozkład korzeni.",
        "recommendation": "Zaleca się traktowanie gleby Dithane M-45 lub fungicydem miedziowym przed sadzeniem w celu zwalczania choroby. Skuteczne jest również opryskiwanie preparatem Bavistin (0,1%) w celu minimalizacji choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fuzarioza (Fusarium oxysporum f. sp. chrysanthemi)', 6, ?)
    """, (json.dumps({
        "description": "Infekcja powoduje chlorozy i martwicę, które zaczynają się od dolnych liści. Łodyga w pobliżu poziomu gleby staje się czarna, a brązowe przebarwienia rozprzestrzeniają się na drewno łodygi na znacznej wysokości ponad ziemią. Ostatecznie cała roślina więdnie i zamiera.",
        "recommendation": "Skuteczne w minimalizowaniu choroby okazało się traktowanie gleby tiophanatem metylu."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mączniak prawdziwy (Erysiphe cichoracearum)', 6, ?)
    """, (json.dumps({
        "description": "Pojawienie się białego, mączystego nalotu na górnych powierzchniach liści jest głównym objawem diagnostycznym choroby. Patogen atakuje również łodygę i kwiaty.",
        "recommendation": "W celu zwalczania choroby zaleca się opryskiwanie preparatem Karathane (0,025%), Bavistinem (0,1%) lub fungicydem na bazie siarki (0,2%) oraz zapewnienie suchego środowiska."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza (Puccinia chrysanthemi)', 6, ?)
    """, (json.dumps({
        "description": "Choroba charakteryzuje się pojawieniem się małych pęcherzyków wielkości główki szpilki na spodniej stronie liści. Pęcherzyki występują również w mniejszym stopniu na górnej powierzchni liści. Pęcherzyki pękają, odsłaniając ciemnobrązową, pylącą masę zarodników.",
        "recommendation": "Zainfekowane liście należy usuwać z rośliny natychmiast po zauważeniu i spalać. Należy unikać podlewania z góry. Opryskiwanie preparatem Mancozeb (0,2%) skutecznie minimalizuje występowanie choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Więdnięcie verticillium (Verticillium dahliae i V. albo-atrum)', 6, ?)
    """, (json.dumps({
        "description": "Początkowe objawy choroby to żółknięcie i brązowienie dolnych liści. Stopniowo kolejne liście ulegają infekcji, stają się brązowe i obumierają. Zainfekowane rośliny są zahamowane w wzroście i często nie wydają kwiatów.",
        "recommendation": "Regularne ogrzewanie lub chemiczne traktowanie gleby pomaga zminimalizować występowanie choroby. Skutecznym sposobem ograniczenia choroby jest również solarizacja gleby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Szara pleśń (Botrytis cinerea)', 6, ?)
    """, (json.dumps({
        "description": "Patogen atakuje kwiaty w wilgotnych szklarniach, powodując powstawanie brązowych, wodnistych plam. Zainfekowane części pokrywają się szarobrązową, pylącą masą zarodników",
        "recommendation": "Środki zapobiegawcze obejmują zapewnienie lepszej wentylacji i dobrej cyrkulacji powietrza poprzez odpowiednie odległości między roślinami. Skuteczne jest również opryskiwanie preparatem Bavistin (0,1%) oraz tlenochlorkiem miedzi (0,2%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Septoria chrysanthemi)',6, ?)
    """, (json.dumps({
        "description": "Objawy choroby pojawiają się na liściach w postaci żółtawych plam, które później stają się ciemnobrązowe i czarne. Plamy powiększają się, zwiększają swoją liczbę, zlewają się ze sobą i tworzą duże obszary obejmujące znaczną część liścia w wilgotnych warunkach. Poważna infekcja może prowadzić do przedwczesnego więdnięcia liści.",
        "recommendation": "Środki zapobiegawcze obejmują zbieranie i niszczenie zainfekowanych liści. Skuteczne jest stosowanie Bavistinu (0,01%) lub Benlate (0,01%) w celu zahamowania infekcji. Należy unikać nadmiernego nawadniania."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zaraza Ascochyta - czarna zgnilizna (Ascochyta chrysanthemi)', 6, ?)
    """, (json.dumps({
        "description": "Infekcja prowadzi do powstawania czarnych zmian na łodygach i dolnych liściach, które z czasem powiększają się, tworząc nieregularne czarne plamy. Powoduje również brązowienie płatków i pędów kwiatowych, które po sczernieniu opadają.",
        "recommendation": "Wśród metod agrotechnicznych najlepszym sposobem na zmniejszenie intensywności choroby jest utrzymanie czystości na polu. Zanurzanie sadzonek w Benlate (0,1%) oraz opryskiwanie Bavistinem, Benlate lub fungicydem miedziowym zapewnia skuteczną kontrolę choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość języczkowatych kwiatów (Stemphylium lycopersici)',6, ?)
    """, (json.dumps({
        "description": "Infekcja powoduje powstawanie brązowych lub białych martwiczych plamek otoczonych kolorowymi aureolami na kwiatach języczkowych. Atak choroby jest szczególnie nasilony przy wysokiej wilgotności i temperaturze.",
        "recommendation": "W celu zwalczania choroby zaleca się stosowanie preparatów Dithane M-45 (0,2%), Bavistin (0,1%) lub tlenochlorku miedzi. Należy unikać nadmiaru wilgoci poprzez zapewnienie lepszej wentylacji w szklarni."
    }),))

    # Diseases - jaśmin
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zaraza liści (Cercospora jasminicola, Alternaria jasmini)', 7, ?)
    """, (json.dumps({
        "description": "Choroba szybko rozprzestrzenia się w porze deszczowej. Na górnej powierzchni liści pojawiają się czerwonobrązowe, okrągłe plamy o średnicy 2–8 mm. Zainfekowane brzegi liści zwijają się do wewnątrz, stają się twarde i kruche. W przypadku silnej infekcji pąki wegetatywne i młode gałęzie zamierają.",
        "recommendation": "W celu zwalczania choroby należy opryskiwać rośliny Bavistinem (0,1%) lub tlenochlorkiem miedzi (0,3%) w odstępach miesięcznych, począwszy od maja aż do cięcia. Zainfekowane liście powinny być zebrane i spalone."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza (Uromyces hobsoni)', 7, ?)
    """, (json.dumps({
        "description": "Na liściach pojawiają się pomarańczowe, powietrzne kubeczki po obu stronach liści, choć przeważnie na spodniej powierzchni. W zaawansowanym stadium infekcji powstają liczne pęcherze, które powodują żółknięcie i marszczenie liści. Zainfekowane są również łodygi i gałęzie, co prowadzi do pękania kory i ostatecznie do obumierania gałęzi.",
        "recommendation": "Zainfekowane rośliny i ich części należy usunąć. Chorobę można zwalczać przez pylenie siarką w dawce 20–25 kg/ha. Zaleca się również opryskiwanie mieszanką Bordeaux lub tlenochlorkiem miedzi (0,3%) w celu kontroli choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fuzarioza (Fusarium solani, sclerotium rolfsii)', 7, ?)
    """, (json.dumps({
        "description": "Początkowym objawem choroby jest żółknięcie dolnych liści, które stopniowo rozprzestrzenia się ku górze, ostatecznie prowadząc do obumarcia rośliny. Choroba występuje w skupiskach. U podstawy zainfekowanej rośliny widoczna jest sieć wachlarzowatych strzępek grzybni, która później tworzy brązowe sklerocja przypominające nasiona gorczycy. W przypadku więdnięcia sklerotialnego, oprócz wyżej wymienionych objawów, białe grzybnie zwykle oplatają korzenie, a sklerocja przylegają do korzeni więdnących roślin.",
        "recommendation": "Podlewanie gleby wokół roślin 1% mieszanką Bordeaux zapobiega rozprzestrzenianiu się choroby. Skuteczne w zwalczaniu więdnięcia sklerotialnego są również Pseudomonas fluorescens, Bacillus subtilis i Trichoderma viride. Zastosowanie talcowych komercyjnych preparatów P. fluorescens w dawce 20 g/doniczkę oraz B. subtilis i T. viride w dawce 25 g/doniczkę znacząco zmniejszyło występowanie choroby w eksperymentach doniczkowych."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Fulvia fulva)', 7, ?)
    """, (json.dumps({
        "description": "Objawy choroby pojawiają się na górnej powierzchni liści w postaci jasnożółtych plam, które z czasem przybierają oliwkowobrązowy kolor. Zainfekowane liście ulegają zamieraniu wskutek zlewania się wielu plam.",
        "recommendation": "Brak danych"
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Alternaria (Alternaria alternata)', 7, ?)
    """, (json.dumps({
        "description": 'Na blaszce liściowej pojawiają się nieregularne brązowe zmiany otoczone ciemnymi pasami, które czasami prowadzą do powstania objawu "dziurkowatości liści" (ang. Shot hole symptom).',
        "recommendation": "Brak danych"
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści Phoma (Phoma harbarum)', 7, ?)
    """, (json.dumps({
        "description": "Infekcja objawia się w postaci małych, okrągłych, jasnobrązowych plamek, które później zlewają się, tworząc brązowe do popielatych martwicze obszary. W starszych zmianach obserwuje się objawy 'dziurkowatości liści' (Shot hole symptoms).",
        "recommendation": "Brak danych"
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zaraza liści Glomerella (Glomerella cingulata)', 7, ?)
    """, (json.dumps({
        "description": "Na liściach i gałązkach pojawiają się nieregularne, wodniste, ciemnobrązowe plamy. Zlewanie się tych plam na liściach i gałązkach prowadzi do objawów zamierania (ang. blighting symptoms).",
        "recommendation": "Opryskiwanie Bavistinem (0,1%) lub tlenochlorkiem miedzi (0,3%) w odstępach miesięcznych, począwszy od maja aż do cięcia, pomaga w zwalczaniu choroby. Zainfekowane liście należy zebrać i spalić."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Mozaika (Wirus)', 7, ?)
    """, (json.dumps({
        "description": "Chore rośliny wykazują zahamowanie wzrostu i żółtozielony wygląd z małymi liśćmi. Na liściach pojawiają się nieregularnie rozmieszczone żółtozielone do chlorotycznych plamki o średnicy 1–2 mm, które tworzą wzory w kształcie pierścieni.",
        "recommendation": "Kontrola wektora owadziego za pomocą Metasystox (0,1%) zapobiega przenoszeniu choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Fyllodia (Phytoplasma)', 7, ?)
    """, (json.dumps({
        "description": "Zainfekowane rośliny produkują zdeformowane, zredukowane, zielonkawe struktury przypominające kwiaty zamiast pachnących białych kwiatów na wiechach, które stają się bardzo zagęszczone i zielone. Zielonkawe płatki korony są zredukowane i mają jajowaty kształt. Części kwiatowe przekształcają się w struktury przypominające liście.",
        "recommendation": "Chorobę można kontrolować przez opryskiwanie roślin roztworem chlorowodorku tetracykliny (250 ppm). Sadzonki z zainfekowanych roślin nie powinny być używane do sadzenia."
    }),))

    # Diseases - storczyk
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Plamistość liści (Gloeosporium sp., Colletotrichum sp., Cercospora sp. i Phyllostictina sp.)', 8, ?)
    """, (json.dumps({
        "description": "Grzyby powodują powstawanie ciemnobrązowych plam o różnych rozmiarach na liściach. Ciepła, wilgotna pogoda i brak światła sprzyjają przetrwaniu patogenu.",
        "recommendation": "Usuwanie i niszczenie zainfekowanych liści zapobiega rozprzestrzenianiu się choroby. Skuteczne jest opryskiwanie preparatem Dithane M-45 (0,2%) lub Bavistinem (0,1%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna czarna Pythium (Pythium ultimum)', 8, ?)
    """, (json.dumps({
        "description": "Grzyb atakuje siewki, szczególnie w wilgotnych warunkach pogodowych. Zainfekowane rośliny czernieją, a liście zaczynają opadać.",
        "recommendation": "Chore liście i rośliny należy usunąć i zniszczyć. Wstrzymanie podlewania na kilka dni oraz przeniesienie rośliny do mniej wilgotnego miejsca pomaga ograniczyć rozwój choroby. W celu zwalczania choroby należy zastosować fungicydy, takie jak Metalaksyl (0,1%), Fosetyl-Al lub Mancozeb (0,2%)."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Zgnilizna serca (Phytophthora palmivora)', 8, ?)
    """, (json.dumps({
        "description": "Patogen atakuje pseudobulwy, co prowadzi do żółknięcia i opadania liści. Po przecięciu pseudobulwy widoczne są ciemne, zgniłe obszary. Choroba występuje u gatunków takich jak Cattleya, Phalaenopsis i Vanda.",
        "recommendation": "Zainfekowane rośliny należy usunąć. Aby zapobiec rozprzestrzenianiu się choroby, należy zastosować opryski systemicznymi fungicydami, takimi jak Fosetyl-Al i Metalaksyl."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Szara pleśń (Botrytis cinerea) ', 8, ?)
    """, (json.dumps({
        "description": "Odmiany Cattleya, Phalaenopsis, Dendrobium, Oncidium i Vanda są podatne na tę chorobę. Infekcja pojawia się na płatkach kwiatów jako małe, wodniste, brązowe plamy, które szybko się powiększają. W zaawansowanym stadium całe kwiaty, a czasami także liście, mogą być pokryte szarawą pleśnią.",
        "recommendation": "Aby kontrolować chorobę, należy unikać nadmiernej wilgotności, utrzymywać wysoką temperaturę i zapewnić dobrą wentylację. Zainfekowane części roślin powinny zostać usunięte i zniszczone. Opryskiwanie roślin preparatami Dithane M-45 (0,2%) lub Bavistin (0,1%) w regularnych odstępach czasu jest skuteczne w zwalczaniu choroby."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Rdza (Hemileia americana)', 8, ?)
    """, (json.dumps({
        "description": "Rdza wywołana przez grzyb Hemileia Americana charakteryzuje się pojawieniem się pomarańczowo-żółtych pęcherzyków na spodniej stronie liści. Na górnej powierzchni liści, bezpośrednio nad pęcherzykami, pojawiają się żółtozielone chlorotyczne obszary.",
        "recommendation": "Zainfekowane liście należy usunąć i spalić. Liście można oprószyć siarką lub opryskać siarką zwilżalną, aby zwalczyć chorobę."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Więdnięcie storczyków (Sclerotium rolfsii)', 8, ?)
    """, (json.dumps({
        "description": "Początkowym objawem jest żółknięcie podstawy liści, które później brązowieją. Infekcja pseudobulw prowadzi do gnicia i obumierania całej rośliny.",
        "recommendation": "Wszystkie zainfekowane liście należy natychmiast usunąć i spalić. Bardzo skutecznym środkiem w zwalczaniu choroby okazały się preparaty oparte na Trichoderma sp.."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Bakteryjna zgnilizna miękka (Erwinia carotovora)', 8, ?)
    """, (json.dumps({
        "description": "Objawy choroby pojawiają się w postaci małych, okrągłych, pęcherzykowatych plam o ciemnozielonym kolorze na górnej powierzchni liści. Infekcja prowadzi do miękkiej, mazistej i nieprzyjemnie pachnącej zgnilizny pseudobulw. Jest to poważna choroba storczyków z rodzaju Cattleya.",
        "recommendation": "W celu zarządzania zgnilizną miękką zaleca się stosowanie Streptocycline w stężeniu 0,1%."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Bakteryjna brązowa plama (Xanthomonas cattleyae)', 8, ?)
    """, (json.dumps({
        "description": "Choroba atakuje rośliny w każdym wieku. Początkowe objawy pojawiają się na liściach w postaci małych, wodnistych plamek. Plamy powiększają się, zlewają ze sobą i powodują zamieranie dużej części liścia, który następnie opada. Patogen może również zaatakować naczynia przewodzące wodę, co prowadzi do załamania całej rośliny.",
        "recommendation": "Wszystkie zainfekowane rośliny należy usunąć i natychmiast zniszczyć. Rozprzestrzenianie się choroby można zapobiec poprzez wielokrotne opryskiwanie preparatami Agrimycin lub Tetracycline."
    }),))
    cursor.execute("""
        INSERT INTO diseases (DiseaseName, FlowerID, Description)
        VALUES ('Choroby wirusowe (Do najczęstszych należą wirus mozaiki Cymbidium (CyMV), wirus mozaiki tytoniu-0 (TMV-0) oraz wirus pierścieniowej plamistości Odontoglossum (ORSV))', 8, ?)
    """, (json.dumps({
        "description": "Wiele wirusów atakuje storczyki. Do najczęstszych należą Cymbidium mosaic virus (CyMV), Tobacco mosaic virus-0 (TMV-0) oraz Odontoglossum ring spot virus (ORSV). Te wirusy powodują martwicę liści objawiającą się pierścieniami, smugami i nieregularnymi wzorami barw (mozaiką). W ciężkich przypadkach może dochodzić do deformacji liści i kwiatów, plamistości oraz skręcania.",
        "recommendation": "- Wszystkie chore rośliny należy usunąć natychmiast po ich wykryciu.\n"
                          "- Przez cały sezon wegetacyjny należy kontrolować populacje owadów.\n"
                          "- W celu zwalczania mszyc i innych owadów przenoszących choroby należy stosować opryski preparatem Malathion.\n"
                          "- Do rozmnażania należy używać wyłącznie materiału nasadzeniowego wolnego od wirusów."
    }),))


    # healthy states
    cursor.execute("""
            INSERT INTO diseases (DiseaseName, FlowerID, Description)
            VALUES ('Roślina wygląda na zdrową', 1, ?)
        """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
            INSERT INTO diseases (DiseaseName, FlowerID, Description)
            VALUES ('Roślina wygląda na zdrową', 2, ?)
        """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 3, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 4, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 5, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 6, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 7, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))
    cursor.execute("""
                INSERT INTO diseases (DiseaseName, FlowerID, Description)
                VALUES ('Roślina wygląda na zdrową', 8, ?)
            """, (json.dumps({
        "description": "Brak symptomów wsazujących na występowanie choroby - roślina wygląda na zdrową.",
        "recommendation": "Sytuacja nie wymaga rekomendacji leczenia. Dobra robota!"
    }),))

    symptoms_data = [
        # Leaf Color
        {"SymptomName": "Leaf Color",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "Normal", "points": [0, 0, 2, 4]},
                 {"label": "Yellowing", "points": [3, 5, 7, 8]},
                 {"label": "Brown", "points": [7, 9, 10, 10]}
             ]
         }
         },
        # Petal Color
        {"SymptomName": "Petal Color",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "Normal", "points": [0, 0, 2, 4]},
                 {"label": "Pale", "points": [2, 4, 6, 7]},
                 {"label": "Green", "points": [4, 6, 8, 9]},
                 {"label": "Brown", "points": [7, 9, 10, 10]}

             ]
         }
         },
        # Bulb Condition
        {"SymptomName": "Bulb Condition",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "triangular",
             "functions": [
                 {"label": "Normal", "points": [0, 3, 6]},
                 {"label": "Rotten", "points": [5, 7, 10]}
             ]
         }
         },
        # Smell
        {"SymptomName": "Smell",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "triangular",
             "functions": [
                 {"label": "Normal", "points": [0, 3, 6]},
                 {"label": "Rotting", "points": [5, 7, 10]}
             ]
         }
         },
        # Defoliation
        {"SymptomName": "Defoliation",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "triangular",
             "functions": [
                 {"label": "None", "points": [0, 0, 3]},
                 {"label": "Partial", "points": [2, 5, 8]},
                 {"label": "Severe", "points": [6, 10, 10]}
             ]
         }
         },
        # Lesions on Stems
        {"SymptomName": "Lesions on Stems",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "None", "points": [0, 0, 2, 4]},
                 {"label": "Spots", "points": [3, 5, 7, 8]},
                 {"label": "Streaks", "points": [7, 9, 10, 10]}
             ]
         }
         },
        # Root Weakness or Rotting
        {"SymptomName": "Root Weakness or Rotting",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "triangular",
             "functions": [
                 {"label": "No Weakness", "points": [0, 0, 3]},
                 {"label": "Moderate Weakness", "points": [2, 5, 8]},
                 {"label": "Severe Rotting", "points": [6, 10, 10]}
             ]
         }
         },
        # Slowed Growth
        {"SymptomName": "Slowed Growth",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "triangular",
             "functions": [
                 {"label": "Normal", "points": [0, 0, 3]},
                 {"label": "Slow", "points": [2, 5, 8]},
                 {"label": "Stunted", "points": [6, 10, 10]}
             ]
         }
         },
        # Leaf Spots - Size
        {"SymptomName": "Leaf Spots - Size",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "None", "points": [0, 0, 2, 3]},
                 {"label": "Small", "points": [2, 4, 6, 7]},
                 {"label": "Medium", "points": [4, 6, 8, 9]},
                 {"label": "Large", "points": [7, 9, 10, 10]}
             ]
         }
         },
        # Leaf Spots - Kind
        {"SymptomName": "Leaf Spots - Kind",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "None", "points": [0, 0, 1, 2]},
                 {"label": "Lines", "points": [1, 1, 2, 4]},
                 {"label": "Rings", "points": [3, 5, 6, 7]},
                 {"label": "Spots", "points": [6, 7, 8, 9]},
                 {"label": "Holes", "points": [8, 9, 10, 10]}
             ]
         }
         },
        #Spotting on Petals
        {
            "SymptomName": "Spotting on Petals",
            "MinValue": 0,
            "MaxValue": 10,
            "MembershipParameters": {
                "type": "triangular",
                "functions": [
                    {"label": "No Spotting", "points": [0, 2, 4]},
                    {"label": "Spotting", "points": [3, 5, 10]}
                ]
            }
        },
        # Fungus growth
        {
            "SymptomName": "Fungus Growth Spots",
            "MinValue": 0,
            "MaxValue": 10,
            "MembershipParameters": {
                "type": "trapezoidal",
                "functions": [
                    {"label": "No Growth", "points": [0, 0, 2, 4]},
                    {"label": "Small Growth", "points": [3, 5, 7, 8]},
                    {"label": "Large Growth", "points": [7, 9, 10, 10]}
                ]
            }
        },
        # Spore masses
        {
            "SymptomName": "Spore Masses",
            "MinValue": 0,
            "MaxValue": 10,
            "MembershipParameters": {
                "type": "triangular",
                "functions": [
                    {"label": "No Spores", "points": [0, 0, 3]},
                    {"label": "Few Spores", "points": [2, 5, 8]},
                    {"label": "Abundant Spores", "points": [6, 10, 10]}
                ]
            }
        },
        # Spot Color Scale - YORB
        {"SymptomName": "Spot Color Scale - YORB",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "N/A", "points": [0, 0, 1, 2]},
                 {"label": "Yellow", "points": [1, 1, 2, 4]},
                 {"label": "Orange", "points": [3, 5, 6, 7]},
                 {"label": "Red", "points": [6, 7, 9, 10]},
                 {"label": "Brown", "points": [8, 9, 10, 10]}
             ]
         }
         },
        # Spot Color Greyscale - WGB
        {"SymptomName": "Spot Color Greyscale - WGB",
         "MinValue": 0, "MaxValue": 10,
         "MembershipParameters": {
             "type": "trapezoidal",
             "functions": [
                 {"label": "N/A", "points": [0, 0, 1, 2]},
                 {"label": "White", "points": [1, 1, 2, 4]},
                 {"label": "Grey", "points": [3, 5, 6, 8]},
                 {"label": "Black", "points": [7, 8, 9, 10]}
             ]
         }
         }
    ]

    for symptom in symptoms_data:
        cursor.execute("""
            INSERT INTO symptoms (SymptomName, MinValue, MaxValue, MembershipParameters)
            VALUES (?, ?, ?, ?)
        """, (
            symptom["SymptomName"],
            symptom["MinValue"],
            symptom["MaxValue"],
            json.dumps(symptom["MembershipParameters"])
        ))

    # print_table('symptoms')

    rules_data = [ #  gladiolus diseases
        {"DiseaseID": 1, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Defoliation", "Condition": "Severe"},
            {"SymptomName": "Bulb Condition", "Condition": "Rotten"},

        ]},
        {"DiseaseID": 2, "conditions": [
            {"SymptomName": "Fungus Growth Spots", "Condition": "Large Growth"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Orange"},
            {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},

        ]},
        {"DiseaseID": 3, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Brown"},
            {"SymptomName": "Bulb Condition", "Condition": "Rotten"},

        ]},
        {"DiseaseID": 4, "conditions": [
            {"SymptomName": "Fungus Growth Spots", "Condition": "Large Growth"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Black"},
            {"SymptomName": "Smell", "Condition": "Rotting"},
            {"SymptomName": "Leaf Color", "Condition": "Brown"},
            {"SymptomName": "Bulb Condition", "Condition": "Rotten"},

        ]},
        {"DiseaseID": 5, "conditions": [
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Bulb Condition", "Condition": "Normal"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},

        ]},

        {"DiseaseID": 6, "conditions": [
            {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
            {"SymptomName": "Spore Masses", "Condition": "Few Spores"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},

        ]},
        {"DiseaseID": 7, "conditions": [
            {"SymptomName": "Petal Color", "Condition": "Pale"},
            {"SymptomName": "Slowed Growth", "Condition": "Slow"},

        # rose diseases
        ]},
        {"DiseaseID": 8, "conditions": [
            {"SymptomName": "Petal Color", "Condition": "Pale"},
            {"SymptomName": "Fungus Growth Spots", "Condition": "Large Growth"},
            {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"}

        ]},
        {"DiseaseID": 9, "conditions": [
            {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}

        ]},
        {"DiseaseID": 10, "conditions": [
            {"SymptomName": "Defoliation", "Condition": "Severe"},
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Spot Color Greyscale - YORB", "Condition": "Brown"}

        ]},
        {"DiseaseID": 11, "conditions": [
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}

        ]},
        {"DiseaseID": 12, "conditions": [
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Orange"},
            {"SymptomName": "Defoliation", "Condition": "Severe"},
            {"SymptomName": "Slowed Growth", "Condition": "Slow"},

        ]},
        {"DiseaseID": 13, "conditions": [
            {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
            {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
            {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Black"}

        ]},
        {"DiseaseID": 14, "conditions": [
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Defoliation", "Condition": "Severe"},

        ]},
        {"DiseaseID": 15, "conditions": [
            {"SymptomName": "Defoliation", "Condition": "Severe"},
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Rings"},
            {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"}
        ]},
        #carnation diseases
        {"DiseaseID": 16, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Lesions on Stems", "Condition": "Streaks"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}
        ]},
        {"DiseaseID": 17, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
        ]},
        {"DiseaseID": 18, "conditions": [
            {"SymptomName": "Defoliation", "Condition": "Severe"},
            {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
            {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}
        ]},
        {"DiseaseID": 19, "conditions": [
            {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}
        ]},
        {"DiseaseID": 20, "conditions": [
            {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},
            {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"}
        ]},
        {"DiseaseID": 21, "conditions": [
            {"SymptomName": "Slowed Growth", "Condition": "Stunted"},
            {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
            {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}
        ]},
        {"DiseaseID": 22, "conditions": [  # double with another disease
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Lesions on Stems", "Condition": "Streaks"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"}
        ]},
        {"DiseaseID": 23, "conditions": [
            {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
            {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"}
        ]},
        {"DiseaseID": 24, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
            {"SymptomName": "Lesions on Stems", "Condition": "Streaks"},
        ]},
        {"DiseaseID": 25, "conditions": [
            {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
        ]},
        # marigold diseases
        {
            "DiseaseID": 26,
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                       ]
        },
        {
            "DiseaseID": 27,
            "conditions": [
                {"SymptomName": "Defoliation", "Condition": "Severe"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Slowed Growth", "Condition": "Slow"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 28,
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"},
            ]
        },
        {
            "DiseaseID": 29,
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
            ]
        },

        # china aster (gwiazdosz)
        {
            "DiseaseID": 30,
            "conditions": [
                {"SymptomName": "Slowed Growth", "Condition": "Slow"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
            ]
        },
        {
            "DiseaseID": 31,
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Black"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
            ]
        },
        {
            "DiseaseID": 32,
            "conditions": [
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Grey"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},            ]
        },
        {
            "DiseaseID": 33,
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Orange"},
                {"SymptomName": "Spore Masses", "Condition": "Abundant Spores"},

            ]
        },
        {
            "DiseaseID": 34,
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Defoliation", "Condition": "Severe"},
            ]
        },
        # chrysanthemum
        {
            "DiseaseID": 35,
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Streaks"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 36,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Brown"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 37,
            "conditions": [
                {"SymptomName": "Slowed Growth", "Condition": "Slow"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Moderate Weakness"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            ]
        },
        {
            "DiseaseID": 38,
            "conditions": [
                {"SymptomName": "Slowed Growth", "Condition": "Slow"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            ]
        },
        {
            "DiseaseID": 39,
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Large"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},            ]
        },
        {
            "DiseaseID": 40, # fusarium solani
            "conditions": [
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Large"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
            ]
        },
        {
            "DiseaseID": 41,
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Large"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            ]
        },
        {
            "DiseaseID": 42, # powdery mildew
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"},
            ]
        },
        {
            "DiseaseID": 43,  # rust
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Spore Masses", "Condition": "Abundant Spores"},

            ]
        },
        {
            "DiseaseID": 44,  # verticilium
            "conditions": [
                {"SymptomName": "Slowed Growth", "Condition": "Stunted"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
                {"SymptomName": "Defoliation", "Condition": "Partial"},
            ]
        },
        {
            "DiseaseID": 45,  # bortrytis
            "conditions": [
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Grey"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},
                {"SymptomName": "Spore Masses", "Condition": "Abundant Spores"},
            ]
        },
        {
            "DiseaseID": 46,  # septoria
            "conditions": [
                {"SymptomName": "Slowed Growth", "Condition": "Stunted"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
                {"SymptomName": "Defoliation", "Condition": "Partial"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
            ]
        },
        {
            "DiseaseID": 47,  # ascochyta
            "conditions": [
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
                {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Black"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
            ]
        },
        {
            "DiseaseID": 48,  # stemphylium
            "conditions": [
                {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"},
            ]
        },

        # jasmine
        {
            "DiseaseID": 49,  # Cercospora jasminicola, Alternaria jasmini
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
            ]
        },
        {
            "DiseaseID": 50,  # rust
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Orange"},
                {"SymptomName": "Spore Masses", "Condition": "Abundant Spores"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            ]
        },
        {
            "DiseaseID": 51,  # fusarium
            "conditions": [
                {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "White"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "Severe Rotting"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            ]
        },
        {
            "DiseaseID": 52,  # fulvia fulva
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Yellow"},
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
            ]
        },
        {
            "DiseaseID": 53,  # alternaria
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Holes"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 54,  # phoma
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 55,  # glomerella
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Lesions on Stems", "Condition": "Spots"},
            ]
        },
        {
            "DiseaseID": 56,  # mosaic
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Rings"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Yellow"},
                {"SymptomName": "Slowed Growth", "Condition": "Slow"},
            ]
        },
        {
            "DiseaseID": 57,  # phytoplasma
            "conditions": [
                {"SymptomName": "Petal Color", "Condition": "Green"},
            ]
        },

        # orchid
        {
            "DiseaseID": 58,  # gleosporium
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Medium"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 59,  # pythium
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Large"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Greycale - WGB", "Condition": "Black"},
                {"SymptomName": "Defoliation", "Condition": "Severe"},
            ]
        },
        {
            "DiseaseID": 60,  # phytophtora
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
                {"SymptomName": "Defoliation", "Condition": "Severe"},
                {"SymptomName": "Bulb Condition", "Condition": "Rotten"},
            ]
        },
        {
            "DiseaseID": 61,  # bortrytis
            "conditions": [
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "Grey"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},
                {"SymptomName": "Spotting on Petals", "Condition": "Spotting"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },
        {
            "DiseaseID": 62,  # rust
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Yellow"},
            ]
        },
        {
            "DiseaseID": 63,  # sclerotium
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Yellowing"},
                {"SymptomName": "Defoliation", "Condition": "Partial"},
                {"SymptomName": "Bulb Condition", "Condition": "Rotten"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "Small Growth"},
            ]
        },
        {
            "DiseaseID": 64,  # erwinia
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Large"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Bulb Condition", "Condition": "Rotten"},
                {"SymptomName": "Smell", "Condition": "Rotting"},
            ]
        },
        {
            "DiseaseID": 65,  # xanthomonas
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
                {"SymptomName": "Defoliation", "Condition": "Partial"},
            ]
        },
        {
            "DiseaseID": 66,  # viral virus diseases
            "conditions": [
                {"SymptomName": "Leaf Spots - Size", "Condition": "Small"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "Spots"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "Brown"},
            ]
        },



        # healthy states
        {
            "DiseaseID": 67,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 68,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 69,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 70,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 71,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 72,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 73,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        },
        {
            "DiseaseID": 74,
            "conditions": [
                {"SymptomName": "Leaf Color", "Condition": "Normal"},
                {"SymptomName": "Petal Color", "Condition": "Normal"},
                {"SymptomName": "Bulb Condition", "Condition": "Normal"},
                {"SymptomName": "Smell", "Condition": "Normal"},
                {"SymptomName": "Defoliation", "Condition": "None"},
                {"SymptomName": "Lesions on Stems", "Condition": "None"},
                {"SymptomName": "Root Weakness or Rotting", "Condition": "No Weakness"},
                {"SymptomName": "Slowed Growth", "Condition": "Normal"},
                {"SymptomName": "Leaf Spots - Size", "Condition": "None"},
                {"SymptomName": "Leaf Spots - Kind", "Condition": "None"},
                {"SymptomName": "Spotting on Petals", "Condition": "No Spotting"},
                {"SymptomName": "Fungus Growth Spots", "Condition": "No Growth"},
                {"SymptomName": "Spore Masses", "Condition": "No Spores"},
                {"SymptomName": "Spot Color Scale - YORB", "Condition": "N/A"},
                {"SymptomName": "Spot Color Greyscale - WGB", "Condition": "N/A"}
            ]
        }
    ]

    for rule in rules_data:
        cursor.execute("""
            INSERT INTO rules (DiseaseID)
            VALUES (?)
        """, (rule["DiseaseID"],))
        rule_id = cursor.lastrowid
        for condition in rule["conditions"]:
            cursor.execute("""
                INSERT INTO rule_conditions (RuleID, SymptomID, Condition)
                SELECT ?, SymptomID, ?
                FROM symptoms WHERE SymptomName = ?
            """, (rule_id, condition["Condition"], condition["SymptomName"]))

    print_table('rules')
    print_table('rule_conditions')

    # Commit and close
    conn.commit()
    conn.close()
    print("Database populated successfully.")

# Run the population script
populate_database()


#def test_database(db_path="plant_diseases.db"):
    #conn = sqlite3.connect(db_path)
    #cursor = conn.cursor()

   #cursor.execute("SELECT * FROM flowers")
    #print("Flowers:", cursor.fetchall())

    #cursor.execute("SELECT * FROM diseases")
    #print("Diseases:", cursor.fetchall())

    #cursor.execute("SELECT * FROM symptoms")
    #print("Symptoms:", cursor.fetchall())

    #cursor.execute("SELECT * FROM rules")
    #print("Rules:", cursor.fetchall())

    #cursor.execute("SELECT * FROM rule_conditions")
    #print("Conditions:", cursor.fetchall())

    #conn.close()

# Test the database
# test_database()


# do każdej rośliny trzeba będzie dodać przypadek zdrowy, może jeszcze przypadek zwykłego przysychania z braku podlania