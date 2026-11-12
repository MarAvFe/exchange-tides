"""Turncoat - Rafe Moreno, 1701. Acts: Running (1-7), The Pardon (8-14), The Hound (15-21)."""
from sk import *

npc("brandt", ("Teo Brandt, bosun", "Teo Brandt, contramaestre"), "crew", False, 17012, "portrait_sailor")
npc("pia", ("Pia Sorel, of the Lark", "Pia Sorel, de la Alondra"), "crew", True, 17013, "portrait_sailor")
npc("brack", ("Captain Ottilie Brack", "Capitana Ottilie Brack"), "crew", True, 1701, "portrait_smuggler")

enemy("the_jackal", ("The Jackal", "El Chacal"), 110, 8, 0.9, 66, 14000, "ship_raider", 7)
enemy("the_hound", ("The Hound", "El Sabueso"), 290, 20, 0.8, 72, 50000, "ship_frigate_pirate", 11)

item("vega_letter", ("Vega's Letter", "Carta de Vega"),
     ("Marisol Vega's letter to Lieutenant Hale, sealed with the crest of a ruined house.", "La carta de Marisol Vega a la teniente Hale, sellada con el blasón de una casa arruinada."))
item("lark_log", ("Logbook of the Lark", "Diario de la Alondra"),
     ("Waterlogged, half the pages gone. Raiders give the ship that carries it a wide berth.", "Empapado, con la mitad de las páginas perdidas. Los corsarios se apartan del barco que lo lleva."), "sailing_combat_frequency(-10%)")
item("pia_statement", ("Pia Sorel's Statement", "La declaración de Pia Sorel"),
     ("What a survivor of the Lark saw from the water, signed before a magistrate.", "Lo que una superviviente de la Alondra vio desde el agua, firmado ante un magistrado."))

HALE = ("Lieutenant Ada Hale", "Teniente Ada Hale")

STORY = campaign("turncoat", ("Turncoat", "Chaquetero"), 1701,
 ("1701. Rafe Moreno was sailing master on Commodore Grimmer's frigate for four years. Last month he watched Grimmer burn a merchant ship, the Lark, with her crew still aboard. That night Moreno took a schooner and twelve men and slipped away. Grimmer wants the schooner back and Moreno on the bottom.",
  "1701. Rafe Moreno fue piloto de la fragata del comodoro Grimmer durante cuatro años. El mes pasado vio a Grimmer quemar un barco mercante, la Alondra, con la tripulación a bordo. Esa noche Moreno se llevó una goleta y doce hombres y se escabulló. Grimmer quiere recuperar la goleta y ver a Moreno en el fondo del mar."),
 ("Pardoned", "Indultado"),
 ("The Admiralty pardoned you and your twelve men. Brack's Hound was towed into port under a borrowed flag, and the Lark's log went into Lieutenant Hale's strongbox. The next year a merchant captain from Puerto Ambar went after Grimmer herself. You drank to her in every tavern that would still serve you.",
  "El Almirantazgo os indultó a ti y a tus doce hombres. El Sabueso de Brack entró a remolque en puerto bajo una bandera prestada, y el diario de la Alondra acabó en el cofre de la teniente Hale. Al año siguiente, una capitana mercante de Puerto Ambar fue en persona a por Grimmer. Brindaste por ella en cada taberna que aún te servía."),
[
 # ---------------- Act I: Running
 chapter("running", ("Running", "A la fuga"), 0, {"p1": "other"}, [
  say("barkeep", ("Grimmer's people were in here last night asking after you, Rafe. I told them you'd drowned. They'll check.",
                  "Anoche estuvo aquí la gente de Grimmer preguntando por ti, Rafe. Les dije que te habías ahogado. Lo comprobarán."),
      ("Already gone.", "Ya me he ido.")),
  goal("arrive", ("Get clear of Blackwater Cay: sail to {p1}.", "Aléjate de Cayo Aguanegra: navega a {p1}."), port="{p1}"),
  say("brandt", ("Twelve of us came with you, captain. Twelve of us borrowed from the Blackwater lender to pay for the quiet. He'll sell us to Grimmer if we don't pay him back.",
                 "Doce vinimos contigo, capitán. Los doce pedimos prestado al prestamista de Aguanegra para pagar su silencio. Nos venderá a Grimmer si no le devolvemos el dinero."),
      ("Then we pay him back.", "Entonces se lo devolvemos."))]),
 chapter("scouts", ("Scouts", "Exploradores"), 0, {}, [
  goal("combat", ("Grimmer's scouts are on your wake. Win a fight against them.", "Los exploradores de Grimmer siguen tu estela. Gana un combate contra ellos."), wins=1),
  say("brandt", ("They were flying Grimmer's pennant and still they hesitated, captain. They know your schooner. Half of them learned to sail on her.",
                 "Llevaban el gallardete de Grimmer y aun así dudaron, capitán. Conocen tu goleta. La mitad aprendió a navegar en ella."),
      ("Hesitating men miss.", "Quien duda, falla.")),
  unlock("spice"),
  goal("networth", ("Start trading to pay the crew: reach a net worth of 8,000.", "Empieza a comerciar para pagar a la tripulación: alcanza un patrimonio de 8.000."), amount=8000)]),
 chapter("quiet", ("Paying for Quiet", "El precio del silencio"), 1, {}, [
  goal("repay", ("Pay off the Blackwater lender before Grimmer outbids you.", "Paga al prestamista de Aguanegra antes de que Grimmer puje más que tú.")),
  say("brandt", ("Debt's clear. The lads say they'll follow you anywhere now, as long as it isn't back.", "Deuda saldada. Los muchachos dicen que ahora te seguirán a donde sea, mientras no sea de vuelta."),
      ("It won't be.", "No lo será."))]),
 chapter("cover", ("Cotton and Lies", "Algodón y mentiras"), 1, {"p2": "other,new,has:market"}, [
  say("brandt", ("Your face is on a poster in every port Grimmer pays for. A cotton trader is the dullest man on any quay. Nobody looks at a cotton trader.",
                 "Tu cara está en un cartel en cada puerto que paga Grimmer. Un tratante de algodón es el hombre más aburrido de cualquier muelle. Nadie mira a un tratante de algodón."),
      ("Then I'm a cotton trader.", "Entonces soy tratante de algodón.")),
  goal("deliver", ("Sell yourself as a cotton trader: bring 30 Cotton Bales to {p2}.", "Hazte pasar por tratante de algodón: lleva 30 de Fardos de algodón a {p2}."), good="cotton", amount=30, port="{p2}"),
  take("cotton", 30),
  reward(6000),
  log(("Nobody on the quay at {p2} looked twice at a cotton trader.", "Nadie en el muelle de {p2} miró dos veces a un tratante de algodón."))]),
 chapter("lark_ghost", ("The Lark's Ghost", "El fantasma de la Alondra"), 2, {"p3": "other,new,has:tavern"}, [
  say("brandt", ("You've been talking in your sleep, captain. About the Lark. There's a woman in {p3} who says she swam from her. Pia Sorel.",
                 "Hablas en sueños, capitán. De la Alondra. Hay una mujer en {p3} que dice que salió nadando de ella. Pia Sorel."),
      ("Then I owe her a visit.", "Entonces le debo una visita.")),
  goal("talk", ("Find Pia Sorel at the tavern in {p3}.", "Busca a Pia Sorel en la taberna de {p3}."), npc="pia", port="{p3}", building="tavern"),
  say("pia", ("I know your face. You were on his quarterdeck while we burned. Give me one reason not to call the bailiffs.",
              "Conozco tu cara. Estabas en su alcázar mientras ardíamos. Dame una razón para no llamar a los alguaciles."),
      ("Because I want him hanged for it.", "Porque quiero que lo ahorquen por ello.")),
  say("pia", ("Two of us got off. Tomas sold the logbook to pay his passage home. I don't know where. Find it, and I might believe you.",
              "Salimos dos. Tomas vendió el diario de a bordo para pagarse el pasaje a casa. No sé dónde. Encuéntralo y puede que te crea."),
      ("I'll find it.", "Lo encontraré.")),
  unlock("arms")]),
 chapter("old_colours", ("Old Colours", "Viejos colores"), 2, {}, [
  log(("Grimmer's raiders know your schooner. Some fire high on purpose.", "Los corsarios de Grimmer conocen tu goleta. Algunos disparan alto a propósito.")),
  goal("combat", ("Win 2 fights against Grimmer's raiders.", "Gana 2 combates contra los corsarios de Grimmer."), wins=2),
  goal("networth", ("Keep the crew fed and armed: reach a net worth of 25,000.", "Mantén a la tripulación comida y armada: alcanza un patrimonio de 25.000."), amount=25000)]),
 chapter("heir", ("The Heir", "La heredera"), 3, {}, [
  goal("talk", ("A merchant heir in Puerto Ambar is asking questions about Grimmer. Find her at the market.", "Una heredera mercante de Puerto Ambar anda haciendo preguntas sobre Grimmer. Búscala en el mercado."), npc="vega", port="puerto_ambar", building="market"),
  say("vega", ("You sailed for him. Grimmer's raiders took three of my family's ships, and our house went under. I want to know why.",
               "Navegaste para él. Los corsarios de Grimmer se llevaron tres barcos de mi familia, y nuestra casa se hundió. Quiero saber por qué."),
      ("Your ships wouldn't pay him for safe passage.", "Vuestros barcos no quisieron pagarle por el paso seguro.")),
  say("vega", ("Then help me prove it. There's a lieutenant in the Admiralty, Ada Hale, who still reads her letters. Take her this one from me.",
               "Entonces ayúdame a probarlo. Hay una teniente en el Almirantazgo, Ada Hale, que todavía lee sus cartas. Llévale esta de mi parte."),
      ("One letter. Then I'm gone.", "Una carta. Y luego me voy.")),
  get("vega_letter")]),
 # ---------------- Act II: The Pardon
 chapter("hale", ("The Lieutenant", "La teniente"), 3, {"p4": "other,new,has:governor"}, [
  goal("talk", ("Bring Vega's letter to Lieutenant Hale at the governor's house in {p4}.", "Lleva la carta de Vega a la teniente Hale, en la casa de la gobernación de {p4}."), npc="hale", port="{p4}", building="governor"),
  give("vega_letter"),
  say("hale", ("A deserter from Grimmer's own quarterdeck. Give me something I can check, Moreno, and I'll put your name on a pardon. What happened to the Lark?",
               "Un desertor del propio alcázar de Grimmer. Deme algo que pueda comprobar, Moreno, y pondré su nombre en un indulto. ¿Qué le pasó a la Alondra?"),
      ("He burned her. With the crew aboard.", "La quemó. Con la tripulación a bordo.")),
  say("hale", ("I believe you. The Admiralty won't, not on your word. Bring me the Lark's log, or a survivor who'll swear to what she saw.",
               "Le creo. El Almirantazgo no, no con su palabra. Tráigame el diario de la Alondra, o una superviviente que jure lo que vio."),
      ("I know where to start.", "Sé por dónde empezar.")),
  unlock("textiles")]),
 chapter("log", ("The Lark's Log", "El diario de la Alondra"), 4, {"p5": "other,new,has:curio"}, [
  say("brandt", ("A sailor called Tomas sold a burned logbook to a curio dealer in {p5}, the lads say. Paid for his passage with it.",
                 "Dicen los muchachos que un marinero llamado Tomas vendió un diario quemado a un anticuario de {p5}. Se pagó el pasaje con él."),
      ("Set a course.", "Pon rumbo.")),
  goal("talk", ("The Lark's logbook was sold to the curio dealer at {p5}.", "El diario de la Alondra se vendió al anticuario de {p5}."), npc="curio", port="{p5}", building="curio"),
  say("curio", ("Waterlogged, half the pages gone. I was going to ask a price. Take it. I don't want anything Grimmer's men are looking for.",
                "Empapado, con la mitad de las páginas perdidas. Iba a pedirle un precio. Lléveselo. No quiero nada que busquen los hombres de Grimmer."),
      ("Thank you.", "Gracias.")),
  get("lark_log"),
  goal("networth", ("Grimmer will pay well for that book. Make yourself harder to buy: reach a net worth of 45,000.", "Grimmer pagará bien por ese diario. Hazte más difícil de comprar: alcanza un patrimonio de 45.000."), amount=45000)]),
 chapter("wolves", ("Wolves", "Lobos"), 4, {}, [
  log(("Grimmer knows you have the log. His wolves are out.", "Grimmer sabe que tienes el diario. Sus lobos han salido.")),
  goal("sink", ("Sink 3 of Grimmer's wolves before they find your crew.", "Hunde 3 lobos de Grimmer antes de que den con tu tripulación."), n=3),
  unlock("tobacco")]),
 chapter("jackal", ("The Jackal", "El Chacal"), 5, {"p6": "other,new"}, [
  say("brack", ("Rafe. We have your bosun. Big man, talks too much about you. Bring me the book, alone, off {p6}, and you can have him back.",
                "Rafe. Tenemos a tu contramaestre. Un hombretón, habla demasiado de ti. Tráeme el diario, solo, frente a {p6}, y te lo devuelvo."),
      ("I'll come. I won't come alone.", "Iré. No iré solo."), ("Captain Ottilie Brack", "Capitana Ottilie Brack")),
  goal("npccombat", ("Brack's sloop, the Jackal, holds Teo Brandt off {p6}. Take him back.", "La balandra de Brack, el Chacal, retiene a Teo Brandt frente a {p6}. Recupéralo."), enemy="the_jackal", port="{p6}"),
  say("brandt", ("Took you long enough, captain. Brack wasn't aboard. She left her mate to lose the fight for her. That's how she does it.",
                 "Ya era hora, capitán. Brack no iba a bordo. Dejó a su segundo perder el combate por ella. Así lo hace ella."),
      ("She learned that from me.", "Eso lo aprendió de mí.")),
  log(("Teo Brandt is back aboard. Brack wasn't on the Jackal.", "Teo Brandt vuelve a bordo. Brack no iba en el Chacal."))]),
 chapter("spread", ("Spreading Out", "Repartirse"), 5, {}, [
  say("brandt", ("Twelve men on one schooner is one target. Put some of us on a second hull and Grimmer has to choose.",
                 "Doce hombres en una goleta son un solo blanco. Pon a algunos en un segundo casco y Grimmer tendrá que elegir."),
      ("Then we'll make him choose.", "Entonces haremos que elija.")),
  goal("fleet", ("Buy a second ship and split the crew.", "Compra un segundo barco y reparte a la tripulación."), n=2),
  goal("networth", ("Keep both crews paid: reach a net worth of 70,000.", "Mantén pagadas a las dos tripulaciones: alcanza un patrimonio de 70.000."), amount=70000)]),
 chapter("witness", ("The Second Witness", "La segunda testigo"), 6, {}, [
  goal("talk", ("Show Pia Sorel in {p3} the Lark's log.", "Enséñale a Pia Sorel, en {p3}, el diario de la Alondra."), npc="pia", port="{p3}", building="tavern"),
  say("pia", ("That's the captain's hand. That's the last page he wrote, the night before. ... All right. I'll swear to what I saw from the water. But my mother lost her house when the Lark went down, and I want it back.",
              "Esa es la letra del capitán. Esa es la última página que escribió, la noche antes. ... Está bien. Juraré lo que vi desde el agua. Pero mi madre perdió su casa cuando se hundió la Alondra, y la quiero de vuelta."),
      ("Then she'll have it.", "Entonces la tendrá.")),
  goal("deposit", ("Buy back the Sorel house: keep 30,000 in a bank.", "Recompra la casa de los Sorel: ten 30.000 en un banco."), amount=30000),
  get("pia_statement"),
  log(("Pia Sorel signed her statement before a magistrate.", "Pia Sorel firmó su declaración ante un magistrado."))]),
 chapter("bounty", ("Grimmer's Bounty", "La recompensa de Grimmer"), 6, {}, [
  say("barkeep", ("Your price went up again, Rafe. Ten thousand for you, five for the schooner, and a barrel of rum for every one of your men. Grimmer must be worried.",
                  "Tu precio ha vuelto a subir, Rafe. Diez mil por ti, cinco por la goleta y un barril de ron por cada uno de tus hombres. Grimmer debe de estar preocupado."),
      ("Good. Worried men make mistakes.", "Bien. Los hombres preocupados cometen errores.")),
  goal("combat", ("Bounty hunters are out. Win 2 fights.", "Hay cazarrecompensas sueltos. Gana 2 combates."), wins=2),
  goal("networth", ("Stay ahead of the bounty: reach a net worth of 100,000.", "Mantente por delante de la recompensa: alcanza un patrimonio de 100.000."), amount=100000)]),
 # ---------------- Act III: The Hound
 chapter("pardon_case", ("The Case", "El caso"), 6, {}, [
  goal("talk", ("Bring the log and Pia's statement to Lieutenant Hale in {p4}.", "Lleva el diario y la declaración de Pia a la teniente Hale en {p4}."), npc="hale", port="{p4}", building="governor"),
  say("hale", ("The log and a sworn witness. That's a case, Moreno. I'll send it to the Admiralty board. It'll take months, and Grimmer will hear about it in weeks.",
               "El diario y una testigo jurada. Eso ya es un caso, Moreno. Lo mandaré al tribunal del Almirantazgo. Tardará meses, y Grimmer se enterará en semanas."),
      ("Then I'll keep moving.", "Entonces seguiré moviéndome.")),
  goal("contracts", ("Governors who owe you are harder for Grimmer to buy. Complete 3 governor contracts.", "Los gobernadores que te deben favores son más difíciles de comprar para Grimmer. Cumple 3 contratos de gobernador."), n=3),
  unlock("wine")]),
 chapter("chart_maker", ("The Chart-Maker", "El cartógrafo"), 7, {"p7": "other,new,has:shipyard"}, [
  say("hale", ("One more question. Where does Grimmer anchor? If I'm to go after him one day, I need his chart.",
               "Una pregunta más. ¿Dónde fondea Grimmer? Si algún día voy a por él, necesito su carta náutica."),
      ("He moves every season. Only his chart-maker knows where.", "Cambia cada temporada. Solo su cartógrafo sabe dónde.")),
  say("brandt", ("The chart-maker's sister builds boats in {p7}, captain. She doesn't know what her brother draws for a living.",
                 "La hermana del cartógrafo construye barcos en {p7}, capitán. No sabe para quién dibuja su hermano."),
      ("Then somebody should warn her.", "Entonces alguien debería avisarla.")),
  goal("talk", ("Warn the shipwright at {p7} about her brother's employer.", "Avisa a la carpintera de ribera de {p7} sobre el patrón de su hermano."), npc="shipwright", port="{p7}", building="shipyard"),
  say("shipwright", ("My brother draws charts for a commodore. He says it pays well and he can't say more. ... You're telling me it's Grimmer. If anything happens to him, I'll know who to ask for help.",
                     "Mi hermano dibuja cartas para un comodoro. Dice que pagan bien y que no puede contar más. ... Me estás diciendo que es Grimmer. Si le pasa algo, sabré a quién pedir ayuda."),
      ("Ask the Admiralty for Lieutenant Hale.", "Pregunta en el Almirantazgo por la teniente Hale.")),
  log(("You warned the chart-maker's sister. If Grimmer takes her brother, she'll go to Hale.", "Avisaste a la hermana del cartógrafo. Si Grimmer se lleva a su hermano, acudirá a Hale."))]),
 chapter("brack_offer", ("Brack's Offer", "La oferta de Brack"), 8, {}, [
  say("brack", ("Rafe. You taught me to sail, so I'll make this quick. Give me the schooner and the book, and Grimmer lets your crew live. Refuse, and I come with the Hound.",
                "Rafe. Tú me enseñaste a navegar, así que seré rápida. Dame la goleta y el diario, y Grimmer deja vivir a tu tripulación. Si te niegas, vendré con el Sabueso."),
      ("You'll have to come and take them.", "Tendrás que venir a quitármelos."), ("Captain Ottilie Brack", "Capitana Ottilie Brack")),
  goal("fleet", ("You'll need every hull against the Hound. Sail with three ships.", "Necesitarás todos los cascos contra el Sabueso. Navega con tres barcos."), n=3),
  goal("sink", ("Brack's escorts are gathering. Sink 2 of them.", "Los escoltas de Brack se están reuniendo. Hunde 2."), n=2)]),
 chapter("vega_again", ("The Heir's Ship", "El barco de la heredera"), 8, {}, [
  goal("talk", ("Marisol Vega has sent for you. Find her at the market in Puerto Ambar.", "Marisol Vega te ha mandado llamar. Búscala en el mercado de Puerto Ambar."), npc="vega", port="puerto_ambar", building="market"),
  say("vega", ("I'm fitting out a sloop. My mother's ledger, my father's name and every coin I could borrow. Lieutenant Hale says you're the man who'd know what a merchant should carry against Grimmer.",
               "Estoy aparejando una balandra. El libro de mi madre, el nombre de mi padre y cada moneda que he podido pedir prestada. La teniente Hale dice que usted es el hombre que sabría qué debe llevar un mercader contra Grimmer."),
      ("Muskets, and the nerve to use them.", "Mosquetes, y valor para usarlos.")),
  goal("deliver", ("Bring 10 Muskets to Vega in Puerto Ambar for her new ship.", "Lleva 10 de Mosquetes a Vega en Puerto Ambar para su barco nuevo."), good="arms", amount=10, port="puerto_ambar"),
  take("arms", 10),
  say("vega", ("Thank you, Mister Moreno. If I ever find Grimmer, I'll tell him who armed me.", "Gracias, señor Moreno. Si alguna vez encuentro a Grimmer, le diré quién me armó."),
      ("Don't. Just hit him.", "No se lo diga. Péguele.")),
  reward(30000)]),
 chapter("hound", ("The Hound", "El Sabueso"), 9, {"p8": "other,new"}, [
  goal("networth", ("Refit for the fight: build a net worth of 200,000.", "Prepárate para el combate: alcanza un patrimonio de 200.000."), amount=200000),
  goal("npccombat", ("Brack and the Hound are waiting off {p8}.", "Brack y el Sabueso esperan frente a {p8}."), enemy="the_hound", port="{p8}"),
  say("brack", ("You always did fight better than you lied, Rafe. Take the Hound. Grimmer won't forgive me for losing her anyway.",
                "Siempre peleaste mejor de lo que mentías, Rafe. Quédate el Sabueso. Grimmer no me perdonará haberlo perdido de todos modos."),
      ("Come with us.", "Ven con nosotros."), ("Captain Ottilie Brack", "Capitana Ottilie Brack")),
  log(("The Hound struck her colours. Brack went over the side in the night and swam for it.", "El Sabueso arrió su bandera. Brack se tiró por la borda de noche y se fue nadando."))]),
 chapter("pardon", ("Pardon", "Indulto"), 10, {}, [
  goal("talk", ("Bring the Hound's colours to Lieutenant Hale in {p4}.", "Lleva la bandera del Sabueso a la teniente Hale en {p4}."), npc="hale", port="{p4}", building="governor"),
  say("hale", ("The Lark's log, a sworn witness and the Hound's colours. That's enough for your pardon, Moreno. It isn't enough for Grimmer. He moves his anchorage every season, and only his chart-maker knows where.",
               "El diario de la Alondra, una testigo jurada y la bandera del Sabueso. Basta para su indulto, Moreno. No basta para Grimmer. Cambia de fondeadero cada temporada, y solo su cartógrafo sabe dónde."),
      ("His sister will come to you.", "Su hermana acudirá a usted.")),
  say("hale", ("Marisol Vega will sail within the year. If she comes to me, I'll know what to tell her.", "Marisol Vega zarpará antes de un año. Si viene a verme, sabré qué decirle."),
      ("Tell her the Lark's crew were good people.", "Dígale que la tripulación de la Alondra era buena gente.")),
  log(("Pardoned. The Lark's log is with Lieutenant Hale.", "Indultado. El diario de la Alondra está en manos de la teniente Hale."))]),
 chapter("crew_shares", ("Shares", "El reparto"), 10, {}, [
  say("brandt", ("Pardoned men, captain. All twelve. The lads are asking what we do now.", "Hombres indultados, capitán. Los doce. Los muchachos preguntan qué hacemos ahora."),
      ("We trade, and we pay everyone their share.", "Comerciamos, y le pagamos a cada uno su parte.")),
  goal("deposit", ("Pay twelve men their shares: keep 90,000 in a bank.", "Paga a los doce hombres su parte: ten 90.000 en un banco."), amount=90000),
  goal("talk", ("Tell Pia Sorel in {p3} that her mother's house is hers again.", "Dile a Pia Sorel, en {p3}, que la casa de su madre vuelve a ser suya."), npc="pia", port="{p3}", building="tavern"),
  say("pia", ("I didn't think you'd do it. ... There's a berth on your ship for a woman who swims well?", "No pensé que lo harías. ... ¿Hay sitio en tu barco para una mujer que nada bien?"),
      ("There is now.", "Ahora sí.")),
  reward(80000),
  END]),
])
