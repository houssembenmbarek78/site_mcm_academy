const fondImageUrl = `url("/digimoov_website_templates/static/img/fond.jpg")`;
const examenUrl = `url("/digimoov_website_templates/static/img/Examen_de_capacité_de_transport_léger_de_marchandise.jpg")`;

if (document.getElementById("examen-fond")) {
  document.getElementById("examen-fond").style.backgroundImage = fondImageUrl;

  console.log(
    "changee fond.jpg",
    document.getElementById("examen-fond").style.backgroundImage
  );
}
if (document.getElementById("examen-fond-2")) {
  document.getElementById("examen-fond").style.backgroundImage = fondImageUrl;

  console.log(
    "changee fond.jpg",
    document.getElementById("examen-fond").style.backgroundImage
  );
}
if (document.getElementById("examen-background-examen")) {
  document.getElementById("examen-background-examen").style.backgroundImage =
    examenUrl;

  console.log(
    "changee fond.jpg",
    document.getElementById("examen-background-examen").style.backgroundImage
  );
}
