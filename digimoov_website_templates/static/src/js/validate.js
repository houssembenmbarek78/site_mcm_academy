// document.addEventListener("DOMContentLoaded", function () {
//   const promos = {
//     solo: ["deliveroo", "ubereats", "coursierjob"],
//     // pro: ["pro1", "pro2", "pro3"],
//   };
//   //n = 0 => solo | n=1 =>pro
//   const checkCode = function (n, val) {
//     if (val !== "") {
//       console.log(promos.pro);
//       if (promos.solo.includes(val)) {
//         console.log("foundit");
//         return true;
//       }
//     }
//     return false;
//   };

//   const onChange = function (evt) {
//     const value = evt.target.value;
//     if (window.location.pathname.includes("formation-solo")) {
//       btn_appliquer.disabled = !checkCode(1, value);
//       // console.log(checkCode(1, value));
//       // if (checkCode(1, value)) btn_appliquer.disabled = false;
//     }

//     if (window.location.pathname.includes("formation-pro")) {
//       btn_appliquer.disabled = !checkCode(2, value);
//     }
//   };
//   var promocode = document.getElementById("promo_code");
//   if (window.location.pathname.includes("formation-premium")) {
//     promocode.style.style.display = "none";
//     console.log("none");
//   }
//   var input = document.getElementById("promo_input");
//   var btn_appliquer = document.getElementById("appliquer_promo");
//   btn_appliquer.disabled = true;
//   input.addEventListener("input", onChange, false);
// });
