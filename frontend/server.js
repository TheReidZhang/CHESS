const express = require("express");
const path = require("path");
const cors = require("cors");
const fetch = require("node-fetch");
const session = require("express-session");
const app = express();
app.use(
  session({
    secret: "IMustSayItsWorth",
    resave: false,
    saveUninitialized: false,
    store: new (require("connect-pg-simple")(session))({
      conString:
        "postgres:postgres:cmsc435team5@chess.czqnldjtsqip.us-east-2.rds.amazonaws.com:5432",
    }),
    cookie: { maxAge: 30 * 24 * 60 * 60 * 1000 },
  })
);

// const proxy = "http://0.0.0.0:5000";
const proxy = "http://backend:5000";
app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "build/")));

app.get("/user", function (req, res) {
  if (req.session.user) {
    fetch(proxy + "/user", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user: req.session.user,
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  } else {
    res.json({ valid: false });
  }
});

app.get("/logout", function (req, res) {
  req.session.destroy((err) => {
    if (err) {
      console.log("Error!");
    }
    res.json({ msg: "logged out" });
  });
});

app.post("/login", function (req, res) {
  if (req.session.user) {
    res.json({ valid: false });
  } else {
    const { username, password } = req.body;
    fetch(proxy + "/login", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        if (json["valid"]) req.session.user = username;
        res.json(json);
      });
  }
});

app.post("/chess/info", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/chess/info", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        session_id: req.body.session_id,
        user: req.session.user,
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.get("/resume", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/resume", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        user: req.session.user,
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.post("/chess/new", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    const { mode } = req.body;
    fetch(proxy + "/chess/new", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        ...req.body,
        ...{ user: req.session.user },
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.post("/chess/update", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/chess/update", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        ...req.body,
        ...{ user: req.session.user },
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.get("/chess/:session_id/:coordinate", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    const {session_id, coordinate} = req.params;
    fetch(proxy + "/chess/" + session_id + "/" + coordinate, {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        user: req.session.user,
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});


app.get("/replays", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/replays", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        user: req.session.user,
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.post("/replay", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/replay", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        ...req.body,
        ...{user: req.session.user}
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.post("/undo", function (req, res) {
  if (!req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/undo", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        ...req.body,
        ...{user: req.session.user}
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});


app.post("/signup", function (req, res) {
  if (req.session.user) {
    res.json({ valid: false });
  } else {
    fetch(proxy + "/signup", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        ...req.body
      }),
    })
      .then((response) => response.json())
      .then((json) => res.json(json));
  }
});

app.get("/*", (req, res) => {
  res.sendFile(path.join(__dirname, ".", "build", "index.html"));
});

app.listen(3000);
