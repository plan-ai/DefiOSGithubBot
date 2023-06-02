import fs from "fs";

import { retry } from "@octokit/plugin-retry";
import { throttling } from "@octokit/plugin-throttling";
import { Octokit } from "@octokit/rest";
import _ from "lodash";
import * as util from "./util.js";

const MyOctokit = Octokit.plugin(retry, throttling);

const cfg = _.merge({}, defaults, custom);
const client = new MyOctokit({
  auth: cfg.auth.oAuthToken,
  retry: {
    enabled: process.env.NODE_ENV !== "test",
  },
  throttle: {
    enabled: process.env.NODE_ENV !== "test",
    onRateLimit: (retryAfter, { method, url, request: { retryCount } }) => {
      if (retryCount < 3) {
        client.log.warn(
          `Rate limit exceeded ${
            retryCount + 1
          } times for ${method} ${url}; retrying in ${retryAfter} seconds`
        );
        return true;
      }

      client.log.warn(
        `Rate limit exceeded ${
          retryCount + 1
        } times for ${method} ${url}; aborting`
      );
    },
    onAbuseLimit: (retryAfter, { method, url }) => {
      client.log.warn(`Abuse detected for ${method} ${url}; aborting`);
    },
  },
});
client.cfg = cfg;
client.util = { ...util };
