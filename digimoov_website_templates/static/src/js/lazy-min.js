//check browser
navigator.saysWho = (() => {
  const { userAgent } = navigator;
  let match =
    userAgent.match(
      /(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i
    ) || [];
  let temp;

  if (/trident/i.test(match[1])) {
    temp = /\brv[ :]+(\d+)/g.exec(userAgent) || [];

    return `IE ${temp[1] || ""}`;
  }

  if (match[1] === "Chrome") {
    temp = userAgent.match(/\b(OPR|Edge)\/(\d+)/);

    if (temp !== null) {
      return temp.slice(1).join(" ").replace("OPR", "Opera");
    }

    temp = userAgent.match(/\b(Edg)\/(\d+)/);

    if (temp !== null) {
      return temp.slice(1).join(" ").replace("Edg", "Edge (Chromium)");
    }
  }

  match = match[2]
    ? [match[1], match[2]]
    : [navigator.appName, navigator.appVersion, "-?"];
  temp = userAgent.match(/version\/(\d+)/i);

  if (temp !== null) {
    match.splice(1, 1, temp[1]);
  }

  return match.join(" ");
})();

var nav = navigator.saysWho.substr(0, navigator.saysWho.indexOf(" "));

//Safari Browser

if (nav.toUpperCase() == "SAFARI") {
  // console.log("Browser: ", nav.toUpperCase());
  const fondImageUrl = `url("/digimoov_website_templates/static/img/fond.jpg")`;

  if (window.location.pathname == "/examen-capacite-transport-marchandises") {
    const examenUrl = `url("/digimoov_website_templates/static/img/Examen_de_capacité_de_transport_léger_de_marchandise.jpg")`;

    if (document.getElementById("examen-fond")) {
      document.getElementById("examen-fond").style.backgroundImage =
        fondImageUrl;

      // console.log(
      //   "changed: ",
      //   document.getElementById("examen-fond").style.backgroundImage
      // );
    }
    if (document.getElementById("examen-fond-2")) {
      document.getElementById("examen-fond-2").style.backgroundImage =
        fondImageUrl;

      // console.log(
      //   "changed: ",
      //   document.getElementById("examen-fond-2").style.backgroundImage
      // );
    }
    if (document.getElementById("examen-background-examen")) {
      document.getElementById(
        "examen-background-examen"
      ).style.backgroundImage = examenUrl;

      // console.log(
      //   "changed: ",
      //   document.getElementById("examen-background-examen").style
      //     .backgroundImage
      // );
    }
  } else if (window.location.pathname == "/qui-sommes-nous") {
    const quisommesnousUrl = `url("/digimoov_website_templates/static/img/quisommenous.png")`;
    if (document.getElementById("img-quisommenous")) {
      document.getElementById("img-quisommenous").style.backgroundImage =
        quisommesnousUrl;

      // console.log(
      //   "change",
      //   document.getElementById("img-quisommenous").style.backgroundImage
      // );
    }
    if (document.getElementById("img-fond")) {
      document.getElementById("img-fond").style.backgroundImage = fondImageUrl;

      //   console.log(
      //     "change",
      //     document.getElementById("img-fond").style.backgroundImage
      //   );
    }
  }
  let allImgs = [].slice.call(document.getElementsByTagName("IMG"));
  allImgs.forEach((element) => {
    // console.log(element.getAttribute("data-srcSafari"));
    if (element.getAttribute("data-srcSafari")) {
      element.dataset.src = element.getAttribute("data-srcSafari");
    }
  });
} else {
  console.log("Navigateur: ", nav); // log browser
}

document.addEventListener("DOMContentLoaded", function () {
  var e = [].slice.call(document.querySelectorAll("img.lazy"));
  if ("IntersectionObserver" in window) {
    let n = new IntersectionObserver(function (e, t) {
      e.forEach(function (e) {
        if (e.isIntersecting) {
          let t = e.target;
          (t.src = t.dataset.src), t.classList.remove("lazy"), n.unobserve(t);
        }
      });
    });
    e.forEach(function (e) {
      n.observe(e);
    });
  }
});
