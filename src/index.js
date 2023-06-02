import fs from "fs";

import { Webhooks, createNodeMiddleware } from "@octokit/webhooks";
import express from "express";

const app = express();
const port = process.env.PORT || 8080;

app.listen(port, () => {
  console.log(`Website is running on http://localhost:${port}`);
});

app.get("/", (request, response) => {
  response.redirect("https://github.com/apps/defios-bot");
});