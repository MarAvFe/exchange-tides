"""The Grimmer Debt - Marisol Vega, 1702. The original seven chapters (grimmer_original.json, unchanged) with new
ones woven between them. Acts: Letters of Credit (1-7), The Cartographer (8-14), The Undertow (15-21)."""
import json, os
from sk import *

ORIG = json.load(open(os.path.join(os.path.dirname(__file__), "grimmer_original.json"), encoding="utf-8"))

enemy("undertow_tender", ("The Provender", "El Avituallador"), 180, 12, 0.85, 70, 30000, "ship_brigantine_pirate", 9)
enemy("grimmer_flagship", ("The Undertow", "La Resaca"), 360, 26, 0.75, 76, 90000, "ship_frigate_navy", 14)

item("vega_deeds", ("House Vega Deeds", "Escrituras de la Casa Vega"),
     ("The deeds to your family's warehouse, bought back from the creditors.", "Las escrituras del almacén de tu familia, recompradas a los acreedores."), "trade_buy_mult(-2%)")
item("grimmer_offer", ("Grimmer's Letter", "La carta de Grimmer"),
     ("An offer to restore House Vega, in a fine hand, if you stop. You kept it as evidence.", "Una oferta para restaurar la Casa Vega, con letra elegante, si te detienes. La guardaste como prueba."))

HALE = ("Lieutenant Ada Hale", "Teniente Ada Hale")
MORENO = ("Rafe Moreno", "Rafe Moreno")

STORY = campaign("grimmer_debt", ("The Grimmer Debt", "La deuda de Grimmer"), 1702,
 ("The Reach is strangling. Commodore Silas Grimmer, once the Admiralty's finest, now sells safe passage to the highest bidder and sinks the rest. Honest trade is dying. You have a small ship, a smaller purse, and a reputation still to make.",
  "El Estrecho se asfixia. El comodoro Silas Grimmer, antaño lo mejor del Almirantazgo, vende ahora pasos seguros al mejor postor y hunde al resto. El comercio honrado agoniza. Tienes un barco pequeño, una bolsa aún más pequeña y una reputación por hacer."),
 ("The Reach is Free!", "¡El Estrecho es libre!"),
 ("Commodore Grimmer is beaten and the trade lanes are open again. Your name will be toasted in every tavern from Saltmere to Tidewell.",
  "El comodoro Grimmer ha caído y las rutas comerciales vuelven a estar abiertas. Brindarán por tu nombre en cada taberna, de Salmar a Pozoclaro."),
[
 # ---------------- Act I: Letters of Credit
 ORIG["letters"],
 chapter("mother_ledger", ("Mother's Ledger", "El libro de mi madre"), 0, {}, [
  goal("talk", ("The banker in Puerto Ambar has asked to see you about your family's accounts.", "El banquero de Puerto Ambar ha pedido verte por las cuentas de tu familia."), npc="banker", port="puerto_ambar", building="bank"),
  say("banker", ("Captain Vega. Your father's creditors have been patient for three years, and patience is expensive. The family warehouse goes to auction at the end of next year unless someone buys it back.",
                 "Capitana Vega. Los acreedores de su padre llevan tres años siendo pacientes, y la paciencia sale cara. El almacén de la familia sale a subasta a finales del año que viene si nadie lo recompra."),
      ("Then someone will.", "Entonces alguien lo hará.")),
  log(("House Vega's warehouse goes to auction unless you buy it back.", "El almacén de la Casa Vega saldrá a subasta si no lo recompras.")),
  goal("networth", ("Rebuild the family trade: reach a net worth of 12,000.", "Reconstruye el negocio familiar: alcanza un patrimonio de 12.000."), amount=12000)]),
 ORIG["ledger"],
 chapter("lost_ships", ("Three Lost Ships", "Tres barcos perdidos"), 1, {"p9": "other,new,has:market"}, [
  say("barkeep", ("Your family's ships? The Swallow, the Lantern and the Good Measure. Their crews' families live in {p9}. They say the raiders flew a black pennant with a white gull. Grimmer's colours.",
                  "¿Los barcos de su familia? La Golondrina, el Farol y la Buena Medida. Las familias de sus tripulaciones viven en {p9}. Dicen que los corsarios llevaban un gallardete negro con una gaviota blanca. Los colores de Grimmer."),
      ("Then I owe those families a visit.", "Entonces les debo una visita a esas familias.")),
  goal("deliver", ("Bring 30 Salt Fish to the crews' families in {p9}.", "Lleva 30 de Pescado salado a las familias de las tripulaciones en {p9}."), good="fish", amount=30, port="{p9}"),
  take("fish", 30),
  say("merchant", ("Fish from a Vega ship. My husband sailed on the Swallow. ... A deserter from Grimmer's deck came through last year asking about the Lark. Moreno, he called himself. He said the Admiralty has a lieutenant who listens.",
                   "Pescado de un barco Vega. Mi marido navegaba en la Golondrina. ... El año pasado pasó por aquí un desertor de la cubierta de Grimmer preguntando por la Alondra. Moreno, se llamaba. Dijo que el Almirantazgo tiene una teniente que escucha."),
      ("I know Moreno. He armed my ship.", "Conozco a Moreno. Él armó mi barco."))]),
 ORIG["crowe"],
 chapter("crowe_books", ("Crowe's Books", "Los libros de Crowe"), 2, {"p10": "other,new,has:bank"}, [
  say("barkeep", ("That ledger you took off the clerk. My cousin keeps books at the bank in {p10}. She'll read it for you, if you're the kind of customer banks like.",
                  "Ese libro que le quitó al escribiente. Mi prima lleva los libros en el banco de {p10}. Se lo leerá, si es usted de la clase de clientes que les gustan a los bancos."),
      ("I'm becoming that kind.", "Me estoy volviendo de esa clase.")),
  goal("deposit", ("Keep 25,000 in a bank so the bankers will read Crowe's ledger with you.", "Ten 25.000 en un banco para que los banqueros lean contigo el libro de Crowe."), amount=25000),
  goal("talk", ("Read Crowe's ledger with the banker in {p10}.", "Lee el libro de Crowe con el banquero de {p10}."), npc="banker", port="{p10}", building="bank"),
  say("banker", ("Payments from a commodore's agent every quarter. Payments out to raider captains. And insurance bought on every ship Crowe's rivals lost, from a house called Harrow & Sons. Someone always profits twice in these books.",
                 "Pagos del agente de un comodoro cada trimestre. Pagos a capitanes corsarios. Y seguros contratados sobre cada barco que perdieron los rivales de Crowe, con una casa llamada Harrow e Hijos. En estos libros siempre hay alguien que cobra dos veces."),
      ("Harrow & Sons. I'll remember the name.", "Harrow e Hijos. Recordaré el nombre.")),
  ]),
 chapter("moreno_tip", ("A Turncoat's Tip", "El soplo de un chaquetero"), 3, {"p11": "other,new,has:tavern"}, [
  goal("talk", ("Rafe Moreno has sent word he's in {p11}. Meet him at the tavern.", "Rafe Moreno ha mandado aviso de que está en {p11}. Reúnete con él en la taberna."), npc="moreno", port="{p11}", building="tavern"),
  say("moreno", ("Captain Vega. You found my muskets useful, I hear. Listen. Grimmer moves his anchorage every season, and only his chart-maker knows where. The chart-maker's sister builds boats. If she comes to you for help, help her.",
                 "Capitana Vega. Me dicen que mis mosquetes le fueron útiles. Escuche. Grimmer cambia de fondeadero cada temporada, y solo su cartógrafo sabe dónde. La hermana del cartógrafo construye barcos. Si acude a usted pidiendo ayuda, ayúdela."),
      ("I will.", "Lo haré."), MORENO),
  goal("networth", ("Prepare for whatever comes: reach a net worth of 60,000.", "Prepárate para lo que venga: alcanza un patrimonio de 60.000."), amount=60000)]),
 # ---------------- Act II: The Cartographer
 ORIG["cartographer"],
 chapter("brother", ("The Brother's Tale", "El relato del hermano"), 3, {}, [
  say("sailor", ("Grimmer kept me drawing for two years. Coves, reefs, depths. He anchors in a different cove every season, but he always comes back to Blackwater Cay to pay his crews. And he's built a fort at Mangrove Key to guard the lagoon.",
                 "Grimmer me tuvo dos años dibujando. Calas, arrecifes, profundidades. Fondea en una cala distinta cada temporada, pero siempre vuelve a Cayo Aguanegra a pagar a sus tripulaciones. Y ha levantado un fuerte en Cayo Manglar para guardar la laguna."),
      ("Then we'll start with the fort.", "Entonces empezaremos por el fuerte."), ("The Rescued Cartographer", "El cartógrafo rescatado")),
  goal("fleet", ("A fort won't fall to one sloop. Buy a second ship.", "Un fuerte no cae ante una sola balandra. Compra un segundo barco."), n=2),
  goal("networth", ("Arm your ships: reach a net worth of 85,000.", "Arma tus barcos: alcanza un patrimonio de 85.000."), amount=85000)]),
 chapter("warehouse", ("The Warehouse", "El almacén"), 4, {}, [
  say("banker", ("The auction is in the spring, Captain. The creditors will take a fair price before then, and not a coin less.",
                 "La subasta es en primavera, capitana. Los acreedores aceptarán un precio justo antes de esa fecha, y ni una moneda menos."),
      ("Name it.", "Diga la cifra.")),
  goal("deposit", ("Buy back House Vega's warehouse: keep 60,000 in a bank.", "Recompra el almacén de la Casa Vega: ten 60.000 en un banco."), amount=60000),
  get("vega_deeds"),
  log(("House Vega's warehouse is yours again.", "El almacén de la Casa Vega vuelve a ser tuyo."))]),
 ORIG["fort"],
 chapter("warrant_work", ("The Warrant", "La orden"), 5, {}, [
  say("hale", ("With that warrant, governors will give you Admiralty work. Take it. Grimmer will notice a merchant who has friends.",
               "Con esa orden, los gobernadores le darán trabajo del Almirantazgo. Acéptelo. Grimmer se fijará en una mercader que tiene amigos."),
      ("Good. Let him notice.", "Bien. Que se fije."), HALE),
  goal("contracts", ("Complete 3 governor contracts under the Admiralty warrant.", "Cumple 3 contratos de gobernador bajo la orden del Almirantazgo."), n=3),
  goal("networth", ("Reach a net worth of 120,000.", "Alcanza un patrimonio de 120.000."), amount=120000)]),
 ORIG["smoke"],
 chapter("grimmer_letter", ("A Letter from the Commodore", "Una carta del comodoro"), 6, {}, [
  say("grimmer", ("Captain Vega. Your father was a stubborn man and paid for it. I would hate to see the daughter pay twice. Stop now, and I'll see House Vega's ships sail unmolested for as long as I live.",
                  "Capitana Vega. Su padre era un hombre testarudo y lo pagó. Me disgustaría ver a la hija pagar dos veces. Deténgase ahora y me ocuparé de que los barcos de la Casa Vega naveguen sin que nadie los moleste mientras yo viva."),
      ("Then I'll make sure that isn't long.", "Entonces me aseguraré de que no sea mucho tiempo.")),
  get("grimmer_offer"),
  goal("sink", ("Grimmer has turned his wolves loose on House Vega. Sink 3 of them.", "Grimmer ha soltado a sus lobos contra la Casa Vega. Hunde 3."), n=3)]),
 # ---------------- Act III: The Undertow
 chapter("allies", ("Allies", "Aliados"), 6, {}, [
  goal("talk", ("Rafe Moreno is in {p11} with his schooner and twelve pardoned men.", "Rafe Moreno está en {p11} con su goleta y doce hombres indultados."), npc="moreno", port="{p11}", building="tavern"),
  say("moreno", ("Twelve men who owe Grimmer a ship and a burned crew. We'll sail in your line, Captain, if you'll have us.",
                 "Doce hombres a los que Grimmer les debe un barco y una tripulación quemada. Navegaremos en su línea, capitana, si nos acepta."),
      ("I'll have you.", "Os acepto."), MORENO),
  goal("fleet", ("Sail with three ships.", "Navega con tres barcos."), n=3)]),
 chapter("provender", ("The Provender", "El Avituallador"), 7, {"p12": "other,new"}, [
  say("varga", ("Grimmer's crews eat. A brig called the Provender brings their food and powder every month. She's off {p12} this week. No food, no fight.",
                "Las tripulaciones de Grimmer comen. Un bergantín llamado el Avituallador les lleva comida y pólvora cada mes. Esta semana está frente a {p12}. Sin comida, no hay pelea."),
      ("Then we'll take their dinner.", "Entonces les quitaremos la cena.")),
  goal("npccombat", ("Sink Grimmer's supply brig, the Provender, off {p12}.", "Hunde el bergantín de suministros de Grimmer, el Avituallador, frente a {p12}."), enemy="undertow_tender", port="{p12}"),
  log(("Grimmer's supplies are on the bottom. His crews will be hungry by the time you meet them.", "Los suministros de Grimmer están en el fondo. Sus tripulaciones tendrán hambre cuando os encontréis."))]),
 chapter("battery", ("The Shore Battery", "La batería de costa"), 7, {}, [
  say("varga", ("Blackwater has an old battery on the point that nobody's manned in years. Give my people muskets and we'll keep Grimmer's boats off the beach while you deal with his frigate.",
                "Aguanegra tiene una vieja batería en la punta que nadie ha guarnecido en años. Da mosquetes a mi gente y mantendremos los botes de Grimmer lejos de la playa mientras tú te encargas de su fragata."),
      ("How many muskets?", "¿Cuántos mosquetes?")),
  goal("deliver", ("Bring 15 Muskets to Varga's people at Blackwater Cay.", "Lleva 15 de Mosquetes a la gente de Varga en Cayo Aguanegra."), good="arms", amount=15, port="blackwater_cay"),
  take("arms", 15),
  goal("networth", ("Reach a net worth of 200,000.", "Alcanza un patrimonio de 200.000."), amount=200000)]),
 chapter("hale_fleet", ("Hale's Squadron", "La escuadra de Hale"), 8, {}, [
  goal("talk", ("Report your plan to Lieutenant Hale through the governor of {p7}.", "Informa de tu plan a la teniente Hale a través de la gobernación de {p7}."), npc="hale", port="{p7}", building="governor"),
  say("hale", ("Two Admiralty brigs will sail with you, unofficially. Officially, they're on a survey. If you lose, they were never there. If you win, the Admiralty planned it all along.",
               "Dos bergantines del Almirantazgo navegarán con usted, extraoficialmente. Oficialmente, están levantando cartas. Si pierde, nunca estuvieron allí. Si gana, el Almirantazgo lo planeó todo desde el principio."),
      ("That sounds like the Admiralty.", "Eso suena al Almirantazgo."), HALE),
  goal("contracts", ("Keep the governors on side: complete 2 more contracts.", "Mantén a los gobernadores de tu lado: cumple 2 contratos más."), n=2)]),
 chapter("undertow", ("The Undertow", "La Resaca"), 9, {}, [
  say("governor", ("Grimmer's frigate, the Undertow, carries fourteen guns and a crew of cutthroats. Gather a fortune for powder and repairs before you face him.",
                   "La fragata de Grimmer, la Resaca, monta catorce cañones y una tripulación de degolladores. Reúne una fortuna para pólvora y reparaciones antes de enfrentarte a él."),
      ("I'll be ready.", "Me prepararé.")),
  goal("networth", ("Build a net worth of 300,000.", "Alcanza un patrimonio de 300.000."), amount=300000),
  goal("npccombat", ("Defeat Commodore Grimmer at Blackwater Cay.", "Derrota al comodoro Grimmer en Cayo Aguanegra."), enemy="grimmer_flagship", port="blackwater_cay"),
  say("grimmer", ("You... a trader. Beaten by a ledger and a lucky broadside. The Reach will forget you, captain.",
                  "Tú... de mostrador a cubierta. Vencido por un libro de cuentas y una andanada con suerte... El Estrecho te olvidará."),
      ("The Reach will trade freely. That is enough.", "El Estrecho comerciará en libertad. Con eso basta.")),
  reward(100000),
  log(("Grimmer is defeated. The trade lanes are open.", "Grimmer ha sido derrotado. Las rutas comerciales están abiertas."))]),
 chapter("aftermath", ("The Day After", "El día después"), 9, {}, [
  goal("talk", ("Lieutenant Hale wants your account of the battle, at the governor's house in {p7}.", "La teniente Hale quiere tu relato de la batalla, en la casa de la gobernación de {p7}."), npc="hale", port="{p7}", building="governor"),
  say("hale", ("Grimmer will hang at Kestrel Bay. I'm told I'm to be promoted for a battle I didn't fight. I owe you a favour, Captain Vega. Call it in whenever you like.",
               "Grimmer será ahorcado en Bahía Cernícalo. Me dicen que me van a ascender por una batalla que no libré. Le debo un favor, capitana Vega. Cóbrelo cuando quiera."),
      ("I'll remember.", "Lo recordaré."), HALE),
  goal("sink", ("Grimmer's last captains won't surrender. Sink 3 of them.", "Los últimos capitanes de Grimmer no se rinden. Hunde 3."), n=3)]),
 chapter("house_vega", ("House Vega", "La Casa Vega"), 10, {}, [
  say("banker", ("The warehouse is yours, Captain, and every creditor has been paid. All that's missing is a house to go with the name.",
                 "El almacén es suyo, capitana, y se ha pagado a todos los acreedores. Solo falta una casa que vaya con el nombre."),
      ("Then let's build one.", "Entonces construyamos una.")),
  goal("deposit", ("Reopen House Vega: keep 150,000 in a bank.", "Reabre la Casa Vega: ten 150.000 en un banco."), amount=150000),
  goal("fleet", ("A trading house needs a fleet. Own four ships.", "Una casa de comercio necesita una flota. Ten cuatro barcos."), n=4),
  reward(100000),
  log(("House Vega opens its doors again in Puerto Ambar.", "La Casa Vega vuelve a abrir sus puertas en Puerto Ambar.")),
  END]),
])
