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
console.log(nav); // log browser
//Safari Browser

if (nav.toUpperCase() == "SAFARI") {
  //replace webp image if Safari browser
  // console.log("SAFARI browser --- ");
  let allImgs = [].slice.call(document.getElementsByTagName("IMG"));
  allImgs.forEach((element) => {
    // console.log(element.getAttribute("data-srcsafari"));
    if (element.getAttribute("data-srcsafari")) {
      element.dataset.src = element.getAttribute("data-srcsafari");
    }
  });
} else {
  console.log("rien à changer");
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
