import { onRequestGet as __api_channel_js_onRequestGet } from "/home/abdulaziz/Desktop/eshmat_official/functions/api/channel.js"
import { onRequestGet as __api_visit_js_onRequestGet } from "/home/abdulaziz/Desktop/eshmat_official/functions/api/visit.js"

export const routes = [
    {
      routePath: "/api/channel",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_channel_js_onRequestGet],
    },
  {
      routePath: "/api/visit",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_visit_js_onRequestGet],
    },
  ]