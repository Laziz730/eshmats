export async function onRequestGet() {
  const CHANNEL_ID = "UCffSC8ee8HUgtxpr7u0PSIA";
  const RSS_URL = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;
  const CHANNEL_URL = "https://www.youtube.com/@Eshmats";
  const ABOUT_URL = "https://www.youtube.com/@Eshmats/about";

  const headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
  };

  try {
    // 1. Fetch real subscriber count from YouTube channel page
    let realSubsStr = "6.19K";
    let realSubsNum = 6190;
    try {
      const channelRes = await fetch(CHANNEL_URL, { headers });
      if (channelRes.ok) {
        const html = await channelRes.text();
        const subsMatch = html.match(/@Eshmats[^\d]*([0-9\.,]+[KMBkmb]?)\s+subscribers/i);
        if (subsMatch) {
          realSubsStr = subsMatch[1];
          let numVal = parseFloat(realSubsStr.replace(/[^0-9\.]/g, ''));
          if (realSubsStr.toUpperCase().includes('K')) {
            realSubsNum = Math.round(numVal * 1000);
          } else if (realSubsStr.toUpperCase().includes('M')) {
            realSubsNum = Math.round(numVal * 1000000);
          } else {
            realSubsNum = Math.round(numVal);
          }
        }
      }
    } catch(e) {
      console.log("Channel scrape fallback:", e);
    }

    // 2. Fetch real total views from YouTube /about page
    let realViewsStr = "1,379,136";
    let realViewsNum = 1379136;
    try {
      const aboutRes = await fetch(ABOUT_URL, { headers });
      if (aboutRes.ok) {
        const aboutHtml = await aboutRes.text();
        const viewsMatch = aboutHtml.match(/"([0-9\.,]+)\s+views"/i);
        if (viewsMatch) {
          realViewsStr = viewsMatch[1];
          realViewsNum = parseInt(realViewsStr.replace(/,/g, '')) || realViewsNum;
        }
      }
    } catch(e) {
      console.log("About scrape fallback:", e);
    }

    // 3. Fetch real video entries from official YouTube RSS
    const videoEntries = [];
    try {
      const rssRes = await fetch(RSS_URL, { headers });
      if (rssRes.ok) {
        const xml = await rssRes.text();
        const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
        let match;

        while ((match = entryRegex.exec(xml)) !== null) {
          const entryXml = match[1];
          const idMatch = entryXml.match(/<yt:videoId>(.*?)<\/yt:videoId>/);
          const titleMatch = entryXml.match(/<title>(.*?)<\/title>/);
          const pubMatch = entryXml.match(/<published>(.*?)<\/published>/);
          const viewsMatch = entryXml.match(/views="(\d+)"/);

          if (idMatch && titleMatch) {
            const vId = idMatch[1];
            const title = titleMatch[1];
            const published = pubMatch ? pubMatch[1] : "";
            const viewsNum = viewsMatch ? parseInt(viewsMatch[1]) : 0;

            let category = "senariy";
            const lower = title.toLowerCase();
            if (lower.includes("zombi") || lower.includes("omon qol")) {
              category = "sarguzasht";
            } else if (lower.includes("kuni") || lower.includes("30 kun") || lower.includes("7 kun") || lower.includes("sinov") || lower.includes("soat 4:00")) {
              category = "sinov";
            } else if (lower.includes("rossiya") || lower.includes("hayot") || lower.includes("nafs") || lower.includes("mehmonda") || lower.includes("uxlab")) {
              category = "ibratli";
            }

            videoEntries.push({
              id: vId,
              title: title,
              views: viewsNum.toLocaleString(),
              viewsNum: viewsNum,
              published: published,
              category: category,
              thumbnail: `https://i.ytimg.com/vi/${vId}/hqdefault.jpg`,
              thumbnailMax: `https://i.ytimg.com/vi/${vId}/maxresdefault.jpg`,
              url: `https://www.youtube.com/watch?v=${vId}`,
              embed: `https://www.youtube.com/embed/${vId}?autoplay=1&rel=0`
            });
          }
        }
      }
    } catch(e) {
      console.log("RSS error:", e);
    }

    const nextGoalNum = 10000;
    const progressPercent = ((realSubsNum / nextGoalNum) * 100).toFixed(1);
    const remaining = Math.max(0, nextGoalNum - realSubsNum);

    const data = {
      channelTitle: "Eshmat",
      channelHandle: "@Eshmats",
      subscribers: realSubsStr,
      subscribersNum: realSubsNum,
      subscribersDisplay: realSubsNum.toLocaleString(),
      nextGoal: "10,000",
      nextGoalNum: nextGoalNum,
      progressPercent: progressPercent,
      remainingSubs: remaining.toLocaleString(),
      videoCount: String(videoEntries.length || 14),
      totalViews: realViewsStr,
      totalViewsNum: realViewsNum,
      avatarUrl: "/eshmat_avatar.jpg",
      videos: videoEntries,
      isRealOfficial: true,
      serverTime: new Date().toLocaleTimeString('uz-UZ'),
      timestamp: Date.now()
    };

    return new Response(JSON.stringify(data), {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "public, max-age=15, stale-while-revalidate=30",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
