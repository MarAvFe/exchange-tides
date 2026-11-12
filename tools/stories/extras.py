"""Side tasks woven into the stories: a short scene and an objective, inserted after a chapter's opening
dialogue. Keyed by story id, then chapter id. Applied by build.py."""
from sk import *

EXTRAS = {
 # ---------------------------------------------------------------- The Grimmer Debt (Vega)
 "grimmer_debt": {
  "letters": [goal("networth", ("Find your feet as a trader: reach a net worth of 4,000.", "Hazte con el oficio: alcanza un patrimonio de 4.000."), amount=4000)],
  "lost_ships": [
   say("sailor", ("The Swallow's bosun drinks here. He says Grimmer's ships always come out of the south on a falling tide. Test it, and you'll know he's not lying.",
                  "El contramaestre de la Golondrina bebe aquí. Dice que los barcos de Grimmer siempre salen por el sur con la marea bajando. Compruébalo y sabrás que no miente."),
       ("I'll test it.", "Lo comprobaré.")),
   goal("combat", ("Win a fight against Grimmer's raiders.", "Gana un combate contra los corsarios de Grimmer."), wins=1)],
  "warehouse": [goal("contracts", ("The creditors want proof you can earn: complete a governor contract.", "Los acreedores quieren pruebas de que sabes ganar dinero: cumple un contrato de gobernador."), n=1)],
  "grimmer_letter": [
   say("merchant", ("Half the merchants in this port got the same letter, Captain. Most of them signed.", "La mitad de los mercaderes de este puerto recibieron la misma carta, capitana. La mayoría firmó."),
       ("Then I'll buy what they're too scared to carry.", "Entonces compraré lo que les da miedo transportar.")),
   goal("have_good", ("Carry what frightened merchants won't: load 10 Muskets.", "Lleva lo que los mercaderes asustados no se atreven: carga 10 de Mosquetes."), good="arms", amount=10)],
  "provender": [goal("sink", ("The Provender's escorts are on the routes. Sink 2 of them first.", "Los escoltas del Avituallador vigilan las rutas. Hunde 2 primero."), n=2)],
  "allies": [goal("networth", ("Pay three crews: reach a net worth of 160,000.", "Paga a tres tripulaciones: alcanza un patrimonio de 160.000."), amount=160000)],
  "battery": [
   say("varga", ("And bring me a cargo of sugar. Gunners work better with rum in them, whatever the Admiralty says.", "Y tráeme un cargamento de azúcar. Los artilleros trabajan mejor con ron dentro, diga lo que diga el Almirantazgo."),
       ("Sugar and muskets. Some battle plan.", "Azúcar y mosquetes. Vaya plan de batalla.")),
   goal("deliver", ("Bring 20 Cane Sugar to Blackwater Cay for the battery's rum.", "Lleva 20 de Azúcar de caña a Cayo Aguanegra para el ron de la batería."), good="sugar", amount=20, port="blackwater_cay"),
   take("sugar", 20)],
  "aftermath": [goal("contracts", ("Governors want order back on the routes: complete 2 contracts.", "Los gobernadores quieren orden en las rutas: cumple 2 contratos."), n=2)],
  "mother_ledger": [
   say("banker", ("Your mother kept the best books in the Reach, Captain. Keep yours half as well and we'll talk again.", "Su madre llevaba los mejores libros del Estrecho, capitana. Lleve los suyos la mitad de bien y volveremos a hablar."),
       ("I have her ledger.", "Tengo su libro.")),
   goal("deposit", ("Open an account in your own name: keep 3,000 in a bank.", "Abre una cuenta a tu nombre: ten 3.000 en un banco."), amount=3000)],
  "moreno_tip": [goal("sink", ("Grimmer's scouts follow Moreno everywhere. Sink 2 of them.", "Los exploradores de Grimmer siguen a Moreno a todas partes. Hunde 2."), n=2)],
 },
 # ---------------------------------------------------------------- Bad Powder (Wren)
 "bad_powder": {
  "widow": [goal("networth", ("Reach a net worth of 9,000 so you can help the families.", "Alcanza un patrimonio de 9.000 para poder ayudar a las familias."), amount=9000)],
  "the_copy": [
   say("quill", ("And don't come back here for a while. The watchman talks in his sleep as well.", "Y no vuelva por aquí en una temporada. El vigilante también habla en sueños."),
       ("I'll keep away.", "Me mantendré lejos."), ("Hester Quill, mill clerk", "Hester Quill, escribiente del molino")),
   goal("networth", ("Reach a net worth of 16,000.", "Alcanza un patrimonio de 16.000."), amount=16000)],
  "warning": [goal("contracts", ("A man with governors' work is harder to sink quietly. Complete a governor contract.", "A un hombre con encargos de gobernadores cuesta más hundirlo en silencio. Cumple un contrato de gobernador."), n=1)],
  "raider_powder": [goal("networth", ("Reach a net worth of 55,000.", "Alcanza un patrimonio de 55.000."), amount=55000)],
  "decoy": [
   say("kip", ("Whoever warned them knew our course a week ago, sir. We should change how we send letters.", "Quien les avisó conocía nuestro rumbo desde hace una semana, señor. Deberíamos cambiar cómo mandamos las cartas."),
       ("From now on, nothing on paper.", "A partir de ahora, nada por escrito.")),
   goal("combat", ("The Tallow's friends are out. Win a fight.", "Los amigos del Sebo han salido. Gana un combate."), wins=1)],
  "hammerhead": [goal("sink", ("The Hammerhead's escorts scatter. Sink 2 of them so none can warn Grimmer.", "Los escoltas del Martillo se dispersan. Hunde 2 para que ninguno avise a Grimmer."), n=2)],
  "thorne": [
   say("kip", ("He offered pensions, sir. The families could use them.", "Ofreció pensiones, señor. A las familias les vendrían bien."),
       ("They could. They'll get them from someone who isn't buying silence.", "Les vendrían bien. Las tendrán de alguien que no compre silencio.")),
   goal("deposit", ("Start your own fund for the families: keep 40,000 in a bank.", "Empieza tu propio fondo para las familias: ten 40.000 en un banco."), amount=40000)],
  "dorn": [goal("sink", ("Grimmer's men are looking for Dorn too. Sink 2 of them.", "Los hombres de Grimmer también buscan a Dorn. Hunde 2."), n=2)],
  "witnesses": [goal("fleet", ("Witnesses need safe berths. Keep two ships.", "Los testigos necesitan literas seguras. Mantén dos barcos."), n=2)],
  "board": [goal("contracts", ("Show the board you're a trusted trader: complete 2 contracts.", "Demuestra al tribunal que eres un comerciante de confianza: cumple 2 contratos."), n=2)],
 },
 # ---------------------------------------------------------------- The Second Seal (Calder)
 "second_seal": {
  "wanted": [goal("networth", ("Keep trading while you pay: reach a net worth of 4,000.", "Sigue comerciando mientras pagas: alcanza un patrimonio de 4.000."), amount=4000)],
  "steel": [goal("networth", ("Reach a net worth of 12,000.", "Alcanza un patrimonio de 12.000."), amount=12000)],
  "second_seal": [goal("sink", ("Lisle's lookouts are watching the routes. Sink 2 so he doesn't hear you coming.", "Los vigías de Lisle vigilan las rutas. Hunde 2 para que no te oiga llegar."), n=2)],
  "whelp": [
   say("varga", ("Brack never fights where she can't run. Bring three hulls or bring none.", "Brack nunca pelea donde no pueda huir. Lleva tres cascos o ninguno."),
       ("Two will have to do.", "Con dos tendrá que bastar.")),
   goal("networth", ("Refit for a brig fight: reach a net worth of 110,000.", "Prepárate para luchar contra un bergantín: alcanza un patrimonio de 110.000."), amount=110000)],
  "court": [goal("contracts", ("The governor wants to see you're settled: complete a contract.", "El gobernador quiere ver que te has asentado: cumple un contrato."), n=1)],
  "clean_hands": [goal("deposit", ("Put up your half of the partnership: keep 120,000 in a bank.", "Pon tu mitad de la sociedad: ten 120.000 en un banco."), amount=120000)],
  "notice": [
   say("barkeep", ("The Reeve likes you, Ash, and she hates Saltmere. Bring her a cargo of cocoa and she'll like you more.", "La alcaldesa te aprecia, Ceniza, y odia a Salmar. Llévale un cargamento de cacao y te apreciará más."),
       ("Bribery by cocoa. My favourite kind.", "Soborno con cacao. Mi favorito.")),
   goal("deliver", ("Bring 15 Cocoa Beans to Driftmoor.", "Lleva 15 de Granos de cacao a Brumaria."), good="cocoa", amount=15, port="driftmoor"),
   take("cocoa", 15)],
  "silver": [goal("networth", ("Reach a net worth of 45,000.", "Alcanza un patrimonio de 45.000."), amount=45000)],
  "lisle_price": [goal("sink", ("Crowe's men are hunting Lisle. Sink 2 before they reach Blackwater.", "Los hombres de Crowe buscan a Lisle. Hunde 2 antes de que lleguen a Aguanegra."), n=2)],
  "allies": [goal("contracts", ("Keep the governors close: complete 2 contracts.", "Mantén cerca a los gobernadores: cumple 2 contratos."), n=2)],
 },
 # ---------------------------------------------------------------- Turncoat (Moreno)
 "turncoat": {
  "running": [goal("networth", ("Sell what's in the hold: reach a net worth of 4,000.", "Vende lo que hay en la bodega: alcanza un patrimonio de 4.000."), amount=4000)],
  "quiet": [goal("networth", ("Rebuild your purse after the debt: reach a net worth of 14,000.", "Recompón tu bolsa tras la deuda: alcanza un patrimonio de 14.000."), amount=14000)],
  "cover": [goal("combat", ("A cotton trader still has to fight raiders. Win a fight.", "Un tratante de algodón también tiene que pelear con corsarios. Gana un combate."), wins=1)],
  "lark_ghost": [
   say("brandt", ("She didn't call the bailiffs, captain. That's something.", "No llamó a los alguaciles, capitán. Algo es algo."),
       ("It's a start.", "Es un comienzo.")),
   goal("networth", ("Reach a net worth of 18,000.", "Alcanza un patrimonio de 18.000."), amount=18000)],
  "heir": [goal("deliver", ("Show Vega what you can carry: bring 20 Cane Sugar to Puerto Ambar.", "Demuéstrale a Vega lo que puedes transportar: lleva 20 de Azúcar de caña a Puerto Ambar."), good="sugar", amount=20, port="puerto_ambar"),
           take("sugar", 20)],
  "hale": [goal("networth", ("Reach a net worth of 35,000.", "Alcanza un patrimonio de 35.000."), amount=35000)],
  "wolves": [goal("networth", ("Reach a net worth of 55,000.", "Alcanza un patrimonio de 55.000."), amount=55000)],
  "jackal": [
   say("brandt", ("While you were gone, captain, I counted their guns. Eight on the sloop, and Brack's frigate has twenty.", "Mientras no estabas, capitán, les conté los cañones. Ocho en la balandra, y la fragata de Brack tiene veinte."),
       ("Then we'll need more than luck.", "Entonces necesitaremos algo más que suerte.")),
   goal("contracts", ("Governors' work buys you friends in port: complete a contract.", "El trabajo de los gobernadores te compra amigos en puerto: cumple un contrato."), n=1)],
  "chart_maker": [goal("networth", ("Reach a net worth of 130,000.", "Alcanza un patrimonio de 130.000."), amount=130000)],
  "pardon": [goal("contracts", ("A pardoned man needs honest work: complete 2 contracts.", "Un hombre indultado necesita trabajo honrado: cumple 2 contratos."), n=2)],
  "witness": [goal("sink", ("Grimmer's men are watching Pia's town. Sink 2 of them.", "Los hombres de Grimmer vigilan el pueblo de Pia. Hunde 2."), n=2)],
  "vega_again": [goal("networth", ("Reach a net worth of 160,000.", "Alcanza un patrimonio de 160.000."), amount=160000)],
 },
 # ---------------------------------------------------------------- The Compact (Quill)
 "compact": {
  "clerk": [
   say("merchant", ("Saltmere has always been a fishing town, miss. Fish sells everywhere, even under a Compact.", "Salmar siempre ha sido un pueblo pesquero, señorita. El pescado se vende en todas partes, incluso bajo un Pacto."),
       ("Then I'll start with fish.", "Entonces empezaré con pescado.")),
   goal("have_good", ("Load 20 Salt Fish to start your trade.", "Carga 20 de Pescado salado para empezar tu negocio."), good="fish", amount=20)],
  "stranded": [goal("networth", ("Reach a net worth of 12,000.", "Alcanza un patrimonio de 12.000."), amount=12000)],
  "casks": [goal("networth", ("Reach a net worth of 18,000.", "Alcanza un patrimonio de 18.000."), amount=18000)],
  "thorne_letter": [goal("combat", ("Thorne's answer comes with guns. Win a fight against his hired raiders.", "La respuesta de Thorne llega con cañones. Gana un combate contra sus corsarios a sueldo."), wins=1)],
  "vann_price": [goal("networth", ("Vann measures people in silver. Reach a net worth of 70,000.", "Vann mide a la gente en plata. Alcanza un patrimonio de 70.000."), amount=70000)],
  "contract": [goal("networth", ("Fit out for a barque fight: reach a net worth of 80,000.", "Prepárate para luchar contra una bricbarca: alcanza un patrimonio de 80.000."), amount=80000)],
  "vann_breaks": [
   say("wren", ("You're trusting Vann? She sold you water at three prices for eleven years.", "¿Te fías de Vann? Te vendió agua a tres precios durante once años."),
       ("I'm trusting her arithmetic.", "Me fío de su aritmética."), ("Tobias Wren", "Tobias Wren")),
   goal("contracts", ("Keep the governors listening: complete 2 contracts.", "Mantén a los gobernadores escuchando: cumple 2 contratos."), n=2)],
  "guild": [goal("fleet", ("The guild needs ships to carry its copies. Own four ships.", "El gremio necesita barcos para llevar sus copias. Ten cuatro barcos."), n=4)],
  "first_sale": [goal("deliver", ("Your shipwright wants payment in water and fish. Bring 15 Salt Fish to {p3}.", "Tu carpintera de ribera quiere cobrar en agua y pescado. Lleva 15 de Pescado salado a {p3}."), good="fish", amount=15, port="{p3}"),
                 take("fish", 15)],
  "mate": [goal("networth", ("Reach a net worth of 95,000.", "Alcanza un patrimonio de 95.000."), amount=95000)],
  "invoice": [goal("networth", ("Reach a net worth of 320,000.", "Alcanza un patrimonio de 320.000."), amount=320000)],
 },
 # ---------------------------------------------------------------- The False Light (Bale)
 "false_light": {
  "clear": [
   say("governor", ("And Bale? Bring cotton next time you come. The widows sew sails for a living, and they've no cloth.", "¿Y Bale? Traiga algodón la próxima vez. Las viudas cosen velas para vivir, y no tienen tela."),
       ("They'll have it.", "La tendrán.")),
   goal("deliver", ("Bring 20 Cotton Bales to Coralhaven for the sailmakers.", "Lleva 20 de Fardos de algodón a Puertocoral para las veleras."), good="cotton", amount=20, port="coralhaven"),
   take("cotton", 20)],
  "swimmer": [goal("networth", ("Reach a net worth of 10,000.", "Alcanza un patrimonio de 10.000."), amount=10000)],
  "chart": [goal("combat", ("Kell's boats know you're asking. Win a fight against them.", "Los botes de Kell saben que andas preguntando. Gana un combate contra ellos."), wins=1)],
  "wick": [goal("networth", ("Reach a net worth of 75,000.", "Alcanza un patrimonio de 75.000."), amount=75000)],
  "commander": [goal("contracts", ("Hale wants to see you work for governors first: complete a contract.", "Hale quiere verte trabajar antes para los gobernadores: cumple un contrato."), n=1)],
  "lamp_room": [goal("networth", ("Reach a net worth of 180,000.", "Alcanza un patrimonio de 180.000."), amount=180000)],
  "lit": [goal("fleet", ("Lanterna will need ships to bring the keeper's oil. Own four ships.", "Linterna necesitará barcos para llevar el aceite del farero. Ten cuatro barcos."), n=4)],
  "salvage": [goal("combat", ("Win a fight against the wreckers' boats.", "Gana un combate contra los botes de los raqueros."), wins=1)],
  "house_vega": [goal("contracts", ("House Vega trades with governors. Complete a contract to show you can too.", "La Casa Vega comercia con gobernadores. Cumple un contrato para demostrar que tú también."), n=1)],
  "harrow": [
   say("ezra", ("Harrow smiled the whole time, didn't he? Men like that smile while they count.", "Harrow sonrió todo el rato, ¿verdad? Los hombres así sonríen mientras cuentan."),
       ("He did. I counted too.", "Sonrió. Yo también conté.")),
   goal("sink", ("Harrow's money hires raiders. Sink 2 of them.", "El dinero de Harrow contrata corsarios. Hunde 2."), n=2)],
 },
}

def apply(stories):
    for st in stories:
        ex = EXTRAS.get(st["id"], {})
        for ch in st["chapters"]:
            add = ex.get(ch["id"])
            if not add: continue
            steps = ch["steps"]
            at = 1 if steps and steps[0]["do"] == "say" else 0     # after the opening dialogue
            ch["steps"] = steps[:at] + add + steps[at:]
