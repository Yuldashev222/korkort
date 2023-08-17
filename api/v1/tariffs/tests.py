// Dropdawn
DATA
const
lanAndKom = {
    "Blekinge län": {
        ble_har: "Karlshamn",
        ble_rar: "Karlskrona",
        ble_olo: "Olofström",
        ble_ron: "Ronneby",
        ble_sol: "Sölvesborg",
    },
    "Dalarnas län": {
        dal_ave: "Avesta",
        dal_bor: "Borlänge",
        dal_fal: "Falun",
        dal_gag: "Gagnef",
        dal_hed: "Hedemora",
        dal_lek: "Leksand",
        dal_lud: "Ludvika",
        dal_mal: "Malung-Sälen",
        dal_mor: "Mora",
        dal_ors: "Orsa",
        dal_rat: "Rättvik",
        dal_sme: "Smedjebacken",
        dal_sat: "Säter",
        dal_van: "Vansbro",
        dal_alv: "Älvdalen",
    },
    "Gotlands län": {got_got: "Gotland"},
    "Gävleborgs län": {
        gav_bol: "Bollnäs",
        gav_gav: "Gävle",
        gav_hof: "Hofors",
        gav_hud: "Hudiksvall",
        gav_lju: "Ljusdal",
        gav_nor: "Nordanstig",
        gav_ock: "Ockelbo",
        gav_ova: "Ovanåker",
        gav_san: "Sandviken",
        gav_sod: "Söderhamn",
    },
    "Hallands län": {
        hal_fal: "Falkenberg",
        hal_hal: "Halmstad",
        hal_hyl: "Hylte",
        hal_kun: "Kungsbacka",
        hal_var: "Varberg",
        hal_lah: "Laholm",
    },

    "Jämtlands län": {
        jam_ber: "Berg",
        jam_bra: "Bräcke",
        jam_har: "Härjedalen",
        jam_kro: "Krokom",
        jam_rag: "Ragunda",
        jam_str: "Strömsund",
        jam_are: "Åre",
        jam_ost: "Östersund",
    },

    "Jönköpings län": {
        jon_ane: "Aneby",
        jon_eks: "Eksjö",
        jon_gis: "Gislaved",
        jon_gno: "Gnosjö",
        jon_hab: "Habo",
        jon_jon: "Jönköping",
        jon_mul: "Mullsjö",
        jon_nas: "Nässjö",
        jon_sav: "Sävsjö",
        jon_tra: "Tranås",
        jon_vag: "Vaggeryd",
        jon_vet: "Vetlanda",
        jon_var: "Värnamo",
    },
    "Kalmar län": {
        kal_bor: "Borgholm",
        kal_emm: "Emmaboda",
        kal_hul: "Hultsfred",
        kal_hog: "Högsby",
        kal_kal: "Kalmar",
        kal_mon: "Mönsterås",
        kal_mor: "Mörbylånga",
        kal_nyb: "Nybro",
        kal_osk: "Oskarshamn",
        kal_tor: "Torsås",
        kal_vim: "Vimmerby",
        kal_vas: "Västervik",
    },
    "Kronobergs län": {
        kro_alv: "Alvesta",
        kro_les: "Lessebo",
        kro_lju: "Ljungby",
        kro_mar: "Markaryd",
        kro_tin: "Tingsryd",
        kro_upp: "Uppvidinge",
        kro_vax: "Växjö",
        kro_alm: "Älmhult",
    },
    "Norrbottens län": {
        nor_arj: "Arjeplog",
        nor_arv: "Arvidsjaur",
        nor_bod: "Boden",
        nor_gal: "Gällivare",
        nor_hap: "Haparanda",
        nor_jok: "Jokkmokk",
        nor_kal: "Kalix",
        nor_kir: "Kiruna",
        nor_lul: "Luleå",
        nor_paj: "Pajala",
        nor_pit: "Piteå",
        nor_alv: "Älvsbyn",
        nor_kve: "Överkalix",
        nor_tve: "Övertorneå",
    },
    "Skåne län": {
        ska_bju: "Bjuv",
        ska_bro: "Bromölla",
        ska_bur: "Burlöv",
        ska_bas: "Båstad",
        ska_esl: "Eslöv",
        ska_hel: "Helsingborg",
        ska_has: "Hässleholm",
        ska_hog: "Höganäs",
        ska_hor: "Hörby",
        ska_hoo: "Höör",
        ska_kli: "Klippan",
        ska_kri: "Kristianstad",
        ska_kav: "Kävlinge",
        ska_lan: "Landskrona",
        ska_lom: "Lomma",
        ska_lun: "Lund",
        ska_mal: "Malmö",
        ska_osb: "Osby",
        ska_per: "Perstorp",
        ska_sim: "Simrishamn",
        ska_sjo: "Sjöbo",
        ska_sku: "Skurup",
        ska_sta: "Staffanstorp",
        ska_sva: "Svalöv",
        ska_sve: "Svedala",
        ska_tom: "Tomelilla",
        ska_tre: "Trelleborg",
        ska_vel: "Vellinge",
        ska_yst: "Ystad",
        ska_ast: "Åstorp",
        ska_ost: "Östra Göinge",
        ska_ang: "Ängelholm",
        ska_ork: "Örkelljunga",
    },
    "Stockholms län": {
        sto_bot: "Botkyrka",
        sto_dan: "Danderyd",
        sto_eke: "Ekerö",
        sto_han: "Haninge",
        sto_hud: "Huddinge",
        sto_jar: "Järfälla",
        sto_lid: "Lidingö",
        sto_nac: "Nacka",
        sto_nor: "Norrtälje",
        sto_nyk: "Nykvarn",
        sto_nyn: "Nynäshamn",
        sto_sal: "Salem",
        sto_sig: "Sigtuna",
        sto_sol: "Sollentuna",
        sto_son: "Solna",
        sto_sto: "Stockholm",
        sto_sun: "Sundbyberg",
        sto_sod: "Södertälje",
        sto_tyr: "Tyresö",
        sto_tab: "Täby",
        sto_upp: "Upplands Väsby",
        sto_upb: "Upplands-Bro",
        sto_val: "Vallentuna",
        sto_vax: "Vaxholm",
        sto_var: "Värmdö",
        sto_ost: "Österåker",
    },

    "Södermanlands län": {
        sod_esk: "Eskilstuna",
        sod_fle: "Flen",
        sod_gne: "Gnesta",
        sod_kat: "Katrineholm",
        sod_nyk: "Nyköping",
        sod_oxe: "Oxelösund",
        sod_str: "Strängnäs",
        sod_tro: "Trosa",
        sod_vin: "Vingåker",
    },
    "Uppsala län": {
        upp_enk: "Enköping",
        upp_heb: "Heby",
        upp_hab: "Håbo",
        upp_kni: "Knivsta",
        upp_tie: "Tierp",
        upp_upp: "Uppsala",
        upp_alv: "Älvkarleby",
        upp_ost: "Östhammar",
    },
    "Värmlands län": {
        var_arv: "Arvika",
        var_eda: "Eda",
        var_fil: "Filipstad",
        var_for: "Forshaga",
        var_gru: "Grums",
        var_hag: "Hagfors",
        var_ham: "Hammarö",
        var_kar: "Karlstad",
        var_kil: "Kil",
        var_kri: "Kristinehamn",
        var_mun: "Munkfors",
        var_sto: "Storfors",
        var_sun: "Sunne",
        var_saf: "Säffle",
        var_tor: "Torsby",
        var_arj: "Årjäng",
    },
    "Västerbottens län": {
        vab_bju: "Bjurholm",
        vab_dor: "Dorotea",
        vab_lyc: "Lycksele",
        vab_mal: "Malå",
        vab_nor: "Nordmaling",
        vab_nos: "Norsjö",
        vab_rob: "Robertsfors",
        vab_ske: "Skellefteå",
        vab_sor: "Sorsele",
        vab_sto: "Storuman",
        vab_ume: "Umeå",
        vab_vil: "Vilhelmina",
        vab_vin: "Vindeln",
        vab_van: "Vännäs",
        vab_ase: "Åsele",
    },
    "Västernorrlands län": {
        van_har: "Härnösand",
        van_kra: "Kramfors",
        van_sol: "Sollefteå",
        van_sun: "Sundsvall",
        van_tim: "Timrå",
        van_ang: "Ånge",
        van_orn: "Örnsköldsvik",
    },
    "Västmanlands län": {
        vam_arb: "Arboga",
        vam_fag: "Fagersta",
        vam_hal: "Hallstahammar",
        vam_kun: "Kungsör",
        vam_kop: "Köping",
        vam_nor: "Norberg",
        vam_sal: "Sala",
        vam_ski: "Skinnskatteberg",
        vam_sur: "Surahammar",
        vam_vas: "Västerås",
    },
    "Västra Götalands län": {
        vag_ale: "Ale",
        vag_ali: "Alingsås",
        vag_ben: "Bengtsfors",
        vag_bol: "Bollebygd",
        vag_bor: "Borås",
        vag_dal: "Dals-Ed",
        vag_ess: "Essunga",
        vag_fal: "Falköping",
        vag_far: "Färgelanda",
        vag_gra: "Grästorp",
        vag_gul: "Gullspång",
        vag_got: "Göteborg",
        vag_goe: "Götene",
        vag_her: "Herrljunga",
        vag_hjo: "Hjo",
        vag_har: "Härryda",
        vag_kar: "Karlsborg",
        vag_kun: "Kungälv",
        vag_ler: "Lerum",
        vag_lid: "Lidköping",
        vag_lil: "Lilla Edet",
        vag_lys: "Lysekil",
        vag_mar: "Mariestad",
        vag_mak: "Mark",
        vag_mel: "Mellerud",
        vag_mun: "Munkedal",
        vag_mol: "Mölndal",
        vag_oru: "Orust",
        vag_par: "Partille",
        vag_ska: "Skara",
        vag_sko: "Skövde",
        vag_sot: "Sotenäs",
        vag_ste: "Stenungsund",
        vag_str: "Strömstad",
        vag_sve: "Svenljunga",
        vag_tan: "Tanum",
        vag_tib: "Tibro",
        vag_tid: "Tidaholm",
        vag_tjo: "Tjörn",
        vag_tra: "Tranemo",
        vag_tro: "Trollhättan",
        vag_tor: "Töreboda",
        vag_udd: "Uddevalla",
        vag_ulr: "Ulricehamn",
        vag_var: "Vara",
        vag_vag: "Vårgårda",
        vag_van: "Vänersborg",
        vag_ama: "Åmål",
        vag_ock: "Öckerö",
    },
    "Örebro län": {
        ore_ask: "Askersund",
        ore_deg: "Degerfors",
        ore_hal: "Hallsberg",
        ore_hae: "Hällefors",
        ore_kar: "Karlskoga",
        ore_kum: "Kumla",
        ore_lax: "Laxå",
        ore_lek: "Lekeberg",
        ore_lin: "Lindesberg",
        ore_lju: "Ljusnarsberg",
        ore_nor: "Nora",
        ore_ore: "Örebro",

    },
    "Östergötlands län": {
        ost_box: "Boxholm",
        ost_fin: "Finspång",
        ost_kin: "Kinda",
        ost_lin: "Linköping",
        ost_mjo: "Mjölby",
        ost_mot: "Motala",
        ost_nor: "Norrköping",
        ost_sod: "Söderköping",
        ost_vad: "Vadstena",
        ost_val: "Valdemarsvik",
        ost_ydr: "Ydre",
        ost_atv: "Åtvidaberg",
        ost_ode: "Ödeshög",
    },
    "Hallands län": {
        hal_fal: "Falkenberg",
        hal_hal: "Halmstad",
        hal_hyl: "Hylte",
        hal_kun: "Kungsbacka",
        hal_var: "Varberg",
        hal_lah: "Laholm",
    },
};

const
filter = {
    nor: "Norrbottens län",
    ble: "Blekinge län",
    dal: "Dalarnas län",
    got: "Gotlands län",
    gav: "Gävleborgs län",
    jam: "Jämtlands län",
    jon: "Jönköpings län",
    kal: "Kalmar län",
    kro: "Kronobergs län",
    ska: "Skåne län",
    sto: "Stockholms län",
    sod: "Södermanlands län",
    upp: "Uppsala län",
    var: "Värmlands län",
    vab: "Västerbottens län",
    van: "Västernorrlands län",
    vam: "Västmanlands län",
    vag: "Västra Götalands län",
    ore: "Örebro län",
    ost: "Östergötlands län",
    hal: "Hallands län",
};

// let
apiURL = "https://backend.minalappar.se";
let
apiURL = "https://filer.offentligabeslut.se";
let
token =
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MjcxODkxLCJpYXQiOjE2NzgxODU0OTEsImp0aSI6IjhhOTU0ODM4MjNkZTQ5ZDU4MDVmYzI3ZWEyZjg1Y2E1IiwidXNlcl9pZCI6MX0.Y3Z4CpBgXZshI810FafFVyKZ5RvE43nI07xCZMw0rRI";

let
filesData = [];
let
allData = {};
let
dataRec = [];

const
pageSize = 10;
let
curPage = 1;

// Dropdawns
select
DOM
elements
const
select1 = document.getElementById("custom_select_1");
const
select2 = document.getElementById("custom_select_2");
const
select3 = document.getElementById("custom_select_3");
const
select4 = document.getElementById("custom_select_4");
const
select6 = document.getElementById("custom_select_6");
const
allDataBtn = document.getElementById("all_data");

// Search
From
select
DOM
elements
const
searchForm = document.getElementById("search-form");
const
searchInput = document.getElementById("search-input");
const
searchResults = document.getElementById("search-results");
const
allDataCount = document.getElementById("count");
const
res = document.getElementById("result");

// Pagination
From
select
DOM
elements
const
prevButton = document.querySelector("#prevButton");
const
nextButton = document.querySelector("#nextButton");
const
paginations = document.querySelectorAll("#pag");
const
pagin_div = document.getElementById("pagin_div");

// Query
Values
let
searchVal = "";
let
file_date__year = "";
let
inform__region = "";
let
inform__organ = "";
let
inform__country = "";
let
order_senaste = "";

let
loader = `
< div


class ="loading-holder d-flex align-items-center my-4 p-4 border shadow" >

< h1


class ="loading" > Läser in...< /h1 >

< div


class ="spinner-border ms-auto" role="status" aria-hidden="true" > < /div >

< / div > `;

let
select = `
< option
value = ""


class ="dropdawn" selected >


Välj
kommun
< / option >
`;

let
options2 = select;

function
fetchFile(url)
{
    console.log(url)
fetch(url
      // method: "GET",
// headers: {
            // Authorization: "Bearer " + token,
//},
)
.then((res) = > res.blob())
.then((file) = > {
    let
tempUrl = URL.createObjectURL(file);
let
aTag = document.createElement("a");
aTag.href = tempUrl;

aTag.download = url + ".pdf";
document.body.appendChild(aTag);
aTag.click();
aTag.remove();
console.log(aTag);
});
}

// Recommend
Words
async function
recommendData(param)
{
    dataRec = await getData(param);
}

// recommendData("/hints");

const
autocomplateMatch = (input) = > {
if (input === "")
{
return [];
}

let
reg = new
RegExp(input);
return dataRec.filter((termin) = > {
if (termin.match(reg))
{
return termin;
}
});
};

function
showResults(val)
{
    res.innerHTML = "";
let
list = "";
let
termins = autocomplateMatch(val.toLowerCase());
for (let i = 0; i < termins.length; i++)
{
    list = list + ` < li
onclick = "changeValue(this)" > ` + termins[i] + "</li>";
}
res.innerHTML = "<ul>" + list + "</ul>";
}

function
changeValue(e)
{
    document.getElementById("search-input").value = e.innerHTML;
renderCard(` / files /?search =${e.innerHTML}
`);
showResults(e.innerHTML);
res.innerHTML = "";
}

function
searchAndHighlight(searchTerm, text)
{

    let
html = text;
let
regex = new
RegExp(searchTerm, "g");
let
highlighted = html.replace(regex, ` < mark


class ="coler" > ${searchTerm} < /mark > `);
con1 = highlighted;
}

async function renderCard(params, page = 1) {
window.scrollTo({
top: 0,
left: 0

,
behavior: 'smooth' // för
en
mjukare
scrollning
});
let
limit = 5;
searchResults.innerHTML = loader;
allData = await getData(params);
filesData = allData.results;
allDataCount.innerHTML = allData.count;
if (!filesData)
{
nextButton.style.visibility = "hidden";
prevButton.style.display = "none";
limit = 0;
searchResults.innerHTML = "<h1>Om du ser den här varningen så beror det mest sannolikt på att du inte är ansluten till din organisations IP-adress. Anslut till din organisations IP-adress och försök igen.</h1>";
allDataCount.innerHTML = 0;
return
}

if (numPages() - page < limit) {
limit = numPages() - page;
nextButton.style.visibility = "hidden";
prevButton.style.display = "none";
} else {
nextButton.style.visibility = "visible";
prevButton.style.display = "block";
}
console.log(filesData)

if (page == 1)
{
prevButton.style.visibility = "hidden";
prevButton.style.display = "none";
} else {
prevButton.style.visibility = "visible";
prevButton.style.display = "block";
}




let
con = "";
// create
html
filesData?.forEach((result) = > {
    let
con1 = result.about_text
function
capitalizeAfterPeriod(text)
{
    let
newText = text.replace( / (^ | \.)\s * (\w) / g, function(match, p1, p2)
{
return p1 + " " + p2.toUpperCase();
});
return newText;
}

let
text = con1;
let
newText = capitalizeAfterPeriod(text);
con1 = newText
let
str = searchVal;
if (searchVal[0] == '"')
{
let
massiv = searchVal.split(" -")
str = massiv[0].substr(1, massiv[0].length - 2);

}

if (searchVal) {

let
html = result.about_text;
let
mas = str.trim().toLowerCase().split( /\s + / )
let
highlighted = "";
console.log(mas, "mas")

for (let index = 0; index < mas.length; index++) {
    let regex = new RegExp(mas[index], "g");
highlighted = html.replace(regex, ` < b


class ="coler" > ${mas[index]} < /b > `);
html = searchInput.value != = "" ? highlighted: html;
}

// let
regex = new
RegExp(str, "g");
// console.log(regex)
   // let
highlighted = html.replace(regex, ` < b


class ="coler" > ${str} < /b > `);
con1 = capitalizeAfterPeriod(html);;

// searchAndHighlight(str, result.about_text)
// let position = result.about_text.search(str);
// if (position != -1){

// let
position1 = str.length
// let
position2 = position + position1 - 1;
// let
a = result.about_text.substr(0, position)
// let
c = result.about_text.substr(position2 + 1)
// con1 = a + ` < b


class ="coler" > ${result.about_text.substr(position, position1)} < /b > ` + c;

//}

// let
posit = c.search(str);
// let
posit1 = str.length
         // let
posit2 = posit + posit1 - 1;
// let
aa = c.substr(0, posit)
     // let
c1 = c.substr(posit2 + 1)
     // con1 += aa + ` < b


class ="coler" > ${c.substr(posit, posit1)} < /b > `

// let
pos = c1.search(str);
// let
pos1 = str.length
// let
pos2 = pos + pos1 - 1;
// let
aaa = c1.substr(0, pos)
// let
c12 = c1.substr(pos2 + 1)
// con1 += aaa + ` < b


class ="coler" > ${c1.substr(pos, pos1)} < /b > ` + c12

}

const
content = `
          < div


class ="card" >

< div


class ="card-header" >

< img


class ="logo"


src = "${result.logo}"
/ >
< div


class ="info-holder" >

< div


class ="title-holder" >

< h1


class ="title" > < span class ="capitalize" > ${result.country} < /span > | < span class ="capitalize" > ${result.region} < /span > | < span class ="capitalize" > ${result.organ} < /span > | < span class ="capitalize" > ${result.file_date} < /span > < /h1 >

< / div >
< div


class ="tag-holder" >

< div


class ="tag-box viloyat" >

< img


class ="tag-image shahar"


src = "https://offentligabeslut.se/wp-content/uploads/2023/02/state-1.png"
/ >
< p


class ="tag-text" > ${result.country} < /p >

< / div >
< div


class ="tag-box organ" >

< img


class ="tag-image"


src = "https://offentligabeslut.se/wp-content/uploads/2023/02/position2-1.png"
/ >
< p


class ="tag-text" > ${result.region} < /p >

< / div >
< div


class ="tag-box biloyat" >

< img


class ="tag-image"


src = "https://offentligabeslut.se/wp-content/uploads/2023/02/Vector.png"
/ >
< p


class ="tag-text capitalize" > ${result.organ} < /p >

< / div >
< / div >
< / div >
< / div >
< div


class ="body-text-holder" >

< p


class ="body-text" >

${con1}
< / p >
< / div >
< div


class ="footer-info-holder" >

< div


class ="pdf-info-holder" >

< div


class ="pdf-size-holder" >

< img


class ="pdf-size-image"


src = "https://offentligabeslut.se/wp-content/uploads/2023/02/Vector-1.png"
/ >
< p


class ="pdf-size-text" > ${result.size}MB < /p >

< / div >
< div


class ="pdf-page-count-holder" >

< img


class ="pdf-count-image"


src = "https://offentligabeslut.se/wp-content/uploads/2023/02/5.png"
/ >
< p


class ="pdf-count-text" > ${result.pages} < /p >

< / div >
< / div >
< div


class ="pdf-button-holder" >

< a
href =${result.file}


class ="pdf-oppener pdf-button d_btn" target="_blank" > Öppna < /a >

< a


class ="pdf-download pdf-button cursor d_btn" onclick="downloadPDFReport('${result.file}','${result.filename}')" > Ladda-ner < /a >

< / div >
< / div >
< / div >
`;
con += content;
});
searchResults.innerHTML = con;

let
pagin = "";
if (page !== 1)
{
    pagin += ` < li


class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${1} < /button > < /li > `;

}
if (page !== 1 & & page != = 2) {
pagin += ` < li


class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${2} < /button > < /li > `;

}
if (page !== 1 & & page != = 2 & & page != = 3) {
pagin += ` < li


class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${3} < /button > < /li > `;

}
if (page > 4) {
pagin += ` < li


class ="page-item" > < button class ="page-link" > ${"..."} < /button > < /li > `;

}

if (+page > 4) {
limit = 2
}

for (let i = +page; i <= +page + limit; i++) {
    if (i <= +allDataCount.innerHTML) {
    if (i == = page) {
    pagin += ` < li


    class ="page-item" > < button class ="page-link" style="font-weight: bolder; background: #ffd13a;color: #000;" disabled onclick="clickPage(this)" > ${i} < /button > < /li > `;

    } else {
    pagin += ` < li


    class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${i} < /button > < /li > `;
}
}
}

// if (page < +allDataCount.innerHTML - 5) {
// pagin += ` < li


class ="page-item" > < button class ="page-link" > ${"..."} < /button > < /li > `;

//}

// if (page !== +allDataCount.innerHTML - 1) {
// pagin += ` < li


class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${+allDataCount.innerHTML - 1} < /button > < /li > `;

//}
// if (page !== +allDataCount.innerHTML & & page != = +allDataCount.innerHTML - 1) {
// pagin += ` < li


class ="page-item" > < button class ="page-link" onclick="clickPage(this)" > ${+allDataCount.innerHTML} < /button > < /li > `;

//}

pagin_div.innerHTML = pagin;

// jQuery(document).ready(function($) {
                                      // // Din
SimplePagination.js - kod
här
// var
totalPages = 10; // Ersätt
med
totala
antalet
sidor
//
//    $('#pagination').pagination({
                                  // items: totalPages,
// itemsOnPage: 1,
// cssStyle: 'light-theme',
// onPageClick: function(pageNumber)
{
// var
showFrom = perPage * (pageNumber - 1);
// var
showTo = showFrom + perPage;
// items.hide().slice(showFrom, showTo).show();
// console.log("Salom")
   //}
//});
//});
//

// window.scrollTo(0, 3200);
// Skrolla
till
toppen
av
sidan

// Skrolla
till
toppen
av
sidan

}



select1.addEventListener("change", (e) = > {

if (!select1.value) {
inform__region = "";
inform__country = select1.value;
select2.innerHTML = select;
select2.value = "";
renderCard(
` /files/ ?search=${searchVal} & file_date=${file_date__year} & region=${inform__region} & organ=${inform__organ} & country=${inform__country} & ordering=${order_senaste}`
);
return
}
select2.value = "";
inform__region = "";
inform__country = select1.value;
renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);

for (const key in filter) {
    if (key == select1.value) {
    changeKommon(filter[key]);
    }
}

});

select2.addEventListener("change", () = > {
    inform__region = select2.value;
console.log(inform__region);
renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);
});

select3.addEventListener("change", () = > {
    inform__organ = select3.value;
renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);
});

select4.addEventListener("change", () = > {
    file_date__year = select4.value;
renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);
});

select6.addEventListener("change", () = > {
    order_senaste = select6.value;
console.log(order_senaste)
renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);
});

allDataBtn.addEventListener("click", (event) = > {
    event.preventDefault();
select1.value = "";
select2.value = "";
select3.value = "";
select4.value = "";
select6.value = "";
searchInput.value = "";
inform__country = "";
inform__region = "";
inform__organ = "";
file_date__year = "";
order_senaste = "";
searchVal = "";
select2.innerHTML = select;
renderCard(
` / files /?page =${curPage} & search =${searchVal} & file_date =${file_date__year} & iregion =${
                                                                                                    inform__region} & organ =${
                                                                                                                                  inform__organ} & country =${
                                                                                                                                                                 inform__country} & ordering =${
    order_senaste}
`
);
});

function
changeKommon(lan)
{
    options2 = "";
options2 += select;
for (const key in lanAndKom)
{
if (key == lan)
{
let
kommon = lanAndKom[key];
for (const k in kommon) {

    options2 += ` < option value="${k}" > ${kommon[k]} < /option > `;
}
}
}
select2.innerHTML = options2;
inform__region = select2.value;
}

renderCard("/files")

searchInput.addEventListener("change", (event) = > {
    event.preventDefault();

})

searchForm.addEventListener("submit", async (event) = > {
    event.preventDefault();
searchVal = searchInput.value.trim();
console.log(searchVal);
if (searchVal.length !=
    = 0 & & searchVal.length < 3 & & !inform__country & & !inform__region & & !inform__organ & & !file_date__year & & !order_senaste)
{
alert("Minumum input symbol: 3");
return;
}
await renderCard(
` / files /?search =${searchVal} & file_date =${file_date__year} & region =${inform__region} & organ =${
                                                                                                           inform__organ} & country =${
                                                                                                                                          inform__country} & ordering =${
    order_senaste}
`
);

});

// Pagination
function
previousPage()
{
if (curPage > 1)
{
    curPage - -;
renderCard(` / files /?page =${curPage} & search =${searchVal} & file_date =${file_date__year} & region =${
                                                                                                              inform__region} & organ =${
                                                                                                                                            inform__organ} & country =${
                                                                                                                                                                           inform__country} & ordering =${
    order_senaste}
`, curPage);
}
}



function
nextPage()
{
if (curPage * pageSize < allData.count)
{
    curPage + +;
renderCard(` / files /?page =${curPage} & search =${searchVal} & file_date =${file_date__year} & region =${
                                                                                                              inform__region} & organ =${
                                                                                                                                            inform__organ} & country =${
                                                                                                                                                                           inform__country} & ordering =${
    order_senaste}
`, curPage);
}
}

function
numPages()
{
return Math.ceil(allData.count / pageSize);
}
window.scrollTo(0, 0);
function
clickPage(e)
{
curPage += e.innerHTML - curPage;

console.log(e.innerHTML)
renderCard(` / files /?page =${e.innerHTML} & search =${searchVal} & file_date =${file_date__year} & region =${
                                                                                                                  inform__region} & organ =${
                                                                                                                                                inform__organ} & country =${
                                                                                                                                                                               inform__country} & ordering =${
    order_senaste}
`, curPage);
}

// Pagination
Buttons
nextButton.addEventListener("click", nextPage, false);
prevButton.addEventListener("click", previousPage, false);

// Fetch
data
From
Rest
Api
async function
getData(param)
{
const
response = await fetch(apiURL + param, {
    method: "GET",
    headers: {
        Authorization: "Bearer " + token,
    },
});

const
data = await response.json();
return data;
}




function
downloadPDFReport(pdfLink, nameOfFile)
{
$.ajax({
    url: pdfLink,
    method: 'GET',
    xhrFields: {
        responseType: 'blob'
    },
    success: function(data) {
        var a = document.createElement('a');
var
url = window.URL.createObjectURL(data);
a.href = url;
a.download = `${nameOfFile}.pdf
`;
document.body.append(a);
a.click();
a.remove();
window.URL.revokeObjectURL(url);
}
});
}


