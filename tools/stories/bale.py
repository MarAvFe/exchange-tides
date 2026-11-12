"""The False Light - Okoro Bale, 1708. Acts: Clear Weather (1-7), House Vega (8-14), The False Light (15-21)."""
from sk import *

npc("ezra", ("Ezra Mott, of the Morning Star", "Ezra Mott, del Lucero del Alba"), "crew", False, 17081, "portrait_sailor")
npc("harrow", ("Edmund Harrow, of Harrow & Sons", "Edmund Harrow, de Harrow e Hijos"), "merchant", False, 17082, "portrait_merchant")
npc("hollis", ("Hollis Kell", "Hollis Kell"), "crew", False, 17083, "portrait_sailor")
npc("kell", ("Cassius Kell", "Cassius Kell"), "crew", False, 1708, "portrait_smuggler")

enemy("lamp_sloop", ("The Wick", "La Mecha"), 110, 8, 0.9, 66, 14000, "ship_sloop_pirate", 7)
enemy("false_light", ("The False Light", "La luz falsa"), 330, 22, 0.8, 74, 60000, "ship_galleon_pirate", 12)

item("old_chart", ("Lanterna Chart, 1688", "Carta de Linterna, 1688"),
     ("The coast as it was the year the Morning Star went down, with the light's arc drawn in red.", "La costa tal como era el año en que se hundió el Lucero del Alba, con el arco del faro dibujado en rojo."), "sailing_storm_frequency(-10%)")
item("red_lantern", ("Red Lantern", "Farol rojo"),
     ("Red glass and a hood to aim the beam. Kell's boats carried them. You read the coast better for having it.", "Cristal rojo y una capucha para dirigir el haz. Los botes de Kell los llevaban. Con él lees mejor la costa."), "sailing_storm_frequency(-15%)")
item("hollis_confession", ("Hollis Kell's Confession", "La confesión de Hollis Kell"),
     ("An old lamp-keeper's account of the night he let the light go out, and who paid him.", "El relato de un viejo farero sobre la noche en que dejó apagarse el faro, y quién le pagó."))

HALE = ("Commander Ada Hale", "Comandante Ada Hale")
VEGA = ("Marisol Vega, House Vega", "Marisol Vega, Casa Vega")

STORY = campaign("false_light", ("The False Light", "La luz falsa"), 1708,
 ("1708. Twenty years ago Okoro Bale was a young navigator on the Morning Star when she struck the rocks below Lanterna on a clear, calm night. The lighthouse was dark. Eleven men drowned, and Bale swore he would never see that harbour again. Now ships are going down on clear nights all over the Reach.",
  "1708. Hace veinte años, Okoro Bale era un joven navegante del Lucero del Alba cuando el barco chocó contra las rocas de Linterna en una noche clara y en calma. El faro estaba apagado. Se ahogaron once hombres, y Bale juró que no volvería a ver aquel puerto. Ahora se hunden barcos en noches despejadas por todo el Estrecho."),
 ("The Light Is Lit", "El faro encendido"),
 ("Lanterna lit its lamp under a new keeper and read out the names of the Morning Star's eleven. You weren't there, and you didn't need to be. Headlands went dark at night the way they should, and ships stopped steering for lights where no lighthouse stood.",
  "Linterna encendió su lámpara con un farero nuevo y leyó en voz alta los nombres de los once del Lucero del Alba. Tú no estabas, y no hacía falta. Los cabos volvieron a quedar a oscuras de noche, como debe ser, y los barcos dejaron de poner rumbo a luces donde no había ningún faro."),
[
 # ---------------- Act I: Clear Weather
 chapter("clear", ("Clear Weather", "Tiempo despejado"), 0, {}, [
  say("governor", ("Another ship lost on a calm night, Bale. The third this season. You read weather better than anyone in the Reach. Tell me it was weather.",
                   "Otro barco perdido en una noche tranquila, Bale. El tercero esta temporada. Usted lee el tiempo mejor que nadie en el Estrecho. Dígame que fue el tiempo."),
      ("It wasn't weather.", "No fue el tiempo.")),
  goal("networth", ("Get your trade moving so you can afford to look into it: reach a net worth of 6,000.", "Pon en marcha tu negocio para poder permitirte investigar: alcanza un patrimonio de 6.000."), amount=6000)]),
 chapter("swimmer", ("The Swimmer", "El nadador"), 0, {"p1": "other,new,has:tavern"}, [
  goal("talk", ("Talk to the families of the lost crews in {p1}.", "Habla con las familias de las tripulaciones perdidas en {p1}."), npc="barkeep", port="{p1}", building="tavern"),
  say("barkeep", ("My sister's boy was on the last one. He swam ashore. He says they steered for a light on the point, steady as a lighthouse. There's no lighthouse on that point.",
                  "El hijo de mi hermana iba en el último. Llegó a nado a la orilla. Dice que pusieron rumbo a una luz en la punta, fija como un faro. En esa punta no hay ningún faro."),
      ("Someone put one there.", "Alguien la puso ahí.")),
  unlock("spice")]),
 chapter("watch", ("Watch Boats", "Botes de vigilancia"), 1, {}, [
  goal("cash", ("Hire boats to watch the coast at night: raise 10,000 in cash.", "Contrata botes para vigilar la costa de noche: reúne 10.000 en efectivo."), amount=10000),
  log(("Your watch boats saw a red lantern on a bare headland, and a sloop carrying it away before dawn.", "Tus botes de vigilancia vieron un farol rojo en un cabo pelado, y una balandra que se lo llevaba antes del alba.")),
  goal("networth", ("Keep the watch boats paid: reach a net worth of 14,000.", "Mantén pagados los botes de vigilancia: alcanza un patrimonio de 14.000."), amount=14000)]),
 chapter("chart", ("Reading the Wrecks", "Leer los naufragios"), 1, {"p2": "other,new,has:curio"}, [
  say("governor", ("You've been drawing on my maps, Bale. Every wreck marked in red.", "Ha estado dibujando en mis mapas, Bale. Cada naufragio marcado en rojo."),
      ("All on clear nights. All below a headland. All where a lighthouse would be, if you didn't know the coast.", "Todos en noches despejadas. Todos bajo un cabo. Todos donde habría un faro, si no conocieras la costa.")),
  say("governor", ("The curio dealer in {p2} sells old charts. If anyone has the coast as it used to be, it's that magpie.",
                   "El anticuario de {p2} vende cartas antiguas. Si alguien tiene la costa tal como era, es esa urraca."),
      ("Then I'll go and see the magpie.", "Entonces iré a ver a la urraca.")),
  goal("deliver", ("The dealer in {p2} trades charts for spice. Bring 10 Spice Chests.", "El anticuario de {p2} cambia cartas por especias. Lleva 10 de Cofres de especias."), good="spice", amount=10, port="{p2}"),
  take("spice", 10),
  get("old_chart"),
  say("curio", ("Lanterna, 1688. The light's arc in red ink. That's the year the Morning Star went down, isn't it? You've gone grey, navigator.",
                "Linterna, 1688. El arco del faro en tinta roja. Es el año en que se hundió el Lucero del Alba, ¿verdad? Se le ha puesto el pelo gris, navegante."),
      ("Twenty years will do that.", "Veinte años lo hacen.")),
  ]),
 chapter("morning_star", ("The Morning Star", "El Lucero del Alba"), 2, {"p3": "other,new,has:tavern"}, [
  say("barkeep", ("There's an old sailor in {p3} who says he was on the Morning Star. Ezra Mott. Nobody believes him, he says so many things.",
                  "Hay un viejo marinero en {p3} que dice que iba en el Lucero del Alba. Ezra Mott. Nadie le cree, dice tantas cosas."),
      ("I'll believe him. I was there.", "Yo le creeré. Yo estaba allí.")),
  goal("talk", ("Find Ezra Mott at the tavern in {p3}.", "Busca a Ezra Mott en la taberna de {p3}."), npc="ezra", port="{p3}", building="tavern"),
  say("ezra", ("Okoro Bale. The navigator boy. You were the only one sober enough to swim. ... The lamp went out at two bells, steady as you like. No storm. Somebody turned it down.",
               "Okoro Bale. El chico navegante. Eras el único lo bastante sobrio para nadar. ... La lámpara se apagó a las dos campanadas, sin más. Sin tormenta. Alguien la bajó."),
      ("The keeper was Hollis Kell.", "El farero era Hollis Kell.")),
  say("ezra", ("And Hollis Kell left Lanterna a year later with a new coat and a full purse. I always wondered where a lamp-keeper finds a purse like that.",
               "Y Hollis Kell se fue de Linterna un año después con casaca nueva y la bolsa llena. Siempre me pregunté dónde encuentra un farero una bolsa así."),
      ("So have I.", "Yo también.")),
  goal("combat", ("Wreckers' boats are watching your ship. Win a fight against them.", "Los botes de los raqueros vigilan tu barco. Gana un combate contra ellos."), wins=1),
  unlock("arms")]),
 chapter("salvage", ("Salvage", "Restos del naufragio"), 2, {"p4": "other,new,has:market"}, [
  goal("talk", ("Find out where the wrecked cargo is being sold. Ask the merchants of {p4}.", "Averigua dónde se vende la carga de los naufragios. Pregunta a los mercaderes de {p4}."), npc="merchant", port="{p4}", building="market"),
  say("merchant", ("Wreck goods? Crates with the brands scraped off, going cheap. A man called Cassius Kell sells them. His father kept the Lanterna light, years back.",
                   "¿Mercancía de naufragios? Cajas con las marcas raspadas, baratas. Las vende un tal Cassius Kell. Su padre cuidaba el faro de Linterna, hace años."),
      ("I know the name.", "Conozco ese nombre.")),
  log(("Cassius Kell's father kept the Lanterna light the night the Morning Star went down.", "El padre de Cassius Kell cuidaba el faro de Linterna la noche que se hundió el Lucero del Alba.")),
  goal("networth", ("Reach a net worth of 24,000.", "Alcanza un patrimonio de 24.000."), amount=24000)]),
 chapter("kell_boats", ("Kell's Boats", "Los botes de Kell"), 3, {}, [
  goal("sink", ("Kell's salvage boats work the wrecks after dark. Sink 2 of them.", "Los botes de Kell saquean los naufragios de noche. Hunde 2."), n=2),
  get("red_lantern"),
  say("ezra", ("Red glass and a hood. You could see that from five miles out and swear it was a harbour. That's how they did it.",
               "Cristal rojo y una capucha. Se ve a cinco millas y jurarías que es un puerto. Así lo hacían."),
      ("That's how they're doing it again.", "Así lo vuelven a hacer.")),
  goal("networth", ("Reach a net worth of 32,000.", "Alcanza un patrimonio de 32.000."), amount=32000)]),
 # ---------------- Act II: House Vega
 chapter("house_vega", ("House Vega", "La Casa Vega"), 3, {}, [
  goal("talk", ("House Vega lost a ship on a clear night last month. Call on Marisol Vega in Puerto Ambar.", "La Casa Vega perdió un barco en una noche despejada el mes pasado. Visita a Marisol Vega en Puerto Ambar."), npc="vega", port="puerto_ambar", building="market"),
  say("vega", ("Okoro Bale. My father would have hired you on the spot. We lost the Clever Gull on a clear night with a full hold. I'll pay for anything that stops this.",
               "Okoro Bale. Mi padre lo habría contratado en el acto. Perdimos la Gaviota Lista en una noche clara con la bodega llena. Pagaré lo que haga falta para pararlo."),
      ("I need an Admiralty officer who'll listen.", "Necesito un oficial del Almirantazgo que escuche."), VEGA),
  say("vega", ("Commander Hale owes me a favour from the Grimmer business. Put up 20,000 for the hunt, and House Vega will match it.", "La comandante Hale me debe un favor del asunto Grimmer. Ponga 20.000 para la cacería, y la Casa Vega pondrá otro tanto."),
      ("Done.", "Hecho."), VEGA),
  goal("deposit", ("Put 20,000 in a bank as your stake in the hunt.", "Deposita 20.000 en un banco como tu parte de la cacería."), amount=20000),
  reward(20000)]),
 chapter("insurance", ("Insured", "Asegurado"), 4, {"p5": "other,new,has:bank"}, [
  say("vega", ("Something else. The Clever Gull was insured with Harrow & Sons. They paid out in a week, without a single question. Insurers never pay in a week.",
               "Otra cosa. La Gaviota Lista estaba asegurada con Harrow e Hijos. Pagaron en una semana, sin una sola pregunta. Las aseguradoras nunca pagan en una semana."),
      ("Unless they already own the salvage.", "A menos que ya sean dueñas de los restos."), VEGA),
  goal("contracts", ("Bankers trust captains with a record. Complete 2 governor contracts.", "Los banqueros confían en capitanes con historial. Cumple 2 contratos de gobernador."), n=2),
  goal("talk", ("Ask the banker in {p5} about Harrow & Sons.", "Pregunta al banquero de {p5} por Harrow e Hijos."), npc="banker", port="{p5}", building="bank"),
  say("banker", ("Harrow insures the cargo, and a salvage company buys the wreck rights the week after. Same signature on both. The salvage company pays Cassius Kell. Draw your own picture, captain.",
                 "Harrow asegura la carga, y una compañía de rescates compra los derechos del naufragio a la semana siguiente. La misma firma en las dos cosas. La compañía de rescates paga a Cassius Kell. Saque usted el dibujo, capitán."),
      ("They're paid when it sinks, and paid again when it's salvaged.", "Cobran cuando se hunde, y vuelven a cobrar cuando se rescata."))]),
 chapter("two_headlands", ("Two Headlands", "Dos cabos"), 4, {}, [
  say("ezra", ("Kell works two headlands, never the same one twice running. One ship can watch one. You need two.", "Kell trabaja dos cabos, nunca el mismo dos veces seguidas. Un barco vigila uno. Te hacen falta dos."),
      ("Then I'll buy another.", "Entonces compraré otro.")),
  goal("fleet", ("Buy a second ship to watch the second headland.", "Compra un segundo barco para vigilar el segundo cabo."), n=2),
  goal("networth", ("Keep both ships at sea: reach a net worth of 60,000.", "Mantén los dos barcos en el mar: alcanza un patrimonio de 60.000."), amount=60000)]),
 chapter("wick", ("The Wick", "La Mecha"), 5, {"p6": "other,new"}, [
  say("ezra", ("Lantern on the headland above {p6} last night, and a sloop below it. She'll be back tonight.", "Anoche hubo un farol en el cabo de {p6}, y una balandra debajo. Esta noche volverá."),
      ("So will we.", "Nosotros también.")),
  goal("npccombat", ("Catch the lantern sloop off {p6}.", "Atrapa a la balandra del farol frente a {p6}."), enemy="lamp_sloop", port="{p6}"),
  log(("The Wick's crew talked: Kell carries the big lamp on a galleon called the False Light, and he only comes out for rich cargo.", "La tripulación de la Mecha habló: Kell lleva la lámpara grande en un galeón llamado la Luz Falsa, y solo sale por cargamentos ricos.")),
  unlock("textiles")]),
 chapter("harrow", ("Harrow & Sons", "Harrow e Hijos"), 5, {"p7": "other,new,has:market"}, [
  goal("talk", ("Edmund Harrow keeps an office at the market in {p7}. Pay him a visit.", "Edmund Harrow tiene una oficina en el mercado de {p7}. Hazle una visita."), npc="harrow", port="{p7}", building="market"),
  say("harrow", ("Captain Bale. Wreckers, salvage, lanterns. What an imagination. We're a respectable house. Since you're interested in salvage, I can offer you a share in our next recovery. A generous one.",
                 "Capitán Bale. Raqueros, rescates, faroles. Qué imaginación. Somos una casa respetable. Ya que le interesan los rescates, puedo ofrecerle una parte de nuestra próxima recuperación. Generosa."),
      ("Your next recovery hasn't sunk yet.", "Su próxima recuperación todavía no se ha hundido.")),
  goal("networth", ("Harrow will try to outspend you. Reach a net worth of 90,000.", "Harrow intentará gastar más que tú. Alcanza un patrimonio de 90.000."), amount=90000)]),
 chapter("commander", ("The Commander", "La comandante"), 6, {"p8": "other,new,has:governor"}, [
  goal("talk", ("Commander Hale is stationed at {p8}. Bring her the red lantern.", "La comandante Hale está destinada en {p8}. Llévale el farol rojo."), npc="hale", port="{p8}", building="governor"),
  say("hale", ("Commander, for my sins. Vega wrote to me. If Kell is lighting false fires, I need him caught with the lamp lit, at sea, in front of witnesses. My ships are too well known. Yours isn't.",
               "Comandante, por mis pecados. Vega me escribió. Si Kell enciende fuegos falsos, necesito atraparlo con la lámpara encendida, en el mar, delante de testigos. Mis barcos son demasiado conocidos. El suyo no."),
      ("Then I'll be the bait.", "Entonces seré el cebo."), HALE),
  say("hale", ("Kell goes after sugar. Load a full cargo of it and sail the coast like a man who's never heard of wreckers.",
               "Kell va detrás del azúcar. Cargue una bodega entera y navegue la costa como alguien que nunca ha oído hablar de raqueros."),
      ("I've played the fool before.", "Ya me he hecho el tonto otras veces."), HALE),
  unlock("tobacco")]),
 chapter("bait", ("Bait", "El cebo"), 6, {}, [
  goal("have_good", ("Load 40 Cane Sugar as bait for Kell's wreckers.", "Carga 40 de Azúcar de caña como cebo para los raqueros de Kell."), good="sugar", amount=40),
  goal("sink", ("Kell's scouts take the bait. Sink 2 of them so the big ship has to come out.", "Los exploradores de Kell pican. Hunde 2 para que el barco grande tenga que salir."), n=2),
  log(("Kell's scouts are gone. Next time, he'll come himself.", "Los exploradores de Kell han caído. La próxima vez vendrá él mismo."))]),
 # ---------------- Act III: The False Light
 chapter("ezra_map", ("Ezra's Map", "El mapa de Ezra"), 7, {}, [
  say("ezra", ("I've sat in every tavern on this coast for twenty years, Okoro, listening. I know which headlands Kell hasn't used yet. There are three. Cover all three.",
               "Llevo veinte años sentado en todas las tabernas de esta costa, Okoro, escuchando. Sé qué cabos no ha usado Kell todavía. Son tres. Cúbrelos los tres."),
      ("Three headlands, three ships.", "Tres cabos, tres barcos.")),
  goal("fleet", ("Sail with three ships to cover Ezra's headlands.", "Navega con tres barcos para cubrir los cabos de Ezra."), n=3),
  goal("networth", ("Reach a net worth of 140,000.", "Alcanza un patrimonio de 140.000."), amount=140000)]),
 chapter("convoy", ("Kell Moves First", "Kell mueve primero"), 7, {}, [
  say("vega", ("Kell went for my convoy last night, Okoro. Not with a lantern. With guns. I think Harrow is frightened.",
               "Kell atacó anoche mi convoy, Okoro. No con un farol. Con cañones. Creo que Harrow tiene miedo."),
      ("Frightened men make noise. Noise is easy to follow.", "Los hombres asustados hacen ruido. El ruido es fácil de seguir."), VEGA),
  goal("combat", ("Kell's gunboats are hitting convoys. Win 2 fights against them.", "Las cañoneras de Kell atacan convoyes. Gana 2 combates contra ellas."), wins=2),
  goal("contracts", ("Escort governors' cargo through the danger: complete 2 contracts.", "Escolta la carga de los gobernadores a través del peligro: cumple 2 contratos."), n=2)]),
 chapter("nephew", ("The Swimmer's Word", "La palabra del nadador"), 8, {}, [
  say("hale", ("A lit lamp needs witnesses who saw one before. The boy who swam ashore in {p1}, will he speak?",
               "Una lámpara encendida necesita testigos que ya hayan visto otra. El chico que llegó a nado en {p1}, ¿hablará?"),
      ("I'll ask him.", "Se lo preguntaré."), HALE),
  goal("talk", ("Ask the barkeep's nephew in {p1} to stand witness.", "Pide al sobrino del tabernero de {p1} que sea testigo."), npc="barkeep", port="{p1}", building="tavern"),
  say("barkeep", ("He'll do it, if you see his mother right. She hasn't worked since the wreck. A cargo of cocoa to sell from her front room would keep her through the winter.",
                  "Lo hará, si se ocupa usted de su madre. No ha trabajado desde el naufragio. Un cargamento de cacao para vender en su sala le daría para pasar el invierno."),
      ("She'll have it.", "Lo tendrá.")),
  goal("deliver", ("Bring 25 Cocoa Beans to {p1} for the swimmer's mother.", "Lleva 25 de Granos de cacao a {p1} para la madre del nadador."), good="cocoa", amount=25, port="{p1}"),
  take("cocoa", 25),
  log(("The swimmer will stand witness before Commander Hale.", "El nadador será testigo ante la comandante Hale."))]),
 chapter("lamp_room", ("The Lamp Room", "La sala de la lámpara"), 8, {}, [
  say("curio", ("You asked about Hollis Kell once. He's alive, navigator. He sold me that chart. He lives in a room above my shop and pays his rent in old stories.",
                "Una vez preguntó por Hollis Kell. Está vivo, navegante. Él me vendió esa carta. Vive en un cuarto encima de mi tienda y paga el alquiler con historias viejas."),
      ("Then I'd like to hear one.", "Entonces me gustaría oír una.")),
  goal("talk", ("Find Hollis Kell above the curio shop in {p2}.", "Busca a Hollis Kell encima del anticuario de {p2}."), npc="hollis", port="{p2}", building="curio"),
  say("hollis", ("The Morning Star. I've waited twenty years for someone to ask me properly. A man from Harrow's paid me forty silver to turn the lamp down at two bells. I thought they'd lose a cargo. I didn't think eleven men would drown.",
                 "El Lucero del Alba. Llevo veinte años esperando a que alguien me lo preguntara como es debido. Un hombre de Harrow me pagó cuarenta de plata por bajar la lámpara a las dos campanadas. Pensé que perderían una carga. No pensé que se ahogarían once hombres."),
      ("I was one of the ones who didn't.", "Yo fui de los que no se ahogaron.")),
  say("hollis", ("Then write it down, navigator. I'll put my mark on it. My son learned the trade from me, and I'd like it to end with me.",
                 "Entonces escríbelo, navegante. Pondré mi marca. Mi hijo aprendió el oficio de mí, y quisiera que acabara conmigo."),
      ("It will.", "Acabará.")),
  get("hollis_confession"),
  unlock("wine")]),
 chapter("false_light", ("The False Light", "La luz falsa"), 9, {"p9": "other,new"}, [
  goal("networth", ("Kell's galleon is well armed. Build a net worth of 220,000 to fit out for the fight.", "El galeón de Kell va bien armado. Alcanza un patrimonio de 220.000 para equiparte para el combate."), amount=220000),
  goal("npccombat", ("Sail the coast off {p9} with your hold full of sugar. Kell will come.", "Navega la costa frente a {p9} con la bodega llena de azúcar. Kell vendrá."), enemy="false_light", port="{p9}"),
  say("kell", ("My father let the lamp go out the night your ship went down. Drunk, they said. He wasn't drunk. Harrow paid him, and he taught me the trade.",
               "Mi padre dejó apagarse la lámpara la noche que se hundió tu barco. Borracho, dijeron. No estaba borracho. Harrow le pagó, y él me enseñó el oficio."),
      ("Your father has said so in writing. It ends with you.", "Tu padre lo ha dicho por escrito. Se acaba contigo.")),
  log(("Cassius Kell is taken, with the lamp lit, in front of witnesses.", "Cassius Kell ha sido capturado con la lámpara encendida, delante de testigos."))]),
 chapter("harrow_falls", ("Harrow Falls", "La caída de Harrow"), 9, {"p10": "other,new,has:governor"}, [
  goal("networth", ("Harrow's lawyers are expensive. So are yours. Reach a net worth of 280,000.", "Los abogados de Harrow son caros. Los tuyos también. Alcanza un patrimonio de 280.000."), amount=280000),
  goal("talk", ("Bring Kell, Hollis's confession and Harrow's ledgers to Commander Hale at the governor's house in {p10}.", "Lleva a Kell, la confesión de Hollis y los libros de Harrow a la comandante Hale, en la casa de la gobernación de {p10}."), npc="hale", port="{p10}", building="governor"),
  say("hale", ("Kell's in irons, and Harrow & Sons is shut. The insurance money goes back to the families. I'll send word to Lanterna that the Morning Star's navigator found the men who put out the light. You needn't go back.",
               "Kell está encadenado, y Harrow e Hijos ha cerrado. El dinero del seguro vuelve a las familias. Mandaré aviso a Linterna de que el navegante del Lucero del Alba encontró a los hombres que apagaron el faro. No hace falta que vuelva."),
      ("I never needed to go back. I needed to know.", "Nunca necesité volver. Necesitaba saberlo."), HALE)]),
 chapter("lit", ("The Light Is Lit", "El faro encendido"), 10, {}, [
  say("ezra", ("Lanterna needs a new keeper, Okoro, and a keeper needs wages. The town can't pay them. It never could. That's how Harrow bought the last one.",
               "Linterna necesita un farero nuevo, Okoro, y un farero necesita sueldo. El pueblo no puede pagarlo. Nunca pudo. Así compró Harrow al anterior."),
      ("Then the keeper's wages will come from somewhere else.", "Entonces el sueldo del farero saldrá de otra parte.")),
  goal("deposit", ("Fund the Lanterna keeper's wages for twenty years: keep 100,000 in a bank.", "Paga el sueldo del farero de Linterna para veinte años: ten 100.000 en un banco."), amount=100000),
  say("ezra", ("They'll read the eleven names when they light it. Yours won't be among them. That's the point, isn't it?",
               "Leerán los once nombres cuando lo enciendan. El tuyo no estará entre ellos. De eso se trata, ¿no?"),
      ("That's the point.", "De eso se trata.")),
  reward(80000),
  log(("Word goes to Lanterna about the Morning Star, with twenty years of a keeper's wages.", "La noticia del Lucero del Alba llega a Linterna, con veinte años de sueldo para un farero.")),
  END]),
])
