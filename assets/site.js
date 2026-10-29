// OneView marketing site — navigation toggle and the demo-request form.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  var form = document.getElementById("demo-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var button = form.querySelector("button[type=submit]");

  function show(kind, text) {
    status.className = "form-status " + kind;
    status.textContent = text;
    status.focus();
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var data = Object.fromEntries(new FormData(form).entries());
    var payload = {
      firstName: data.firstName,
      lastName: data.lastName,
      email: data.email,
      phone: data.phone || "",
      company: data.company,
      role: data.role || "",
      banks: data.banks || "",
      message: data.message || "",
      consentProcessing: data.consentProcessing === "on",
      consentMarketing: data.consentMarketing === "on",
      website: data.website || "",
    };

    button.disabled = true;
    button.textContent = "Sending request…";
    try {
      var res = await fetch(form.dataset.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      var body = await res.json().catch(function () { return {}; });
      if (!res.ok) throw new Error(body.error || "The request could not be sent (error " + res.status + ").");
      form.reset();
      show("ok", "Request received. We will email you within two working days to arrange a time.");
      button.textContent = "Request sent";
    } catch (err) {
      show("err", (err && err.message ? err.message : "The request could not be sent.") + " You can also email hello@oneview.co.za.");
      button.disabled = false;
      button.textContent = "Request a demo";
    }
  });
})();
