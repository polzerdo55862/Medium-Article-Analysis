const fetch = require('node-fetch')

fetch("https://medium.com/_/graphql", {
  "headers": {
    "accept": "*/*",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "apollographql-client-name": "lite",
    "apollographql-client-version": "main-20210709-201441-e2b0667512",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "graphql-operation": "VisitorQuery",
    "medium-frontend-app": "lite/main-20210709-201441-e2b0667512",
    "medium-frontend-path": "/@marcopeixeiro/followers",
    "medium-frontend-route": "ShowUserFollowers",
    "ot-tracer-sampled": "true",
    "ot-tracer-spanid": "2e41b665343b3803",
    "ot-tracer-traceid": "4c6cab8e2a838662",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.2.295221725.1621173585; g_state={\"i_p\":1623770068928,\"i_l\":2}; _parsely_visitor={%22id%22:%22pid=8f4536d17b56e2274f7a0c810c984f39%22%2C%22session_count%22:10%2C%22last_session_ts%22:1623711416645}; nonce=lwErVge1; uid=2686c0a17e1a; sid=1:gTX8sAPOs+tnr/5UEDJ/EgI/IAf6DnSxKXdnXCmOYGCinfLBMOrl65WmYZ/Ghbyt; optimizelyEndUserId=2686c0a17e1a; lightstep_guid/lite-web=5e6344d96db8ce82; lightstep_session_id=1969cbaa5b13685f; lightstep_guid/medium-web=cb10cf35625be98; sz=1519; pr=2.5; tz=-120; __cfruid=10ddcce37f51910c8430eb557f1871ff4c1aec7f-1625153442; _gid=GA1.2.1444921638.1625885234; xsrf=a7b1837955c0; _dd_s=rum=0&expire=1626002835766; _gat=1"
  },
  "referrer": "https://medium.com/@marcopeixeiro/followers",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"operationName\":\"VisitorQuery\",\"variables\":{},\"query\":\"query VisitorQuery {\\n  visitor {\\n    id\\n    isBot\\n    geolocation {\\n      country\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}",
  "method": "POST",
  "mode": "cors"
}).then(x => x.text()).then(text => console.log(text));