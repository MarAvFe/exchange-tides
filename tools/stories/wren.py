"""Bad Powder - Tobias Wren, 1694. Three acts: The Verdict (1-7), The Carrier (8-14), Coat or No Coat (15-21)."""
from sk import *

npc("nan", ("Nan Strand", "Nan Strand"), "crew", True, 16941, "portrait_sailor")
npc("kip", ("Kip Wade, powder boy", "Kip Wade, mozo de pólvora"), "crew", False, 16942, "portrait_sailor")
npc("dorn", ("Felix Dorn", "Felix Dorn"), "merchant", False, 16943, "portrait_merchant")
npc("pruett", ("Joss Pruett, master of the Hammerhead", "Joss Pruett, patrón del Martillo"), "crew", False, 1694, "portrait_sailor")
npc("thorne", ("Governor Magnus Thorne", "Gobernador Magnus Thorne"), "governor", False, 16944, "portrait_governor")

enemy("powder_tender", ("The Tallow", "El Sebo"), 70, 5, 1.0, 64, 7000, "ship_sloop_pirate", 6)
enemy("hammerhead", ("The Hammerhead", "El Martillo"), 120, 9, 0.9, 66, 15000, "ship_brigantine_pirate", 7)
enemy("black_gull", ("The Black Gull", "La Gaviota Negra"), 280, 20, 0.8, 72, 45000, "ship_frigate_navy", 11)

item("caked_powder", ("Caked Powder Cask", "Barril de pólvora apelmazada"),
     ("Salvage from the Resolute, branded with a hammer over a wave. It crumbles like wet sand.", "Restos de la Resoluta, con la marca de un martillo sobre una ola. Se desmenuza como arena mojada."))
item("copied_page", ("Copied Ledger Page", "Página copiada del libro"),
     ("Quill's copy: six spoiled casks signed out to the Resolute by Captain S. Grimmer.", "La copia de Quill: seis barriles estropeados enviados a la Resoluta con la firma del capitán S. Grimmer."))
item("raider_powder", ("Raider Powder Sample", "Muestra de pólvora corsaria"),
     ("Fine Admiralty-grade powder, scraped out of a raider's magazine.", "Pólvora fina, de calidad del Almirantazgo, rascada del pañol de un corsario."), "combat_player_accuracy(+3)")
item("dorn_schedule", ("Dorn's Schedule", "El calendario de Dorn"),
     ("Where the Hammerhead anchors, month by month, in a frightened clerk's hand.", "Dónde fondea el Martillo, mes a mes, con la letra de un escribiente asustado."))
item("hammerhead_manifest", ("The Hammerhead's Manifest", "Manifiesto del Martillo"),
     ("Every cask the Hammerhead carried, and who paid for it. You know raiders' powder when you see it.", "Cada barril que llevó el Martillo, y quién lo pagó. Reconoces la pólvora corsaria en cuanto la ves."), "combat_player_accuracy(+5)")
item("quill_affidavit", ("Quill's Affidavit", "Declaración jurada de Quill"),
     ("Hester Quill's sworn statement on the Ironreef ledger, witnessed and sealed.", "La declaración jurada de Hester Quill sobre el libro de Arrecife de Hierro, con testigos y sello."))

GRIMMER = ("Captain Silas Grimmer", "Capitán Silas Grimmer")
QUILL = ("Hester Quill, mill clerk", "Hester Quill, escribiente del molino")

STORY = campaign("bad_powder", ("Bad Powder", "Pólvora podrida"), 1694,
 ("1694. Three months ago the frigate Resolute fought raiders off Isla Brasa, and two of her guns burst on the first broadside. Four gunners died. The board blamed her master gunner, Tobias Wren, and put him ashore with a sloop and a discharge paper. Wren knows how a gun bursts. He has seen the powder.",
  "1694. Hace tres meses la fragata Resoluta se batió con corsarios frente a Isla Brasa, y dos de sus cañones reventaron en la primera andanada. Murieron cuatro artilleros. El tribunal culpó a su maestro artillero, Tobias Wren, y lo dejó en tierra con una balandra y una hoja de licenciamiento. Wren sabe cómo revienta un cañón. Ha visto la pólvora."),
 ("Name Cleared", "Nombre limpio"),
 ("The board struck out your discharge, and the four families shook your hand on the quay. Silas Grimmer sailed away a commodore. You kept the Hammerhead's manifest in oilskin under your bunk, and you never stopped reading the news from the outer Reach.",
  "El tribunal anuló tu licenciamiento, y las cuatro familias te estrecharon la mano en el muelle. Silas Grimmer zarpó convertido en comodoro. Guardaste el manifiesto del Martillo envuelto en hule bajo tu litera, y nunca dejaste de leer las noticias del Estrecho exterior."),
[
 # ---------------- Act I: The Verdict
 chapter("discharged", ("Discharged", "Licenciado"), 0, {"p1": "other,has:shipwright"}, [
  say("governor", ("Your papers, Mister Wren. The board finds the Resolute's guns were overloaded by careless hands. You may trade in the Reach. You may not wear the coat again, and you will not set foot in Driftmoor or Isla Brasa while the families are grieving.",
                   "Sus papeles, señor Wren. El tribunal concluye que los cañones de la Resoluta se cargaron de más por descuido. Puede comerciar en el Estrecho. No volverá a vestir la casaca, y no pisará Brumaria ni Isla Brasa mientras las familias estén de luto."),
      ("The guns were loaded right. The powder was rotten.", "Los cañones estaban bien cargados. La pólvora estaba podrida.")),
  log(("Discharged from the Admiralty. The Resolute's spare powder was sold off as salvage.", "Licenciado del Almirantazgo. La pólvora sobrante de la Resoluta se vendió como chatarra.")),
  goal("talk", ("Find out who bought the Resolute's salvage powder: ask the shipwright at {p1}.", "Averigua quién compró la pólvora de la Resoluta: pregunta en el astillero de {p1}."), npc="shipwright", port="{p1}", building="shipyard"),
  say("shipwright", ("Six casks off the Resolute? I bought them for blasting stumps and never used a pinch. Look at it, it cakes like wet sand. Every lid has the same mark burned in: a hammer over a wave.",
                     "¿Seis barriles de la Resoluta? Los compré para volar tocones y no gasté ni una pizca. Mírela, se apelmaza como arena mojada. Todas las tapas llevan la misma marca a fuego: un martillo sobre una ola."),
      ("That's the Ironreef mill mark.", "Es la marca del molino de Arrecife de Hierro.")),
  get("caked_powder"),
  goal("networth", ("Get your trade on its feet: reach a net worth of 6,000.", "Pon en marcha tu negocio: alcanza un patrimonio de 6.000."), amount=6000)]),
 chapter("widow", ("The Widow's Due", "Lo que se le debe a la viuda"), 0, {"p2": "other,new,has:market"}, [
  say("governor", ("One more thing, Wren. Abel Strand's widow keeps a chandlery in {p2}. The Admiralty paid her a month's wages and called it settled. I thought you should know.",
                   "Una cosa más, Wren. La viuda de Abel Strand tiene una cordelería en {p2}. El Almirantazgo le pagó un mes de sueldo y lo dio por zanjado. Pensé que debía saberlo."),
      ("Abel was my second. I'll see her.", "Abel era mi segundo. Iré a verla.")),
  goal("deliver", ("Bring 20 Salt Fish to Nan Strand's chandlery in {p2}. Her shelves are empty.", "Lleva 20 de Pescado salado a la cordelería de Nan Strand en {p2}. Tiene las estanterías vacías."), good="fish", amount=20, port="{p2}"),
  take("fish", 20),
  say("nan", ("You've a nerve, Tobias Wren. Every quay in the Reach says you killed my Abel. ... Fish. You brought fish. Sit down before I change my mind.",
              "Tienes valor, Tobias Wren. Todos los muelles del Estrecho dicen que mataste a mi Abel. ... Pescado. Has traído pescado. Siéntate antes de que cambie de idea."),
      ("Abel said nothing to you about the powder?", "¿Abel no te dijo nada de la pólvora?")),
  say("nan", ("He said it smelled of vinegar, the week before they sailed. He said he'd told the gunner. That's you. Did you listen?",
              "Dijo que olía a vinagre, la semana antes de zarpar. Dijo que se lo había contado al artillero. Ese eres tú. ¿Le escuchaste?"),
      ("I listened. Nobody above me did.", "Le escuché. Nadie por encima de mí lo hizo.")),
  unlock("spice")]),
 chapter("shipmates", ("Old Shipmates", "Viejos compañeros"), 1, {"p3": "other,new,has:tavern"}, [
  say("nan", ("Kip Wade, the Resolute's powder boy, came out of it with burns on both arms. He drinks in {p3} now. He was in the magazine when the casks came aboard.",
              "Kip Wade, el mozo de pólvora de la Resoluta, salió de aquello con quemaduras en los dos brazos. Ahora bebe en {p3}. Estaba en el pañol cuando subieron los barriles."),
      ("Then he saw who brought them.", "Entonces vio quién los trajo.")),
  goal("talk", ("Find Kip Wade at the tavern in {p3}.", "Busca a Kip Wade en la taberna de {p3}."), npc="kip", port="{p3}", building="tavern"),
  say("kip", ("Mister Wren! They said you'd be hanged. I saw the casks come down, sir. An officer signed for them at the hatch. Gloves, good coat, never looked at us. I didn't see his face, I'm sorry.",
              "¡Señor Wren! Decían que lo ahorcarían. Vi bajar los barriles, señor. Un oficial los firmó en la escotilla. Guantes, buena casaca, no nos miró. No le vi la cara, lo siento."),
      ("Gloves and a good coat narrows it down. Thank you, Kip.", "Guantes y buena casaca ya reduce la lista. Gracias, Kip.")),
  goal("combat", ("Someone told the raiders you're asking questions. Win a fight against them.", "Alguien ha avisado a los corsarios de que andas preguntando. Gana un combate contra ellos."), wins=1)]),
 chapter("hammer_wave", ("The Hammer and the Wave", "El martillo y la ola"), 1, {}, [
  goal("talk", ("Ask at the Ironreef mill office, by the market, who sold that powder to the Admiralty.", "Pregunta en la oficina del molino de Arrecife de Hierro, junto al mercado, quién vendió esa pólvora al Almirantazgo."), npc="quill", port="ironreef", building="market"),
  say("quill", ("You're the gunner from the Resolute. I write up every cask that leaves this yard. Six of yours came back spoiled in March, and somebody signed them out again in April.",
                "Usted es el artillero de la Resoluta. Yo apunto cada barril que sale de este patio. Seis de los suyos volvieron estropeados en marzo, y alguien firmó su salida otra vez en abril."),
      ("Who signed?", "¿Quién firmó?"), QUILL),
  say("quill", ("I can't hand you Governor Thorne's ledger. I can copy one page by candlelight, if the night watchman sleeps. He sleeps very well on cocoa. Thirty sacks of it.",
                "No puedo darle el libro del gobernador Thorne. Puedo copiarle una página a la luz de una vela, si el vigilante de noche duerme. Con cacao duerme de maravilla. Treinta sacos."),
      ("Thirty sacks. Done.", "Treinta sacos. Hecho."), QUILL),
  goal("deliver", ("Bring 30 Cocoa Beans to Ironreef for the night watchman.", "Lleva 30 de Granos de cacao a Arrecife de Hierro para el vigilante de noche."), good="cocoa", amount=30, port="ironreef"),
  take("cocoa", 30)]),
 chapter("the_copy", ("The Copy", "La copia"), 2, {}, [
  say("quill", ("Here. Six casks returned spoiled, signed out to the Resolute's magazine on the ninth of April. Signed by the officer who passed them: Captain S. Grimmer.",
                "Aquí está. Seis barriles devueltos por estropeados, enviados al pañol de la Resoluta el nueve de abril. Firmados por el oficial que los aprobó: capitán S. Grimmer."),
      ("Grimmer. He stood on the quarterdeck while my gunners died.", "Grimmer. Estaba en el alcázar mientras mis artilleros morían."), QUILL),
  say("quill", ("One more thing, and then I never met you. The mill belongs to Governor Thorne. If this page turns up in a courtroom with my hand on it, I lose my place. Keep it somewhere safe.",
                "Una cosa más, y luego nunca le he visto. El molino es del gobernador Thorne. Si esta página aparece en un tribunal con mi letra, pierdo mi puesto. Guárdela en lugar seguro."),
      ("It goes in a bank vault tonight.", "Esta noche va a la cámara de un banco.")),
  get("copied_page"),
  goal("deposit", ("Rent a strongbox for the page: keep 8,000 in a bank.", "Alquila una caja fuerte para la página: ten 8.000 en un banco."), amount=8000),
  unlock("arms")]),
 chapter("warning", ("A Friendly Warning", "Un aviso amistoso"), 2, {}, [
  say("grimmer", ("Mister Wren. I'm told you've been reading other people's ledgers. The board has closed your case, and I'd hate to see it opened by a man who can't prove a thing. Leave it closed and I'll find you a licence to sell to the Admiralty yards.",
                  "Señor Wren. Me cuentan que anda leyendo los libros de otros. El tribunal ha cerrado su caso, y me disgustaría verlo reabierto por un hombre que no puede probar nada. Déjelo cerrado y le conseguiré una licencia para venderle a los astilleros del Almirantazgo."),
      ("I'll keep my own licence, Captain.", "Me quedo con mi propia licencia, capitán."), GRIMMER),
  say("grimmer", ("Pity. The Reach is a big sea, Mister Wren, and it has a great many rocks in it. Good day.",
                  "Lástima. El Estrecho es un mar muy grande, señor Wren, y tiene muchísimas rocas. Buenos días."),
      ("Good day, Captain.", "Buenos días, capitán."), GRIMMER),
  log(("Captain Grimmer offered you a licence to drop the matter. You refused.", "El capitán Grimmer te ofreció una licencia a cambio de olvidar el asunto. La rechazaste.")),
  goal("combat", ("Raiders have started following your sloop. Win 2 fights against them.", "Unos corsarios han empezado a seguir tu balandra. Gana 2 combates contra ellos."), wins=2)]),
 chapter("board_answer", ("The Board's Answer", "La respuesta del tribunal"), 2, {"p4": "other,new,has:governor"}, [
  goal("talk", ("Take the copied page to the governor of {p4}, who sat on the Resolute's board.", "Lleva la página copiada a la gobernación de {p4}, que formó parte del tribunal de la Resoluta."), npc="governor", port="{p4}"),
  say("governor", ("This proves the casks were spoiled when they went aboard. It doesn't prove who carried them. A captain's word against a discharged gunner's is no contest, Wren. Bring me the ship that moved the powder.",
                   "Esto prueba que los barriles ya estaban estropeados al embarcarlos. No prueba quién los llevó. La palabra de un capitán contra la de un artillero licenciado no tiene color, Wren. Tráigame el barco que movió la pólvora."),
      ("Then I'll find the ship.", "Entonces encontraré el barco.")),
  goal("networth", ("A ship hunt costs money. Build a net worth of 25,000.", "Buscar un barco cuesta dinero. Alcanza un patrimonio de 25.000."), amount=25000)]),
 # ---------------- Act II: The Carrier
 chapter("following", ("Following the Powder", "Siguiendo la pólvora"), 3, {"p5": "other,new,has:market"}, [
  say("merchant", ("Powder? It leaves Ironreef every month on brigs with no name painted on the stern. The harbour books in {p5} list every ship that clears. They only open them for captains the governors trust.",
                   "¿Pólvora? Sale de Arrecife de Hierro cada mes en bergantines sin nombre pintado en la popa. Los libros del puerto de {p5} apuntan cada barco que despacha. Solo los abren a capitanes de confianza de los gobernadores."),
      ("Then I'll earn some trust.", "Entonces me ganaré esa confianza.")),
  goal("contracts", ("Earn the governors' trust: complete 2 governor contracts.", "Gánate la confianza de los gobernadores: cumple 2 contratos de gobernador."), n=2),
  goal("talk", ("Ask to read the harbour books at the market in {p5}.", "Pide leer los libros del puerto en el mercado de {p5}."), npc="merchant", port="{p5}", building="market"),
  say("merchant", ("Here, captain. Every month, the same brig, the Hammerhead, Ironreef to nowhere in particular. Nobody asks where nowhere is.",
                   "Aquí tiene, capitán. Todos los meses el mismo bergantín, el Martillo, de Arrecife de Hierro a ninguna parte en concreto. Nadie pregunta dónde queda ninguna parte."),
      ("The Hammerhead. Now I have a name.", "El Martillo. Ya tengo un nombre.")),
  unlock("textiles")]),
 chapter("two_harbours", ("Two Harbours", "Dos puertos"), 3, {}, [
  say("kip", ("I'm done drinking, Mister Wren. Let me sail with you. I can't hold a rammer with these arms, but I can count casks and I know that brig's lines.",
              "Se acabó la bebida, señor Wren. Déjeme navegar con usted. Con estos brazos no puedo sostener un atacador, pero sé contar barriles y conozco las líneas de ese bergantín."),
      ("Welcome aboard, Kip.", "Bienvenido a bordo, Kip.")),
  goal("fleet", ("The Hammerhead uses two harbours. Buy a second ship so you can watch both.", "El Martillo usa dos puertos. Compra un segundo barco para vigilar los dos."), n=2),
  log(("Kip Wade signs on. Your second ship watches the other harbour.", "Kip Wade se enrola. Tu segundo barco vigila el otro puerto.")),
  goal("networth", ("Keep both ships paid: reach a net worth of 45,000.", "Mantén a los dos barcos pagados: alcanza un patrimonio de 45.000."), amount=45000)]),
 chapter("raider_powder", ("The Raiders' Powder", "La pólvora de los corsarios"), 4, {}, [
  say("kip", ("Raiders' guns don't misfire, sir. Not one. Ours did. If their powder's the good stuff, it came from somewhere good.",
              "Los cañones de los corsarios no fallan, señor. Ni uno. Los nuestros sí. Si su pólvora es de la buena, salió de algún sitio bueno."),
      ("Then we'll take a sample out of their magazines.", "Entonces sacaremos una muestra de sus pañoles.")),
  goal("sink", ("Sink 2 raiders and scrape a sample out of their powder rooms.", "Hunde 2 corsarios y rasca una muestra de sus pañoles de pólvora."), n=2),
  get("raider_powder"),
  say("kip", ("Admiralty grade, sir. Fine as flour, dry as a sermon. That's the powder that should have been in our magazine.",
              "Calidad del Almirantazgo, señor. Fina como harina, seca como un sermón. Esa es la pólvora que debería haber estado en nuestro pañol."),
      ("Somebody swapped it and sold ours to the men who fired on us.", "Alguien la cambió y vendió la nuestra a los que nos dispararon."))]),
 chapter("decoy", ("The Decoy", "El señuelo"), 4, {"p6": "other,new"}, [
  say("merchant", ("Your Hammerhead was seen loading off {p6} last night. Low in the water. Go now and you'll catch her at anchor.",
                   "Anoche vieron a su Martillo cargando frente a {p6}. Muy hundido. Si va ahora, la pillará fondeada."),
      ("Kip, make sail.", "Kip, larga velas.")),
  goal("npccombat", ("Catch the brig loading off {p6}.", "Atrapa al bergantín que carga frente a {p6}."), enemy="powder_tender", port="{p6}"),
  say("kip", ("That's not her, sir! It's a sloop called the Tallow, painted up to look like her. Empty hold, and a crew that knew we were coming.",
              "¡No es él, señor! Es una balandra llamada el Sebo, pintada para parecerse. Bodega vacía, y una tripulación que sabía que veníamos."),
      ("Someone told them. Someone who reads my letters.", "Alguien les avisó. Alguien que lee mis cartas.")),
  log(("The Hammerhead was a decoy. Someone knew you were coming.", "El Martillo era un señuelo. Alguien sabía que ibas.")),
  unlock("tobacco")]),
 chapter("leak", ("The Leak", "La filtración"), 5, {}, [
  goal("talk", ("Only the board knew your plans. Go back to the governor of {p4}.", "Solo el tribunal conocía tus planes. Vuelve a la gobernación de {p4}."), npc="governor", port="{p4}"),
  say("governor", ("My secretary, Felix Dorn, copied every letter you sent me. He left two days ago without his wages. I should have seen it. He drinks, he gambles, and lately he's paid his debts.",
                   "Mi secretario, Felix Dorn, copiaba todas las cartas que usted me mandaba. Se fue hace dos días sin cobrar. Debí verlo venir. Bebe, juega, y últimamente paga sus deudas."),
      ("Where does a man like that hide?", "¿Dónde se esconde un hombre así?")),
  say("governor", ("Somewhere with a curio dealer who buys stolen letters, I'd guess. And Wren, if you find him, I want him alive.",
                   "En algún sitio con un anticuario que compre cartas robadas, diría yo. Y Wren, si lo encuentra, lo quiero vivo."),
      ("Alive. Understood.", "Vivo. Entendido.")),
  goal("networth", ("Pay informers along the coast: build a net worth of 70,000.", "Paga a informantes por la costa: alcanza un patrimonio de 70.000."), amount=70000)]),
 chapter("dorn", ("Dorn", "Dorn"), 5, {"p7": "other,new,has:curio"}, [
  goal("talk", ("Your informers point to the curio dealer at {p7}. Find Felix Dorn there.", "Tus informantes señalan al anticuario de {p7}. Busca allí a Felix Dorn."), npc="dorn", port="{p7}", building="curio"),
  say("dorn", ("Don't. Please. Captain Grimmer pays me to read the board's letters, that's all. If he knows I talked to you he'll put me over the side himself.",
               "No. Por favor. El capitán Grimmer me paga por leer las cartas del tribunal, nada más. Si se entera de que he hablado con usted, me tirará por la borda él mismo."),
      ("Then tell me where the Hammerhead anchors, and I'll get you out of the Reach.", "Entonces dime dónde fondea el Martillo y te sacaré del Estrecho.")),
  say("dorn", ("Every month, the same three coves. I wrote them down. Passage money first. Forty casks of sugar will buy me a berth to the mainland.",
               "Cada mes, las mismas tres calas. Las tengo apuntadas. Primero, el pasaje. Cuarenta de azúcar me compran una litera hasta el continente."),
      ("Forty sugar. You'll have them.", "Cuarenta de azúcar. Los tendrás.")),
  goal("have_good", ("Load 40 Cane Sugar for Dorn's passage.", "Carga 40 de Azúcar de caña para el pasaje de Dorn."), good="sugar", amount=40),
  take("sugar", 40),
  get("dorn_schedule")]),
 chapter("hammerhead", ("The Hammerhead", "El Martillo"), 6, {"p8": "other,new"}, [
  say("kip", ("Dorn's schedule says {p8} this month, sir. If he lied, he lied well.", "El calendario de Dorn dice {p8} este mes, señor. Si mintió, mintió bien."),
      ("Run out the guns, Kip.", "Saca los cañones, Kip.")),
  goal("npccombat", ("Catch the powder brig Hammerhead off {p8}.", "Atrapa al bergantín polvorero Martillo frente a {p8}."), enemy="hammerhead", port="{p8}"),
  say("pruett", ("All right, all right! Captain Grimmer gave us the spoiled casks to put in the Resolute's magazine, and we sold her good powder to the raiders off Isla Brasa. The same raiders she fought. It's all in the manifest.",
                 "¡Vale, vale! El capitán Grimmer nos dio los barriles estropeados para meterlos en el pañol de la Resoluta, y vendimos su pólvora buena a los corsarios de Isla Brasa. Los mismos corsarios contra los que luchó. Está todo en el manifiesto."),
      ("You'll say that to the board.", "Eso se lo dirás al tribunal.")),
  get("hammerhead_manifest"),
  log(("Captured Joss Pruett and the Hammerhead's manifest.", "Capturaste a Joss Pruett y el manifiesto del Martillo."))]),
 # ---------------- Act III: Coat or No Coat
 chapter("witnesses", ("Witnesses", "Testigos"), 6, {}, [
  say("governor", ("A brig master in irons will say anything to keep his neck. The board will want more voices, Wren. The men who were there, and the ones who lost them.",
                   "Un patrón de bergantín encadenado dirá lo que sea por salvar el cuello. El tribunal querrá más voces, Wren. Los hombres que estuvieron allí, y quienes los perdieron."),
      ("Kip saw the casks. Nan heard Abel.", "Kip vio los barriles. Nan oyó a Abel.")),
  goal("talk", ("Ask Nan Strand in {p2} to speak before the board.", "Pide a Nan Strand, en {p2}, que hable ante el tribunal."), npc="nan", port="{p2}", building="market"),
  say("nan", ("I'll say it to their faces. Abel told you, you told them, they didn't listen. I've waited three months to say it.",
              "Se lo diré a la cara. Abel te lo dijo, tú se lo dijiste a ellos y no escucharon. Llevo tres meses esperando para decirlo."),
      ("Thank you, Nan.", "Gracias, Nan.")),
  goal("contracts", ("Witnesses need safe passage and wages. Complete 2 more governor contracts to pay for them.", "Los testigos necesitan pasaje seguro y sueldo. Cumple 2 contratos de gobernador más para pagarlos."), n=2),
  unlock("wine")]),
 chapter("frame", ("Grimmer's Answer", "La respuesta de Grimmer"), 7, {}, [
  say("grimmer", ("Smuggled wine in a discharged gunner's hold, Mister Wren? The customs men are very interested. So are some friends of mine with guns. You should have taken the licence.",
                  "¿Vino de contrabando en la bodega de un artillero licenciado, señor Wren? A los aduaneros les interesa mucho. Y también a unos amigos míos con cañones. Debió aceptar la licencia."),
      ("There was never any wine in my hold.", "En mi bodega nunca ha habido vino."), GRIMMER),
  log(("Grimmer has put a smuggling charge on your name and sent raiders after your ships.", "Grimmer ha puesto un cargo de contrabando a tu nombre y ha mandado corsarios a por tus barcos.")),
  goal("sink", ("Grimmer's raiders are hunting your ships. Sink 3 of them.", "Los corsarios de Grimmer cazan tus barcos. Hunde 3."), n=3),
  goal("networth", ("Pay the lawyers fighting the smuggling charge: build a net worth of 120,000.", "Paga a los abogados que pelean el cargo de contrabando: alcanza un patrimonio de 120.000."), amount=120000)]),
 chapter("thorne", ("The Ironmaster", "El señor del hierro"), 7, {}, [
  goal("talk", ("Governor Thorne of Ironreef has asked to see you. Call at his house.", "El gobernador Thorne de Arrecife de Hierro ha pedido verte. Visita su casa."), npc="thorne", port="ironreef", building="governor"),
  say("thorne", ("Mister Wren. My mill made honest powder. What a captain does with it after is the Admiralty's business. Name Pruett, name Grimmer if you must, and leave Ironreef out of it. I'll pay each of the four families a pension from my own purse.",
                 "Señor Wren. Mi molino hizo pólvora honrada. Lo que un capitán haga con ella después es asunto del Almirantazgo. Nombre a Pruett, nombre a Grimmer si hace falta, y deje fuera a Arrecife de Hierro. Pagaré una pensión a cada una de las cuatro familias de mi propio bolsillo."),
      ("Your mill took spoiled casks back and sold them twice.", "Su molino recibió barriles estropeados y los vendió dos veces.")),
  say("thorne", ("Sold them once, Mister Wren, to the Admiralty, and the Admiralty sent them back to us. My clerk recorded it properly. Ask her. The pensions stand either way. Good day.",
                 "Los vendió una vez, señor Wren, al Almirantazgo, y el Almirantazgo nos los devolvió. Mi escribiente lo apuntó como es debido. Pregúntele a ella. Las pensiones siguen en pie de todos modos. Buenos días."),
      ("Good day, Governor.", "Buenos días, gobernador.")),
  log(("Thorne offered pensions to the four families if Ironreef is kept out of it.", "Thorne ofreció pensiones a las cuatro familias si Arrecife de Hierro queda fuera del asunto."))]),
 chapter("quill_choice", ("The Clerk's Choice", "La decisión de la escribiente"), 8, {}, [
  goal("talk", ("Thorne said to ask his clerk. Find Hester Quill at the Ironreef market.", "Thorne dijo que preguntaras a su escribiente. Busca a Hester Quill en el mercado de Arrecife de Hierro."), npc="quill", port="ironreef", building="market"),
  say("quill", ("He's right, as far as it goes. The mill wrote everything down. That's the trouble with writing everything down. If the board asks me, I'll swear to the page. I won't lie for Thorne and I won't lie for you.",
                "Tiene razón, hasta cierto punto. El molino lo apuntó todo. Ese es el problema de apuntarlo todo. Si el tribunal me pregunta, juraré sobre la página. No mentiré por Thorne y no mentiré por usted."),
      ("That's all I'm asking.", "Es todo lo que pido."), QUILL),
  get("quill_affidavit"),
  goal("fleet", ("Grimmer will try to stop you reaching Kestrel Bay. Sail with three ships.", "Grimmer intentará impedir que llegues a Bahía Cernícalo. Navega con tres barcos."), n=3)]),
 chapter("black_gull", ("The Black Gull", "La Gaviota Negra"), 9, {"p9": "other,new"}, [
  say("kip", ("Frigate on the horizon, sir, Admiralty lines and no Admiralty flag. She's waiting off {p9}, right across our course to the board.",
              "Fragata en el horizonte, señor, líneas del Almirantazgo y sin bandera del Almirantazgo. Espera frente a {p9}, justo en nuestro rumbo hacia el tribunal."),
      ("Grimmer's last argument. Clear for action.", "El último argumento de Grimmer. Zafarrancho de combate.")),
  goal("networth", ("Refit for a frigate fight: build a net worth of 180,000.", "Prepárate para luchar contra una fragata: alcanza un patrimonio de 180.000."), amount=180000),
  goal("npccombat", ("Break through the Black Gull off {p9}.", "Abre paso a través de la Gaviota Negra frente a {p9}."), enemy="black_gull", port="{p9}"),
  log(("The Black Gull struck her colours. Her captain would not say who sent him. He didn't need to.", "La Gaviota Negra arrió su bandera. Su capitán no quiso decir quién lo enviaba. No hacía falta."))]),
 chapter("board", ("Before the Board", "Ante el tribunal"), 9, {}, [
  goal("networth", ("The board meets at Kestrel Bay next season. Build a net worth of 240,000 so they take a merchant seriously.", "El tribunal se reúne en Bahía Cernícalo la próxima temporada. Alcanza un patrimonio de 240.000 para que se tomen en serio a un mercader."), amount=240000),
  goal("talk", ("Bring the manifest, the page, Quill's affidavit and your witnesses to the board at Kestrel Bay.", "Lleva el manifiesto, la página, la declaración de Quill y a tus testigos al tribunal de Bahía Cernícalo."), npc="governor", port="kestrel_bay"),
  say("governor", ("The board has read the manifest. Your discharge is struck out and your pension restored, Mister Wren. As for Captain Grimmer, he has friends who outrank everyone in this room. He is to be made commodore and posted to the outer Reach.",
                   "El tribunal ha leído el manifiesto. Su licenciamiento queda anulado y su pensión restituida, señor Wren. En cuanto al capitán Grimmer, tiene amigos por encima de todos los de esta sala. Será nombrado comodoro y destinado al Estrecho exterior."),
      ("You're promoting him.", "Lo están ascendiendo.")),
  say("governor", ("I'm moving him where he can't embarrass us. It's the most the Admiralty will do. I'm sorry.", "Lo mando donde no pueda avergonzarnos. Es lo más que hará el Almirantazgo. Lo siento."),
      ("Then I'll keep the manifest. Someone will want it one day.", "Entonces me quedo el manifiesto. Algún día alguien lo querrá."))]),
 chapter("coat", ("Coat or No Coat", "Con casaca o sin ella"), 10, {}, [
  say("governor", ("The board also offers you your old rank back, Master Gunner. The coat is on the table.", "El tribunal le ofrece además recuperar su antiguo grado, maestro artillero. La casaca está sobre la mesa."),
      ("Give the pension to the four families. I'll keep my sloop.", "Den la pensión a las cuatro familias. Yo me quedo mi balandra.")),
  goal("deposit", ("Thorne's pensions never came. Set up a fund for the four families: keep 60,000 in a bank.", "Las pensiones de Thorne nunca llegaron. Crea un fondo para las cuatro familias: ten 60.000 en un banco."), amount=60000),
  goal("talk", ("Tell Nan Strand in {p2}.", "Díselo a Nan Strand en {p2}."), npc="nan", port="{p2}", building="market"),
  say("nan", ("A fund. In Abel's name. ... You're a stubborn old fool, Tobias Wren. Come for supper on Sunday.",
              "Un fondo. A nombre de Abel. ... Eres un viejo testarudo, Tobias Wren. Ven a cenar el domingo."),
      ("I'll bring fish.", "Traeré pescado.")),
  reward(60000),
  log(("Your name is cleared. Grimmer is promoted to commodore. You keep the Hammerhead's manifest.", "Tu nombre queda limpio. Grimmer asciende a comodoro. Te quedas el manifiesto del Martillo.")),
  END]),
])
