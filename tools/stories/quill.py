"""The Compact - Hester Quill, 1705. Acts: A Clerk at Sea (1-7), Teeth (8-14), The Books Read Aloud (15-21)."""
from sk import *

npc("hurst", ("Wilma Hurst, mate of the Contract", "Wilma Hurst, segunda del Contrato"), "crew", True, 1705, "portrait_smuggler")
npc("vann", ("Governor Liesl Vann", "Gobernadora Liesl Vann"), "governor", True, 17051, "portrait_governor")
npc("thorne", ("Governor Magnus Thorne", "Gobernador Magnus Thorne"), "governor", False, 16944, "portrait_governor")

enemy("the_contract", ("The Contract", "El Contrato"), 170, 13, 0.85, 70, 25000, "ship_barque_pirate", 8)
enemy("the_anvil", ("The Anvil", "El Yunque"), 310, 22, 0.8, 74, 60000, "ship_frigate_navy", 12)

item("compact_ledgers", ("The Compact Ledgers", "Los libros del Pacto"),
     ("Eleven years of copies in your own hand: water sold at three prices, cannon sold twice.", "Once años de copias de tu puño y letra: agua vendida a tres precios, cañones vendidos dos veces."))
item("spring_rights", ("Spring Rights", "Derechos del manantial"),
     ("Fresh water outside the Compact. Ships pay you a little extra for a full cask.", "Agua dulce fuera del Pacto. Los barcos te pagan algo más por una barrica llena."), "trade_sell_mult(+2%)")
item("contract_orders", ("Thorne's Orders", "Las órdenes de Thorne"),
     ("A letter of marque against free traders, under Governor Thorne's seal. Privateers who read it lose their nerve.", "Una patente de corso contra los comerciantes libres, con el sello del gobernador Thorne. Los corsarios que la leen pierden el temple."), "combat_enemy_accuracy(-6)")
item("salary_list", ("The Salary List", "La lista de sueldos"),
     ("Which governors the Compact paid, how much, and on which day of the month.", "A qué gobernadores pagaba el Pacto, cuánto y qué día del mes."))

WREN = ("Tobias Wren", "Tobias Wren")

STORY = campaign("compact", ("The Compact", "El Pacto"), 1705,
 ("1705. Three years after Grimmer's flagship went down, the Reach is free to trade, as long as it buys its cannon from Ironreef and its water from Tidewell. Governor Magnus Thorne and Governor Liesl Vann call their arrangement the Compact. Hester Quill kept both their ledgers for eleven years. She left with copies, and now neither port will let her ashore.",
  "1705. Tres años después del hundimiento de la nave de Grimmer, el Estrecho comercia en libertad, siempre que compre sus cañones en Arrecife de Hierro y su agua en Pozoclaro. El gobernador Magnus Thorne y la gobernadora Liesl Vann llaman a su acuerdo el Pacto. Hester Quill llevó los libros de ambos durante once años. Se marchó con copias, y ahora ninguno de los dos puertos la deja desembarcar."),
 ("The Books Are Open", "Los libros, abiertos"),
 ("Thorne lost his seat and Vann kept hers, at fair prices. Water from your spring sold by the cask, Tobias Wren's powder filled holds from Saltmere to Puerto Ambar, and harbour clerks across the Reach started keeping second copies. You still can't go back to Ironreef. You don't miss the view.",
  "Thorne perdió su cargo y Vann conservó el suyo, a precios justos. El agua de tu manantial se vendió por barricas, la pólvora de Tobias Wren llenó bodegas de Salmar a Puerto Ambar, y los escribientes de los puertos de todo el Estrecho empezaron a guardar segundas copias. Sigues sin poder volver a Arrecife de Hierro. No echas de menos las vistas."),
[
 # ---------------- Act I: A Clerk at Sea
 chapter("clerk", ("A Clerk at Sea", "Una escribiente en el mar"), 0, {}, [
  say("governor", ("Miss Quill. Ironreef and Tidewell have written to every governor in the Reach. You stole private papers, they say. I don't care what you took, but I can't be seen helping you.",
                   "Señorita Quill. Arrecife de Hierro y Pozoclaro han escrito a todos los gobernadores del Estrecho. Dicen que robó papeles privados. No me importa lo que se llevara, pero no pueden verme ayudándola."),
      ("Then don't be seen.", "Entonces que no lo vean.")),
  get("compact_ledgers"),
  goal("networth", ("Build a trade of your own before you take on the Compact: reach a net worth of 8,000.", "Levanta tu propio negocio antes de enfrentarte al Pacto: alcanza un patrimonio de 8.000."), amount=8000)]),
 chapter("stranded", ("Stranded Cargo", "Carga varada"), 0, {"p1": "other,new,has:market"}, [
  say("merchant", ("Ships are leaving the Reach, miss. No cannon without the Compact's stamp, no water without the Compact's price. A captain in {p1} is stuck with a hold of cocoa he can't afford to sail home.",
                   "Los barcos se marchan del Estrecho, señorita. No hay cañones sin el sello del Pacto, ni agua sin el precio del Pacto. Un capitán en {p1} se ha quedado con una bodega de cacao que no puede permitirse llevar a casa."),
      ("Then I'll buy his cocoa and he can sail light.", "Entonces le compro el cacao y que navegue ligero.")),
  goal("have_good", ("Buy 20 Cocoa Beans off the stranded captain's hands.", "Compra 20 de Granos de cacao al capitán varado."), good="cocoa", amount=20),
  log(("The stranded captain sailed home light. He promised to tell his friends about you.", "El capitán varado volvió a casa ligero. Prometió hablar de ti a sus amigos.")),
  unlock("spice")]),
 chapter("spring", ("The Fenced Spring", "El manantial vallado"), 1, {"p2": "other,new,has:tavern"}, [
  goal("talk", ("Ask the barkeep in {p2} about water that doesn't come from Tidewell.", "Pregunta al tabernero de {p2} por agua que no venga de Pozoclaro."), npc="barkeep", port="{p2}", building="tavern"),
  say("barkeep", ("There's a spring above the town, sweet as anything. The Compact paid the old governor to fence it off. Fences rot, love, and the land is for sale.",
                  "Hay un manantial encima del pueblo, de agua dulcísima. El Pacto pagó al viejo gobernador para que lo vallara. Las vallas se pudren, cariño, y el terreno está en venta."),
      ("How much?", "¿Cuánto?")),
  goal("deposit", ("Put 12,000 in a bank to buy the spring rights above {p2}.", "Deposita 12.000 en un banco para comprar los derechos del manantial de {p2}."), amount=12000),
  get("spring_rights"),
  log(("Bought the fenced spring above {p2}.", "Compraste el manantial vallado de {p2}."))]),
 chapter("casks", ("Casks", "Barricas"), 1, {"p3": "other,new,has:shipyard"}, [
  say("barkeep", ("Water's no good without casks, love. Every cooper in the Reach buys his staves from Ironreef. Except the shipwright in {p3}, who's too stubborn to buy anything.",
                  "El agua no sirve de nada sin barricas, cariño. Todos los toneleros del Estrecho compran las duelas en Arrecife de Hierro. Menos la carpintería de ribera de {p3}, que es demasiado terca para comprar nada."),
      ("Stubborn is good.", "Terca está bien.")),
  goal("deliver", ("Bring 20 Hardwood to the shipwright at {p3} for staves.", "Lleva 20 de Madera dura a la carpintería de ribera de {p3} para duelas."), good="timber", amount=20, port="{p3}"),
  take("timber", 20),
  say("shipwright", ("Hardwood. Real hardwood, not Ironreef's pine painted brown. You'll have your casks in a fortnight, and I'll take payment in water.",
                     "Madera dura. Madera dura de verdad, no el pino de Arrecife de Hierro pintado de marrón. Tendrás tus barricas en quince días, y cobraré en agua."),
      ("A fair price.", "Un precio justo.")),
  reward(8000)]),
 chapter("first_sale", ("First Water", "La primera agua"), 2, {}, [
  log(("Your first casks are full. Captains are lining up on the quay at {p2}.", "Tus primeras barricas están llenas. Los capitanes hacen cola en el muelle de {p2}.")),
  goal("contracts", ("Selling water needs a harbour licence. Earn one by completing a governor contract.", "Vender agua exige una licencia portuaria. Gánatela cumpliendo un contrato de gobernador."), n=1),
  goal("networth", ("Grow the water trade: reach a net worth of 22,000.", "Haz crecer el negocio del agua: alcanza un patrimonio de 22.000."), amount=22000)]),
 chapter("gunner", ("The Gunner", "El artillero"), 2, {"p4": "other,new,has:tavern"}, [
  goal("talk", ("Someone is selling powder outside the Compact in {p4}. Find the seller at the tavern.", "Alguien vende pólvora fuera del Pacto en {p4}. Busca al vendedor en la taberna."), npc="wren", port="{p4}", building="tavern"),
  say("wren", ("Ink on your cuffs. You were the girl in the Ironreef mill office, back in ninety-four. You copied a page for me once.", "Tinta en los puños. Tú eras la chica de la oficina del molino de Arrecife de Hierro, allá por el noventa y cuatro. Una vez me copiaste una página."),
      ("And you never paid me.", "Y nunca me la pagaste."), WREN),
  say("wren", ("Then I'll pay now. I cast my own powder these days, outside the Compact. Bring me 30 hardwood for charcoal and I'll fill any hold that asks.",
               "Pues te la pago ahora. Hoy en día hago mi propia pólvora, fuera del Pacto. Tráeme 30 de madera dura para carbón y llenaré cualquier bodega que lo pida."),
      ("Thirty hardwood. I'll bring an invoice.", "Treinta de madera dura. Traeré factura."), WREN),
  goal("have_good", ("Bring 30 Hardwood to Tobias Wren for charcoal.", "Lleva 30 de Madera dura a Tobias Wren para hacer carbón."), good="timber", amount=30),
  take("timber", 30),
  reward(12000),
  log(("Tobias Wren sells powder outside the Compact. The Reach has a second source.", "Tobias Wren vende pólvora fuera del Pacto. El Estrecho tiene un segundo proveedor."))]),
 chapter("powder_run", ("The Powder Run", "El reparto de pólvora"), 3, {}, [
  say("wren", ("First batch is dry. The Compact's thugs know it, too. They'll be waiting on the routes.", "La primera tanda está seca. Los matones del Pacto también lo saben. Estarán esperando en las rutas."),
      ("Let them wait.", "Que esperen."), WREN),
  goal("combat", ("Get Wren's powder through: win 2 fights against the Compact's hired raiders.", "Haz pasar la pólvora de Wren: gana 2 combates contra los corsarios a sueldo del Pacto."), wins=2),
  goal("networth", ("Reach a net worth of 35,000.", "Alcanza un patrimonio de 35.000."), amount=35000),
  unlock("arms")]),
 # ---------------- Act II: Teeth
 chapter("thorne_letter", ("A Letter from Ironreef", "Una carta de Arrecife de Hierro"), 3, {}, [
  say("thorne", ("Miss Quill. You kept my books for eleven years, and you kept them well, which is why I know you understand arithmetic. A spring and a gunner are small numbers. The Compact is a large one. Come home. Your desk is waiting.",
                 "Señorita Quill. Llevó mis libros once años, y los llevó bien, por eso sé que entiende de aritmética. Un manantial y un artillero son números pequeños. El Pacto es un número grande. Vuelva a casa. Su escritorio la espera."),
      ("Small numbers add up, Governor.", "Los números pequeños se suman, gobernador.")),
  log(("Thorne wrote, asking you back. You wrote a total at the bottom of his letter and sent it back.", "Thorne te escribió pidiéndote que volvieras. Escribiste un total al pie de su carta y se la devolviste.")),
  goal("networth", ("Reach a net worth of 50,000.", "Alcanza un patrimonio de 50.000."), amount=50000)]),
 chapter("vann_price", ("Vann's Price", "El precio de Vann"), 4, {"p5": "other,new,has:market"}, [
  goal("talk", ("Governor Vann has come to {p5} to meet you on neutral ground. Find her at the market.", "La gobernadora Vann ha venido a {p5} para verte en terreno neutral. Búscala en el mercado."), npc="vann", port="{p5}", building="market"),
  say("vann", ("Thorne writes letters. I prefer to buy things. Thirty-six thousand for your spring, Hester. Three times what you paid. You'll be rich and nobody will chase you.",
               "Thorne escribe cartas. Yo prefiero comprar cosas. Treinta y seis mil por tu manantial, Hester. El triple de lo que pagaste. Serás rica y nadie te perseguirá."),
      ("The spring isn't for sale.", "El manantial no está en venta.")),
  say("vann", ("Everything is for sale. You taught me that, in my own ledgers. Think about it.", "Todo está en venta. Me lo enseñaste tú, en mis propios libros. Piénsalo."),
      ("I've thought.", "Ya lo he pensado.")),
  unlock("textiles")]),
 chapter("rumours", ("Teeth", "Dientes"), 4, {"p6": "other,new,has:governor"}, [
  goal("talk", ("The governor of {p6} has sent for you.", "La gobernación de {p6} te ha mandado llamar."), npc="governor", port="{p6}"),
  say("governor", ("The Compact has hired a privateer, Miss Quill. A barque called the Contract, with a letter of marque signed by Thorne himself. She's sinking anyone who buys your water or Wren's powder.",
                   "El Pacto ha contratado a un corsario, señorita Quill. Una bricbarca llamada el Contrato, con patente de corso firmada por el propio Thorne. Hunde a cualquiera que compre su agua o la pólvora de Wren."),
      ("Then she sinks me first, or I sink her.", "Entonces que me hunda a mí primero, o la hundo yo.")),
  goal("sink", ("The Contract's escorts are on the routes. Sink 2 raiders.", "Los escoltas del Contrato vigilan las rutas. Hunde 2 corsarios."), n=2)]),
 chapter("contract", ("The Contract", "El Contrato"), 5, {"p7": "other,new"}, [
  goal("npccombat", ("Sink the privateer Contract off {p7}.", "Hunde al corsario Contrato frente a {p7}."), enemy="the_contract", port="{p7}"),
  say("hurst", ("We sailed on orders under Thorne's seal. Here, take them. I'm not drowning for an ironmonger.", "Navegábamos con órdenes bajo el sello de Thorne. Tome, lléveselas. No pienso ahogarme por un ferretero."),
      ("I'll take the orders. Thank you.", "Me llevo las órdenes. Gracias.")),
  get("contract_orders"),
  log(("The Contract is sunk. Her mate gave you Thorne's orders.", "El Contrato está hundido. Su segunda te dio las órdenes de Thorne.")),
  unlock("tobacco")]),
 chapter("mate", ("The Mate's Story", "La historia de la segunda"), 5, {"p8": "other,new,has:bank"}, [
  say("hurst", ("You want to hurt the Compact? Don't chase Thorne. Chase his payroll. Three governors take a salary from the Ironreef mill, paid through the bank in {p8}.",
                "¿Quiere hacerle daño al Pacto? No persiga a Thorne. Persiga su nómina. Tres gobernadores cobran un sueldo del molino de Arrecife de Hierro, pagado a través del banco de {p8}."),
      ("A payroll. Now that's a ledger I'd like to read.", "Una nómina. Ese sí es un libro que me gustaría leer.")),
  goal("deposit", ("Bankers open their books for big depositors. Keep 40,000 in a bank.", "Los banqueros abren sus libros a los grandes depositantes. Ten 40.000 en un banco."), amount=40000),
  goal("talk", ("Ask the banker in {p8} about the Ironreef mill's payments.", "Pregunta al banquero de {p8} por los pagos del molino de Arrecife de Hierro."), npc="banker", port="{p8}", building="bank"),
  say("banker", ("Three governors, paid on the first of every month. I copied the list because nobody told me not to. You clerks are a dangerous breed.",
                 "Tres gobernadores, pagados el día uno de cada mes. Copié la lista porque nadie me dijo que no lo hiciera. Los escribientes sois una raza peligrosa."),
      ("We are.", "Lo somos.")),
  get("salary_list")]),
 chapter("water_fleet", ("The Water Fleet", "La flota del agua"), 6, {}, [
  say("wren", ("Your spring fills more casks than your sloop can carry, Quill. Get a second hull, and I'll paint 'Free Water' on her side myself.",
               "Tu manantial llena más barricas de las que tu balandra puede llevar, Quill. Consigue un segundo casco y yo mismo le pintaré 'Agua libre' en el costado."),
      ("Badly, I expect.", "Mal, supongo."), WREN),
  goal("fleet", ("Buy a second ship for the water trade.", "Compra un segundo barco para el negocio del agua."), n=2),
  goal("contracts", ("Supply governors with free water: complete 2 governor contracts.", "Abastece a los gobernadores con agua libre: cumple 2 contratos de gobernador."), n=2),
  goal("networth", ("Reach a net worth of 110,000.", "Alcanza un patrimonio de 110.000."), amount=110000)]),
 chapter("payroll", ("The Payroll", "La nómina"), 6, {}, [
  goal("talk", ("The governor of {p6} is on the salary list. Ask about it.", "La gobernación de {p6} está en la lista de sueldos. Pregunta por ello."), npc="governor", port="{p6}"),
  say("governor", ("You warned me about the Contract, and all the while I was on the same payroll as the man who hired her. I didn't think of it as a bribe, Miss Quill. I thought of it as a retainer.",
                   "Usted me avisó del Contrato, y mientras tanto yo cobraba de la misma nómina que el hombre que lo contrató. No lo veía como un soborno, señorita Quill. Lo veía como una iguala."),
      ("Ledgers don't know the difference.", "Los libros no distinguen la diferencia.")),
  say("governor", ("No. They don't. I'll stop taking it, and I'll say so when the books are read. Bring me a cargo of muskets for the harbour guard, so nobody says I sold my town's safety too.",
                   "No. No la distinguen. Dejaré de cobrarla, y lo diré cuando se lean los libros. Tráigame un cargamento de mosquetes para la guardia del puerto, para que nadie diga que también vendí la seguridad de mi pueblo."),
      ("Twelve muskets, then.", "Doce mosquetes, entonces.")),
  goal("deliver", ("Bring 12 Muskets to the governor of {p6}.", "Lleva 12 de Mosquetes a la gobernación de {p6}."), good="arms", amount=12, port="{p6}"),
  take("arms", 12)]),
 # ---------------- Act III: The Books Read Aloud
 chapter("anvil_warning", ("The Anvil", "El Yunque"), 6, {}, [
  say("wren", ("Thorne's bought a frigate. Navy lines, twenty-two guns, and he's named her the Anvil. He means it as a joke. It isn't a funny one.",
               "Thorne ha comprado una fragata. Líneas de la armada, veintidós cañones, y la ha llamado el Yunque. Lo dice como un chiste. No tiene gracia."),
      ("Then we'll need more than two hulls.", "Entonces necesitaremos más de dos cascos."), WREN),
  goal("fleet", ("Sail with three ships.", "Navega con tres barcos."), n=3),
  goal("sink", ("Clear the Compact's escorts from the routes: sink 3.", "Limpia las rutas de escoltas del Pacto: hunde 3."), n=3)]),
 chapter("clerks", ("Second Copies", "Segundas copias"), 7, {"p9": "other,new,has:market"}, [
  goal("talk", ("Harbour clerks keep every port's books. Meet the clerks at the market in {p9}.", "Los escribientes de puerto llevan los libros de cada puerto. Reúnete con ellos en el mercado de {p9}."), npc="merchant", port="{p9}", building="market"),
  say("merchant", ("Five of us came, miss, from five ports. We've all seen Compact money in our books. Nobody ever asked us about it. You're asking.",
                   "Hemos venido cinco, señorita, de cinco puertos. Todos hemos visto dinero del Pacto en nuestros libros. Nadie nos preguntó nunca. Usted sí."),
      ("Keep a second copy of everything. Bring it to me.", "Guardad una segunda copia de todo. Traédmela.")),
  log(("Clerks from five ports have started keeping second copies.", "Escribientes de cinco puertos han empezado a guardar segundas copias.")),
  goal("networth", ("Reach a net worth of 160,000.", "Alcanza un patrimonio de 160.000."), amount=160000),
  unlock("wine")]),
 chapter("vann_breaks", ("Vann Breaks", "Vann cede"), 8, {}, [
  goal("talk", ("Governor Vann has asked to meet again in {p5}.", "La gobernadora Vann ha pedido volver a verte en {p5}."), npc="vann", port="{p5}", building="market"),
  say("vann", ("Thorne bought a frigate without asking me. Thorne pays three governors I didn't know about. I can do arithmetic too, Hester. Leave my wells to me, at fair prices, and I'll say all of it before any governor you like.",
               "Thorne compró una fragata sin preguntarme. Thorne paga a tres gobernadores de los que yo no sabía nada. Yo también sé hacer cuentas, Hester. Déjame mis pozos, a precios justos, y lo diré todo ante el gobernador que quieras."),
      ("Fair prices. Written down.", "Precios justos. Por escrito.")),
  log(("Liesl Vann will testify against Thorne, if Tidewell keeps its wells at fair prices.", "Liesl Vann testificará contra Thorne si Pozoclaro conserva sus pozos a precios justos."))]),
 chapter("anvil", ("Hammer and Anvil", "Martillo y yunque"), 9, {"p10": "other,new"}, [
  goal("networth", ("Fit out for the Anvil: reach a net worth of 220,000.", "Equípate para el Yunque: alcanza un patrimonio de 220.000."), amount=220000),
  goal("npccombat", ("The Anvil is waiting off {p10}. Sink her.", "El Yunque espera frente a {p10}. Húndelo."), enemy="the_anvil", port="{p10}"),
  log(("The Anvil is on the bottom. Thorne has no more ships to buy.", "El Yunque está en el fondo. A Thorne no le quedan barcos que comprar."))]),
 chapter("books", ("The Books Read Aloud", "Los libros en voz alta"), 9, {"p11": "other,new,has:governor"}, [
  goal("networth", ("The governors will only hear a trader of standing. Build a net worth of 280,000.", "Los gobernadores solo escucharán a alguien de peso. Alcanza un patrimonio de 280.000."), amount=280000),
  goal("talk", ("Lay the ledgers, Thorne's orders and the salary list before the governor of {p11}.", "Presenta los libros, las órdenes de Thorne y la lista de sueldos ante la gobernación de {p11}."), npc="governor", port="{p11}"),
  say("governor", ("Water sold at three prices. A privateer paid out of a foundry's accounts. Three governors' salaries topped up by a mill. These will be read aloud in every harbour in the Reach, Miss Quill. The Compact is finished.",
                   "Agua vendida a tres precios. Un corsario pagado con las cuentas de una fundición. Los sueldos de tres gobernadores engordados por un molino. Esto se leerá en voz alta en cada puerto del Estrecho, señorita Quill. Se acabó el Pacto."),
      ("Read the totals slowly. People like totals.", "Lean los totales despacio. A la gente le gustan los totales.")),
  log(("The Compact's ledgers are read in every port.", "Los libros del Pacto se leen en todos los puertos."))]),
 chapter("invoice", ("The Invoice", "La factura"), 10, {}, [
  goal("talk", ("Bring Tobias Wren his share in {p4}.", "Lleva a Tobias Wren su parte a {p4}."), npc="wren", port="{p4}", building="tavern"),
  say("wren", ("Eleven years late, and you brought an invoice. 'One page, copied by candlelight, at risk of employment.' What's the total?",
               "Once años tarde, y traes factura. 'Una página, copiada a la luz de una vela, con riesgo del empleo.' ¿Cuál es el total?"),
      ("One drink. You're buying.", "Una copa. Invitas tú."), WREN),
  goal("contracts", ("Keep the free trade going: complete 2 more governor contracts.", "Mantén vivo el comercio libre: cumple 2 contratos de gobernador más."), n=2)]),
 chapter("guild", ("The Clerks' Guild", "El gremio de escribientes"), 10, {}, [
  say("merchant", ("The clerks want a guild, miss. A room, a strongbox, and someone who knows how to keep two copies of everything. They want you.",
                   "Los escribientes quieren un gremio, señorita. Una sala, una caja fuerte y alguien que sepa guardar dos copias de todo. La quieren a usted."),
      ("Then I'll need a very large strongbox.", "Entonces necesitaré una caja fuerte muy grande.")),
  goal("deposit", ("Found the Clerks' Guild: keep 100,000 in a bank.", "Funda el Gremio de Escribientes: ten 100.000 en un banco."), amount=100000),
  reward(80000),
  log(("The Clerks' Guild opens its doors, with two copies of everything.", "El Gremio de Escribientes abre sus puertas, con dos copias de todo.")),
  END]),
])
