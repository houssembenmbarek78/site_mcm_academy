const fondImageUrl = `url("/digimoov_website_templates/static/img/fond.jpg")`;

if (window.location.pathname == "/examen-capacite-transport-marchandises") {
  const examenUrl = `url("/digimoov_website_templates/static/img/Examen_de_capacité_de_transport_léger_de_marchandise.jpg")`;

  if (document.getElementById("examen-fond")) {
    document.getElementById("examen-fond").style.backgroundImage = fondImageUrl;

    console.log(
      "changed: ",
      document.getElementById("examen-fond").style.backgroundImage
    );
  }
  if (document.getElementById("examen-fond-2")) {
    document.getElementById("examen-fond-2").style.backgroundImage =
      fondImageUrl;

    console.log(
      "changed: ",
      document.getElementById("examen-fond-2").style.backgroundImage
    );
  }
  if (document.getElementById("examen-background-examen")) {
    document.getElementById("examen-background-examen").style.backgroundImage =
      examenUrl;

    console.log(
      "changed: ",
      document.getElementById("examen-background-examen").style.backgroundImage
    );
  }
}
if (window.location.pathname == "/qui-sommes-nous") {
  const quisommesnousUrl = `url("/digimoov_website_templates/static/img/quisommenous.png")`;
  if (document.getElementById("img-quisommenous")) {
    document.getElementById("img-quisommenous").style.backgroundImage =
      quisommesnousUrl;

    console.log(
      "change",
      document.getElementById("img-quisommenous").style.backgroundImage
    );
  }
  if (document.getElementById("img-fond")) {
    document.getElementById("img-fond").style.backgroundImage = fondImageUrl;

    console.log(
      "change",
      document.getElementById("img-fond").style.backgroundImage
    );
  }
}
