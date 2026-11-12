"""The Second Seal - Ines 'Ash' Calder, 1699. Acts: Wanted Again (1-7), The Second Seal (8-14), Clean Hands (15-21)."""
from sk import *

npc("fenn", ("Mattias Fenn, engraver", "Mattias Fenn, grabador"), "merchant", False, 16991, "portrait_merchant")
npc("lisle", ("Ewan Lisle", "Ewan Lisle"), "merchant", False, 1699, "portrait_merchant")
npc("brack", ("Captain Ottilie Brack", "Capitana Ottilie Brack"), "crew", True, 1701, "portrait_smuggler")

enemy("second_seal", ("The Second Seal", "El Segundo Sello"), 80, 6, 1.0, 64, 9000, "ship_sloop_pirate", 6)
enemy("the_whelp", ("The Whelp", "El Cachorro"), 150, 11, 0.9, 68, 20000, "ship_brigantine_pirate", 8)
enemy("gilded_purse", ("The Gilded Purse", "La Bolsa Dorada"), 270, 19, 0.8, 72, 50000, "ship_galleon_pirate", 10)

item("forged_seal", ("Forged Customs Seal", "Sello de aduana falsificado"),
     ("Struck from steel, with your mark, off a crate of raiders' muskets.", "Estampado en acero, con tu marca, sacado de una caja de mosquetes corsarios."))
item("steel_die", ("The Steel Die", "El troquel de acero"),
     ("The die Lisle cut. You can tell any forged seal from a real one now, and so can the customs men you show it to.", "El troquel que talló Lisle. Ahora distingues cualquier sello falso de uno auténtico, y también los aduaneros a los que se lo enseñas."), "contraband_seizure(-30%)")
item("brack_receipts", ("Brack's Receipts", "Los recibos de Brack"),
     ("Payments from Crowe & Daughters to a raider captain, in Lisle's handwriting.", "Pagos de Crowe e Hijas a una capitana corsaria, con la letra de Lisle."))

STORY = campaign("second_seal", ("The Second Seal", "El Segundo Sello"), 1699,
 ("1699. Ines Calder, called Ash, cut customs seals for half the smugglers in the Reach until Saltmere put her name on a gallows notice. This spring her mark started turning up on crates of muskets sold to raiders. She didn't cut those seals.",
  "1699. Ines Calder, a la que llaman Ceniza, tallaba sellos de aduana para medio contrabando del Estrecho hasta que Salmar puso su nombre en un cartel de horca. Esta primavera su marca empezó a aparecer en cajas de mosquetes vendidas a corsarios. Esos sellos no los talló ella."),
 ("Partners in Smoke", "Socias de humo"),
 ("Your name came off the musket notices, though Saltmere still wants you for the old seals. Ewan Lisle went to prison and Dimas Crowe went back to buying up markets. You signed half shares with Nell Varga at a table in Blackwater Cay, and neither of you read the contract.",
  "Tu nombre desapareció de los carteles de los mosquetes, aunque Salmar aún te busca por los sellos viejos. Ewan Lisle fue a la cárcel y Dimas Crowe volvió a acaparar mercados. Firmaste a medias con Nell Varga en una mesa de Cayo Aguanegra, y ninguna de las dos leyó el contrato."),
[
 # ---------------- Act I: Wanted Again
 chapter("wanted", ("Wanted Again", "Buscada otra vez"), 0, {}, [
  say("barkeep", ("There's a new notice on the harbour wall, Ash. Your face, your name, and a fresh charge: customs seals on musket crates bound for raiders. Somebody's using your mark.",
                  "Hay un cartel nuevo en el muro del puerto, Ceniza. Tu cara, tu nombre y un cargo fresco: sellos de aduana en cajas de mosquetes para corsarios. Alguien está usando tu marca."),
      ("My mark's the only honest thing I own.", "Mi marca es lo único honrado que tengo.")),
  say("barkeep", ("Then mind your debts. Half this town would sell you to the Saltmere bailiffs for less than you owe.",
                  "Entonces cuida tus deudas. Medio pueblo te vendería a los alguaciles de Salmar por menos de lo que debes."),
      ("Fine. I'll pay everybody.", "Bien. Les pagaré a todos.")),
  goal("repay", ("Pay off your debt so nobody in Driftmoor has a reason to sell you out.", "Salda tu deuda para que nadie en Brumaria tenga motivos para venderte.")),
  log(("Paid off the moneylender. Driftmoor will keep its mouth shut, for now.", "Pagaste al prestamista. Brumaria mantendrá la boca cerrada, por ahora."))]),
 chapter("notice", ("The Notice", "El cartel"), 0, {}, [
  goal("talk", ("Ask the governor of Driftmoor who paid for the notice.", "Pregunta a la gobernación de Brumaria quién pagó el cartel."), npc="governor", port="driftmoor"),
  say("governor", ("Saltmere's bailiffs paid for it, and Saltmere pays a bounty I don't care to collect. I've no love for Saltmere. Keep your trade clean in my harbour and I'll keep forgetting your face.",
                   "Lo pagaron los alguaciles de Salmar, y Salmar paga una recompensa que no me interesa cobrar. Salmar no me cae bien. Mantén tu comercio limpio en mi puerto y yo seguiré olvidando tu cara."),
      ("Clean as a whistle, Reeve.", "Limpio como una patena, alcaldesa.")),
  unlock("spice"),
  goal("networth", ("Earn enough to travel: reach a net worth of 8,000.", "Gana lo suficiente para viajar: alcanza un patrimonio de 8.000."), amount=8000)]),
 chapter("teacher", ("Old Teacher", "La vieja maestra"), 1, {}, [
  goal("talk", ("Show the notice to Nell Varga at the tavern in Blackwater Cay.", "Enséñale el cartel a Nell Varga en la taberna de Cayo Aguanegra."), npc="varga", port="blackwater_cay", building="tavern"),
  say("varga", ("Sit down. A notice with your face on it. I taught you better than to get famous.", "Siéntate. Un cartel con tu cara. Te enseñé mejor que a hacerte famosa."),
      ("I didn't cut those seals, Nell.", "Yo no tallé esos sellos, Nell.")),
  say("varga", ("I know. You'd have spelled 'customs' right. Bring me twenty sugar for my rum men while I think about who did.",
                "Lo sé. Tú habrías escrito 'aduana' bien. Tráeme veinte de azúcar para mis destiladores de ron mientras pienso quién fue."),
      ("You never change.", "Tú nunca cambias.")),
  goal("deliver", ("Bring 20 Cane Sugar to Varga at Blackwater Cay.", "Lleva 20 de Azúcar de caña a Varga en Cayo Aguanegra."), good="sugar", amount=20, port="blackwater_cay"),
  take("sugar", 20),
  reward(8000)]),
 chapter("steel", ("Steel, Not Boxwood", "Acero, no boj"), 1, {}, [
  say("varga", ("I need a real crate seal in my hand, not a notice. Raiders carry them. Take one off a raider and bring it here.",
                "Necesito un sello de caja de verdad en la mano, no un cartel. Los corsarios los llevan. Quítale uno a un corsario y tráemelo."),
      ("One raider, coming up.", "Un corsario, marchando.")),
  goal("combat", ("Win a fight against raiders and take a sealed crate.", "Gana un combate contra corsarios y llévate una caja sellada."), wins=1),
  get("forged_seal"),
  say("varga", ("Steel die. Look at the edge, clean as a coin. Nobody carves that. Somebody paid a real engraver, and there aren't many in the Reach.",
                "Troquel de acero. Mira el canto, limpio como una moneda. Eso no se talla. Alguien pagó a un grabador de verdad, y en el Estrecho no hay muchos."),
      ("Then I'll find the engravers.", "Entonces buscaré a los grabadores."))]),
 chapter("engraver", ("The Engraver", "El grabador"), 2, {"p1": "other,new,has:curio", "p2": "other,new,has:tavern"}, [
  goal("talk", ("Curio dealers know every engraver alive. Ask the one at {p1}.", "Los anticuarios conocen a todos los grabadores vivos. Pregunta al de {p1}."), npc="curio", port="{p1}", building="curio"),
  say("curio", ("Steel dies? Only one man in the Reach ever cut them, old Mattias Fenn, who made the mint's coin stamps. Retired now, drinks in {p2}. His hands shake too much to have done this.",
                "¿Troqueles de acero? Solo un hombre en el Estrecho los ha tallado, el viejo Mattias Fenn, que hacía los cuños de la casa de la moneda. Ahora está retirado, bebe en {p2}. Le tiemblan demasiado las manos para haber hecho esto."),
      ("Then he taught someone.", "Entonces enseñó a alguien.")),
  goal("networth", ("Pay your way along the coast: reach a net worth of 16,000.", "Págate el viaje por la costa: alcanza un patrimonio de 16.000."), amount=16000)]),
 chapter("fenn", ("Mattias Fenn", "Mattias Fenn"), 2, {}, [
  goal("talk", ("Find Mattias Fenn at the tavern in {p2}.", "Busca a Mattias Fenn en la taberna de {p2}."), npc="fenn", port="{p2}", building="tavern"),
  say("fenn", ("Ash Calder. I've seen your boxwood work. Clumsy, but honest about it. This one isn't mine. I taught a boy last winter, a clerk with good eyes and no money. He bought my old tools on credit.",
               "Ash Calder. He visto tu trabajo en boj. Torpe, pero honrado en su torpeza. Este no es mío. El invierno pasado enseñé a un chico, un escribiente con buena vista y sin dinero. Me compró las herramientas viejas a crédito."),
      ("A name, Mister Fenn.", "Un nombre, señor Fenn.")),
  say("fenn", ("He never paid the credit. Bring me ten chests of spice for my wife's kitchen and I'll remember it.",
               "Nunca pagó el crédito. Tráeme diez cofres de especias para la cocina de mi mujer y me acordaré."),
      ("Ten chests. Remember hard.", "Diez cofres. Acuérdese bien.")),
  goal("deliver", ("Bring 10 Spice Chests to Mattias Fenn in {p2}.", "Lleva 10 de Cofres de especias a Mattias Fenn en {p2}."), good="spice", amount=10, port="{p2}"),
  take("spice", 10),
  say("fenn", ("Ewan Lisle. Clerk to some merchant who buys a great deal of everything. Thin, ink to the elbows.", "Ewan Lisle. Escribiente de algún mercader que compra muchísimo de todo. Flaco, con tinta hasta los codos."),
      ("Ewan Lisle. Thank you.", "Ewan Lisle. Gracias.")),
  unlock("tobacco")]),
 chapter("crates", ("Ten Crates", "Diez cajas"), 3, {"p3": "other,new,has:market"}, [
  say("varga", ("Word came back. A merchant called Dimas Crowe has bought muskets in three ports this season. Crowe & Daughters, he calls his house. He has no daughters. His clerk is a Lisle.",
                "Ya hay respuesta. Un mercader llamado Dimas Crowe ha comprado mosquetes en tres puertos esta temporada. Crowe e Hijas, llama a su casa. No tiene hijas. Su escribiente es un tal Lisle."),
      ("A man who lies on his own signboard.", "Un hombre que miente hasta en su propio letrero.")),
  goal("talk", ("Ask the merchants of {p3} about Crowe's buying.", "Pregunta a los mercaderes de {p3} por las compras de Crowe."), npc="merchant", port="{p3}", building="market"),
  say("merchant", ("Crowe pays in good silver and wants receipts in other people's names. His clerk does the writing and sails a sloop called the Second Seal.",
                   "Crowe paga en buena plata y quiere los recibos a nombre de otros. Los escribe su escribiente, que navega en una balandra llamada el Segundo Sello."),
      ("The Second Seal. He's laughing at me.", "El Segundo Sello. Se está riendo de mí.")),
  unlock("arms"),
  goal("networth", ("Build a war chest: reach a net worth of 30,000.", "Reúne un fondo de guerra: alcanza un patrimonio de 30.000."), amount=30000)]),
 # ---------------- Act II: The Second Seal
 chapter("silver", ("Following the Silver", "Siguiendo la plata"), 3, {"p4": "other,new,has:bank"}, [
  say("varga", ("Muskets cost silver, and silver leaves a trail at the bank. Bankers talk to customers with deep pockets.",
                "Los mosquetes cuestan plata, y la plata deja rastro en el banco. Los banqueros hablan con los clientes de bolsillo hondo."),
      ("Then I'll have deep pockets.", "Entonces tendré los bolsillos hondos.")),
  goal("deposit", ("Keep 15,000 in a bank so the bankers take you seriously.", "Ten 15.000 en un banco para que los banqueros te tomen en serio."), amount=15000),
  goal("talk", ("Ask the banker in {p4} where Crowe's silver goes.", "Pregunta al banquero de {p4} adónde va la plata de Crowe."), npc="banker", port="{p4}", building="bank"),
  say("banker", ("Crowe & Daughters draws silver here every month, and a raider captain collects it. A woman called Ottilie Brack. She signs with a cross and counts every coin twice.",
                 "Crowe e Hijas retira plata aquí cada mes, y la recoge una capitana corsaria. Una tal Ottilie Brack. Firma con una cruz y cuenta cada moneda dos veces."),
      ("Crowe sells the raiders muskets and pays them too?", "¿Crowe vende mosquetes a los corsarios y encima les paga?")),
  say("banker", ("He pays them to raid his rivals. Then he buys the rivals' markets cheap. I never said any of this.",
                 "Les paga para que asalten a sus rivales. Luego compra barato los mercados de esos rivales. Yo no he dicho nada de esto."),
      ("Said what?", "¿Decir qué?"))]),
 chapter("muskets", ("Muskets at Sea", "Mosquetes en el mar"), 4, {}, [
  goal("sink", ("Brack's raiders carry crates under your seal. Sink 2 of them.", "Los corsarios de Brack llevan cajas con tu sello. Hunde 2."), n=2),
  log(("Two more crates with your mark go into Varga's cellar as evidence.", "Dos cajas más con tu marca van al sótano de Varga como prueba.")),
  goal("contracts", ("A smuggler with governors' work is harder to hang. Complete 2 governor contracts.", "A una contrabandista con encargos de gobernadores cuesta más ahorcarla. Cumple 2 contratos de gobernador."), n=2),
  unlock("textiles")]),
 chapter("two_hulls", ("Two Hulls", "Dos cascos"), 4, {}, [
  say("varga", ("The Second Seal is a fast little sloop. One ship chases, she runs. Two ships, she runs into the other one.",
                "El Segundo Sello es una balandra pequeña y rápida. Un barco la persigue y huye. Dos barcos, y huye hacia el otro."),
      ("Then I need a second ship.", "Entonces necesito un segundo barco.")),
  goal("fleet", ("Buy a second ship to cut off the Second Seal.", "Compra un segundo barco para cortarle el paso al Segundo Sello."), n=2),
  goal("networth", ("Arm both ships: reach a net worth of 55,000.", "Arma los dos barcos: alcanza un patrimonio de 55.000."), amount=55000)]),
 chapter("second_seal", ("The Second Seal", "El Segundo Sello"), 5, {"p5": "other,new"}, [
  say("barkeep", ("The Second Seal put in at {p5} for water. Her clerk was buying ink by the bottle.", "El Segundo Sello ha hecho escala en {p5} para hacer aguada. Su escribiente compraba tinta por botellas."),
      ("Ink. Of course he was.", "Tinta. Cómo no.")),
  goal("npccombat", ("Run down Crowe's clerk and the Second Seal off {p5}.", "Da caza al escribiente de Crowe y al Segundo Sello frente a {p5}."), enemy="second_seal", port="{p5}"),
  say("lisle", ("Mister Crowe said it was a joke! Your mark on his crates, the bailiffs chasing you, nobody looking at him. I only cut the die. I swear I only cut the die.",
                "¡El señor Crowe dijo que era una broma! Tu marca en sus cajas, los alguaciles detrás de ti y nadie mirándolo a él. Yo solo tallé el troquel. Lo juro, solo tallé el troquel."),
      ("Then you'll swear it to a governor.", "Pues lo jurarás ante un gobernador.")),
  get("steel_die"),
  log(("Captured Ewan Lisle, Crowe's clerk, and the steel die he cut.", "Capturaste a Ewan Lisle, el escribiente de Crowe, y el troquel de acero que talló.")),
  unlock("wine")]),
 chapter("lisle_price", ("Lisle's Price", "El precio de Lisle"), 5, {}, [
  say("lisle", ("Crowe will have me killed before I reach any governor. He has people in every port. Please. Somewhere he can't reach.",
                "Crowe me hará matar antes de que llegue ante ningún gobernador. Tiene gente en todos los puertos. Por favor. Algún sitio donde no llegue."),
      ("There's one port Crowe doesn't own.", "Hay un puerto que Crowe no controla.")),
  goal("talk", ("Hide Lisle with Varga at the tavern in Blackwater Cay.", "Esconde a Lisle con Varga en la taberna de Cayo Aguanegra."), npc="varga", port="blackwater_cay", building="tavern"),
  say("varga", ("You've brought me a clerk. I asked for sugar. ... Fine. He sleeps in the cellar with your crates. If he steals the rum I'll drown him myself.",
                "Me traes un escribiente. Yo te pedí azúcar. ... Bien. Dormirá en el sótano con tus cajas. Si me roba el ron, lo ahogo yo misma."),
      ("He won't touch the rum.", "No tocará el ron.")),
  say("crowe", ("Miss Calder. My clerk is a fool, and you're welcome to him. Let's be practical. Twenty thousand in silver, and you forget my name.",
                "Señorita Calder. Mi escribiente es un necio, y es todo suyo. Seamos prácticos. Veinte mil en plata, y usted olvida mi nombre."),
      ("Keep your silver, Mister Crowe.", "Guárdese su plata, señor Crowe.")),
  goal("networth", ("Crowe's money is everywhere. Build a net worth of 80,000.", "El dinero de Crowe está en todas partes. Alcanza un patrimonio de 80.000."), amount=80000)]),
 chapter("revenge", ("Crowe's Revenge", "La venganza de Crowe"), 6, {}, [
  log(("Crowe has paid every raider on the coast to sink your ships.", "Crowe ha pagado a todos los corsarios de la costa para que hundan tus barcos.")),
  goal("combat", ("Crowe's hired raiders come for you. Win 2 fights.", "Los corsarios a sueldo de Crowe vienen a por ti. Gana 2 combates."), wins=2),
  goal("contracts", ("Keep the governors on your side: complete 2 more contracts.", "Mantén a los gobernadores de tu lado: cumple 2 contratos más."), n=2)]),
 chapter("whelp", ("The Whelp", "El Cachorro"), 6, {"p6": "other,new"}, [
  say("brack", ("You're the seal-cutter. Crowe says you cost him a clerk and a die. He's paying me double to take them back, and I'd like the money.",
                "Tú eres la talladora de sellos. Crowe dice que le has costado un escribiente y un troquel. Me paga el doble por recuperarlos, y me vendría bien el dinero."),
      ("Come and get them, Captain.", "Ven a por ellos, capitana.")),
  goal("npccombat", ("Brack's brig, the Whelp, is waiting off {p6}. Beat her.", "El bergantín de Brack, el Cachorro, espera frente a {p6}. Derrótalo."), enemy="the_whelp", port="{p6}"),
  get("brack_receipts"),
  log(("Brack escaped in a boat, but her cabin held Crowe's receipts in Lisle's hand.", "Brack escapó en un bote, pero en su camarote estaban los recibos de Crowe con la letra de Lisle."))]),
 # ---------------- Act III: Clean Hands
 chapter("shadow", ("Saltmere's Shadow", "La sombra de Salmar"), 7, {"p7": "other,new,has:governor"}, [
  goal("talk", ("Find a governor who will hear Lisle. Try {p7}.", "Busca un gobernador que escuche a Lisle. Prueba en {p7}."), npc="governor", port="{p7}"),
  say("governor", ("Saltmere wants you for the old seals, Miss Calder, and Saltmere is a powerful friend to lose. I'll hear your clerk, but I need to know you'll still be trading here next year. Show me a house of real standing.",
                   "Salmar la busca por los sellos viejos, señorita Calder, y Salmar es un amigo poderoso como para perderlo. Escucharé a su escribiente, pero necesito saber que el año que viene seguirá comerciando aquí. Muéstreme una casa con peso de verdad."),
      ("You'll have one.", "La tendrá.")),
  goal("networth", ("Build a house of standing: reach a net worth of 130,000.", "Levanta una casa con peso: alcanza un patrimonio de 130.000."), amount=130000)]),
 chapter("varga_debt", ("Varga's Bail", "La fianza de Varga"), 7, {"p8": "other,new,has:governor"}, [
  say("barkeep", ("Bad news, Ash. Customs took Nell Varga at {p8}, with a hold full of tobacco. Someone tipped them off. The bail's steep.",
                  "Malas noticias, Ceniza. La aduana se llevó a Nell Varga en {p8}, con la bodega llena de tabaco. Alguien dio el soplo. La fianza es alta."),
      ("Crowe.", "Crowe.")),
  goal("cash", ("Raise 40,000 in cash for Varga's bail.", "Reúne 40.000 en efectivo para la fianza de Varga."), amount=40000),
  goal("talk", ("Pay Varga's bail at the governor's house in {p8}.", "Paga la fianza de Varga en la casa de la gobernación de {p8}."), npc="governor", port="{p8}"),
  say("varga", ("Forty thousand. For an old smuggler with bad knees. You're a worse businesswoman than I taught you to be.",
                "Cuarenta mil. Por una vieja contrabandista con las rodillas mal. Eres peor negociante de lo que te enseñé."),
      ("I'd rather owe you.", "Prefiero deberte a ti.")),
  log(("Paid Nell Varga's bail.", "Pagaste la fianza de Nell Varga."))]),
 chapter("allies", ("Allies", "Aliados"), 8, {}, [
  say("varga", ("Crowe won't stop at me. Get your ships together, all of them, and keep them together until this is done.",
                "Crowe no se detendrá conmigo. Reúne tus barcos, todos, y mantenlos juntos hasta que esto acabe."),
      ("Three hulls and a grudge.", "Tres cascos y un rencor.")),
  goal("fleet", ("Sail with three ships.", "Navega con tres barcos."), n=3),
  goal("sink", ("Clear Crowe's raiders off the routes: sink 3.", "Limpia las rutas de corsarios de Crowe: hunde 3."), n=3)]),
 chapter("fenn_word", ("The Engraver's Word", "La palabra del grabador"), 8, {}, [
  say("varga", ("A governor will ask how a clerk learned to cut steel. Your old engraver can answer that better than the clerk can.",
                "Un gobernador preguntará cómo aprendió un escribiente a tallar acero. Tu viejo grabador puede responder eso mejor que el escribiente."),
      ("Fenn won't like a courtroom.", "A Fenn no le gustarán los tribunales.")),
  goal("talk", ("Ask Mattias Fenn in {p2} to speak at the hearing.", "Pide a Mattias Fenn, en {p2}, que hable en la vista."), npc="fenn", port="{p2}", building="tavern"),
  say("fenn", ("I'll go. My wife says the spice was the best she's had in years, and a man should pay his debts. Besides, I'd like to see Lisle's face when I tell them his letter 'R' leans left.",
               "Iré. Mi mujer dice que las especias eran las mejores en años, y uno debe pagar sus deudas. Además, quiero ver la cara de Lisle cuando les cuente que su 'R' se inclina a la izquierda."),
      ("Does it?", "¿Y es así?")),
  say("fenn", ("Every single one. Bring me eight bolts of fine cloth for a respectable coat, and I'll be there.", "Todas y cada una. Tráeme ocho de telas finas para una casaca respetable, y allí estaré."),
      ("Eight bolts. You'll look like a governor.", "Ocho piezas. Parecerá un gobernador.")),
  goal("deliver", ("Bring 8 Fine Cloth to Mattias Fenn in {p2}.", "Lleva 8 de Telas finas a Mattias Fenn en {p2}."), good="textiles", amount=8, port="{p2}"),
  take("textiles", 8)]),
 chapter("court", ("The Hearing", "La vista"), 9, {}, [
  goal("talk", ("Bring Lisle, the die and Brack's receipts to the governor of {p7}.", "Lleva a Lisle, el troquel y los recibos de Brack ante la gobernación de {p7}."), npc="governor", port="{p7}"),
  say("governor", ("The die matches the seals, the receipts match the clerk's hand, and the clerk has confessed. The musket charge against you is dropped. Saltmere's old charges are Saltmere's business. As for Crowe, a clerk's word won't hang a man with that much silver.",
                   "El troquel coincide con los sellos, los recibos con la letra del escribiente, y el escribiente ha confesado. Se retira el cargo de los mosquetes. Los cargos viejos de Salmar son asunto de Salmar. En cuanto a Crowe, la palabra de un escribiente no ahorca a un hombre con tanta plata."),
      ("He'll trip over his own ledgers one day.", "Algún día tropezará con sus propios libros.")),
  log(("The musket charge is dropped. Crowe walks free, for now.", "Se retira el cargo de los mosquetes. Crowe sigue libre, por ahora."))]),
 chapter("purse", ("The Gilded Purse", "La Bolsa Dorada"), 10, {"p9": "other,new"}, [
  say("crowe", ("You've cost me a clerk, a die and a captain, Miss Calder. I've hired a galleon to collect what I'm owed. She's called the Gilded Purse. I thought you'd appreciate the joke.",
                "Me ha costado un escribiente, un troquel y una capitana, señorita Calder. He contratado un galeón para cobrar lo que se me debe. Se llama la Bolsa Dorada. Pensé que apreciaría la broma."),
      ("I'll appreciate sinking it.", "Apreciaré hundirla.")),
  goal("networth", ("Fit out for a galleon fight: reach a net worth of 200,000.", "Equípate para luchar contra un galeón: alcanza un patrimonio de 200.000."), amount=200000),
  goal("npccombat", ("Sink the Gilded Purse off {p9}.", "Hunde la Bolsa Dorada frente a {p9}."), enemy="gilded_purse", port="{p9}"),
  log(("The Gilded Purse is on the bottom. Crowe has run out of people to send.", "La Bolsa Dorada está en el fondo. A Crowe se le ha acabado la gente que mandar."))]),
 chapter("clean_hands", ("Clean Hands", "Manos limpias"), 10, {}, [
  goal("talk", ("Go home to Varga at the tavern in Blackwater Cay.", "Vuelve a casa, con Varga, en la taberna de Cayo Aguanegra."), npc="varga", port="blackwater_cay", building="tavern"),
  say("varga", ("You could have taken his money. Twice.", "Podrías haber aceptado su dinero. Dos veces."),
      ("I'd rather owe you.", "Prefiero deberte a ti.")),
  say("varga", ("Then work for me. Half shares, and you keep your own seals out of my crates.", "Entonces trabaja conmigo. A medias, y tus sellos lejos de mis cajas."),
      ("Partners, then.", "Socias, pues.")),
  reward(60000),
  log(("You and Nell Varga are partners.", "Nell Varga y tú sois socias.")),
  END]),
])
